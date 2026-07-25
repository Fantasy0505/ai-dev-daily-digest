from __future__ import annotations

import calendar
import html
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Callable
from urllib.parse import urlsplit, urlunsplit

import feedparser
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .models import Article

LOGGER = logging.getLogger(__name__)

RSS_FEEDS = (
    ("OpenAI", "https://openai.com/news/rss.xml"),
    ("Google AI", "https://blog.google/technology/ai/rss/"),
    ("Anthropic", "https://www.anthropic.com/news/rss.xml"),
    ("Microsoft Developer", "https://devblogs.microsoft.com/feed/"),
    ("GitHub Blog", "https://github.blog/feed/"),
    ("Python Blog", "https://blog.python.org/feeds/posts/default"),
    ("Rust Blog", "https://blog.rust-lang.org/feed.xml"),
    ("Kubernetes Blog", "https://kubernetes.io/feed.xml"),
)

TOPIC_WORDS = (
    "ai", "artificial intelligence", "llm", "model", "agent", "openai", "anthropic",
    "gemini", "copilot", "machine learning", "deep learning", "gpu", "nvidia",
    "programming", "developer", "software", "code", "coding", "python", "javascript",
    "typescript", "rust", "java", "go", "linux", "kubernetes", "cloud native", "api",
    "open source", "github", "security", "vulnerability", "cve", "database", "compiler",
    "framework", "release", "sdk", "devops", "computer", "computing",
)
LOW_VALUE_WORDS = ("sponsored", "webinar", "register now", "giveaway", "podcast")
SOURCE_BONUS = {
    "OpenAI": 9, "Google AI": 9, "Anthropic": 9, "Microsoft Developer": 7,
    "GitHub Blog": 7, "GitHub Public Data": 7, "Hacker News": 5,
    "Python Blog": 6, "Rust Blog": 6, "Kubernetes Blog": 6,
}


@dataclass(frozen=True)
class SourceResult:
    name: str
    articles: list[Article]


def make_session(timeout_seconds: int) -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=2, connect=2, read=2, status=2, backoff_factor=0.6,
        status_forcelist=(429, 500, 502, 503, 504), allowed_methods=frozenset({"GET"}),
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.headers.update({"User-Agent": "daily-chinese-tech-digest/1.0"})
    session.request_timeout = timeout_seconds  # type: ignore[attr-defined]
    return session


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def normalise_url(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), "", ""))


