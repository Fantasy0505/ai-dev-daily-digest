from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Article:
    id: str
    title: str
    url: str
    source: str
    published_at: datetime
    excerpt: str
    score: int


@dataclass(frozen=True)
class DigestItem:
    article: Article
    chinese_title: str
    summary: str
    tags: list[str]
