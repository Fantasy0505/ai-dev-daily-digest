from __future__ import annotations

import json
import logging
import re

from openai import OpenAI

from .models import Article, DigestItem

LOGGER = logging.getLogger(__name__)

SYSTEM_INSTRUCTIONS = """你是严谨的中文技术新闻编辑。只能根据输入中的标题、来源、发布时间和摘录写作，不能补充未经提供的数据、功能、时间或结论。输出简洁、专业、面向技术从业者的简体中文。技术名词和项目名可以保留英文。每项摘要为 2 至 4 个完整中文句子，必须同时说清发生了什么及其重要性。若信息不足，只如实说明输入可确认的事实。"""


def _extract_json(text: str) -> object:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\\s*|\\s*```$", "", text, flags=re.IGNORECASE)
    return json.loads(text)


def summarize_articles(articles: list[Article], api_key: str, model: str) -> list[DigestItem]:
    if not articles:
        return []
    payload = [{
        "id": article.id,
        "original_title": article.title,
        "source": article.source,
        "published_at_utc": article.published_at.isoformat(),
        "excerpt": article.excerpt or "（来源未提供摘录）",
    } for article in articles]
    prompt = """请为以下已核验候选新闻生成摘要。每一个输入 id 都必须恰好生成一项。只返回合法 JSON，不要 Markdown 或其他文字，格式必须是：
{"items":[{"id":"输入中的 id","chinese_title":"中文标题","summary":"2-4 句中文摘要","tags":["AI"]}]}
标签从 AI、开源、编程、安全、硬件、开发者工具、云原生、行业 中选择 1-3 个。不要返回任何未在输入中出现的 id，也不要写链接或来源字段。

候选新闻：
""" + json.dumps(payload, ensure_ascii=False)
    client = OpenAI(api_key=api_key)
    response = client.responses.create(model=model, instructions=SYSTEM_INSTRUCTIONS, input=prompt)
    data = _extract_json(response.output_text)
    by_id = {article.id: article for article in articles}
    items_by_id: dict[str, DigestItem] = {}
    for generated in data.get("items", []) if isinstance(data, dict) else []:
        article = by_id.get(generated.get("id")) if isinstance(generated, dict) else None
        title = generated.get("chinese_title", "") if isinstance(generated, dict) else ""
        summary = generated.get("summary", "") if isinstance(generated, dict) else ""
        tags = generated.get("tags", []) if isinstance(generated, dict) else []
        if not article or not isinstance(title, str) or not isinstance(summary, str):
            continue
        safe_tags = [tag for tag in tags if isinstance(tag, str)][:3]
        if title.strip() and summary.strip():
            items_by_id[article.id] = DigestItem(article, title.strip(), summary.strip(), safe_tags)
    if not items_by_id:
        raise ValueError("Model response contained no usable digest items")
    # Keep the editorial result in deterministic ranking order. A partial model response
    # cannot silently discard an otherwise verified news item.
    return [items_by_id.get(article.id, DigestItem(
        article=article,
        chinese_title=article.title,
        summary=article.excerpt or "该条目的原始来源未提供足够摘要；请打开原文核验详情。",
        tags=["技术动态"],
    )) for article in articles]


def fallback_items(articles: list[Article]) -> list[DigestItem]:
    """Fail open using only source content if the model is unavailable."""
    LOGGER.warning("Using source-only fallback; no model-generated editorial summary will be sent.")
    return [DigestItem(
        article=article,
        chinese_title=article.title,
        summary=article.excerpt or "该条目的原始来源未提供足够摘要；请打开原文核验详情。",
        tags=["技术动态"],
    ) for article in articles]