def is_valid_url(url: str) -> bool:
    parsed = urlsplit(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def parse_entry_time(entry: object) -> datetime | None:
    for attribute in ("published_parsed", "updated_parsed", "created_parsed"):
        parsed = getattr(entry, attribute, None)
        if parsed:
            return datetime.fromtimestamp(calendar.timegm(parsed), tz=UTC)
    return None


def relevance_score(title: str, excerpt: str, source: str) -> int:
    text = f"{title} {excerpt}".lower()
    if any(word in text for word in LOW_VALUE_WORDS):
        return -100
    return SOURCE_BONUS.get(source, 0) + 3 * sum(word in text for word in TOPIC_WORDS)


def fetch_rss(source: str, url: str, timeout_seconds: int, cutoff: datetime) -> SourceResult:
    response = make_session(timeout_seconds).get(url, timeout=timeout_seconds)
    response.raise_for_status()
    parsed = feedparser.parse(response.content)
    articles: list[Article] = []
    for index, entry in enumerate(parsed.entries):
        title = clean_text(getattr(entry, "title", ""))
        link = getattr(entry, "link", "")
        published_at = parse_entry_time(entry)
        excerpt = clean_text(getattr(entry, "summary", "") or getattr(entry, "description", ""))
        if not title or not is_valid_url(link) or not published_at or published_at < cutoff:
            continue
        score = relevance_score(title, excerpt, source)
        if score >= 0:
            articles.append(Article(f"rss-{source}-{index}", title, link, source, published_at, excerpt[:900], score))
    return SourceResult(source, articles)


def fetch_github_repositories(timeout_seconds: int, cutoff: datetime) -> SourceResult:
    # GitHub public Search API is a reproducible proxy for recently trending repositories.
    response = make_session(timeout_seconds).get(
        "https://api.github.com/search/repositories",
        params={"q": f"created:>={cutoff.date().isoformat()}", "sort": "stars", "order": "desc", "per_page": 30},
        timeout=timeout_seconds,
    )
    response.raise_for_status()
    articles: list[Article] = []
    for index, repo in enumerate(response.json().get("items", [])):
        created = datetime.fromisoformat(repo["created_at"].replace("Z", "+00:00"))
        if created < cutoff:
            continue
        description = clean_text(repo.get("description") or "")
        name = repo.get("full_name", "")
        score = relevance_score(f"{name} {description}", description, "GitHub Public Data") + min(repo.get("stargazers_count", 0), 100) // 10
        if score >= 5:
            excerpt = f"{description} 鐜版湁 {repo.get('stargazers_count', 0)} 涓?star銆?
            articles.append(Article(f"github-{repo.get('id', index)}", f"GitHub 鐑棬鏂伴」鐩細{name}", repo["html_url"], "GitHub Public Data", created, excerpt, score))
    return SourceResult("GitHub Public Data", articles)


def fetch_hacker_news(timeout_seconds: int, cutoff: datetime) -> SourceResult:
    session = make_session(timeout_seconds)
    response = session.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=timeout_seconds)
    response.raise_for_status()
    def fetch_story(story_id: int) -> Article | None:
        story_response = make_session(timeout_seconds).get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=timeout_seconds
        )
        story_response.raise_for_status()
        story = story_response.json() or {}
        if story.get("type") != "story" or not story.get("url") or not story.get("title"):
            return None
        published_at = datetime.fromtimestamp(story.get("time", 0), tz=UTC)
        if published_at < cutoff:
            return None
        title = clean_text(story["title"])
        score = relevance_score(title, "", "Hacker News") + min(story.get("score", 0), 500) // 25
        if score >= 8:
            excerpt = f"Hacker News 鐑害 {story.get('score', 0)} 鍒嗭紝{story.get('descendants', 0)} 鏉¤璁恒€?
            return Article(f"hn-{story_id}", title, story["url"], "Hacker News", published_at, excerpt, score)
        return None

    articles: list[Article] = []
    # Bounded concurrency avoids one slow story making the entire daily run miss its window.
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(fetch_story, story_id) for story_id in response.json()[:60]]
        for future in as_completed(futures):
            try:
                article = future.result()
                if article:
                    articles.append(article)
            except Exception as exc:
                LOGGER.warning("Hacker News story unavailable: %s", exc)
    return SourceResult("Hacker News", articles)


def collect_articles(timeout_seconds: int, max_items: int) -> list[Article]:
    """Collect sources independently so one unavailable source cannot fail the digest."""
    cutoff = datetime.now(UTC) - timedelta(hours=24)
    jobs: list[tuple[str, Callable[[], SourceResult]]] = [
        (name, lambda n=name, u=url: fetch_rss(n, u, timeout_seconds, cutoff))
        for name, url in RSS_FEEDS
    ]
    jobs.extend([
        ("GitHub Public Data", lambda: fetch_github_repositories(timeout_seconds, cutoff)),
        ("Hacker News", lambda: fetch_hacker_news(timeout_seconds, cutoff)),
    ])
    collected: list[Article] = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(job): name for name, job in jobs}
        for future in as_completed(futures):
            name = futures[future]
            try:
                result = future.result()
                collected.extend(result.articles)
                LOGGER.info("%s: collected %s timely candidates", result.name, len(result.articles))
            except Exception as exc:
                LOGGER.warning("%s unavailable: %s", name, exc)
    return select_articles(collected, max_items)


def select_articles(articles: list[Article], max_items: int) -> list[Article]:
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    selected: list[Article] = []
    for article in sorted(articles, key=lambda item: (item.score, item.published_at), reverse=True):
        url = normalise_url(article.url)
        title = re.sub(r"\W+", "", article.title.lower())
        if url in seen_urls or title in seen_titles:
            continue
        seen_urls.add(url)
        seen_titles.add(title)
        selected.append(article)
        if len(selected) == max_items:
            break
    return selected
