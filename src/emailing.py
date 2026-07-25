from __future__ import annotations

import html
from datetime import datetime, timedelta, timezone

import requests

from .models import DigestItem

CST = timezone(timedelta(hours=8))


def _e(value: str) -> str:
    return html.escape(value, quote=True)


def render_email(items: list[DigestItem]) -> str:
    date = datetime.now(CST).strftime("%Y 年 %m 月 %d 日")
    cards: list[str] = []
    for item in items:
        article = item.article
        tags = "".join(
            f'<span style="display:inline-block;background:#e8f0fe;color:#174ea6;border-radius:12px;padding:3px 8px;margin:0 5px 6px 0;font-size:12px">{_e(tag)}</span>'
            for tag in item.tags
        )
        published = article.published_at.astimezone(CST).strftime("%m-%d %H:%M")
        cards.append(f'''<article style="padding:22px 0;border-bottom:1px solid #e5e7eb">
  <div style="margin-bottom:8px">{tags}</div>
  <h2 style="font-size:19px;line-height:1.45;margin:0 0 9px;color:#111827"><a href="{_e(article.url)}" style="color:#155eef;text-decoration:none">{_e(item.chinese_title)}</a></h2>
  <p style="font-size:15px;line-height:1.75;margin:0 0 10px;color:#374151">{_e(item.summary)}</p>
  <p style="font-size:13px;line-height:1.5;margin:0;color:#6b7280">来源：<a href="{_e(article.url)}" style="color:#4b5563">{_e(article.source)}</a> · 发布于 {published}（北京时间）</p>
</article>''')
    if not cards:
        body = '<p style="font-size:15px;line-height:1.7;color:#374151">过去 24 小时内，没有找到足够可信且与主题相关的公开报道。本期不补充或猜测内容。</p>'
        overview = "今日暂无达到收录标准的技术热点。"
    else:
        body = "".join(cards)
        overview = f"过去 24 小时共筛选出 {len(cards)} 条值得技术从业者关注的动态，涵盖 AI、开源、编程与开发者工具。"
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;background:#f3f4f6;font-family:Arial,'Microsoft YaHei',sans-serif;color:#111827">
<main style="max-width:700px;margin:0 auto;background:#fff;padding:32px 30px">
  <header style="border-bottom:3px solid #155eef;padding-bottom:20px">
    <p style="font-size:13px;color:#6b7280;margin:0 0 8px">{date} · 每日定时推送</p>
    <h1 style="font-size:28px;margin:0;color:#111827">AI 与开发者热点日报</h1>
  </header>
  <section style="background:#eff6ff;padding:16px 18px;margin:24px 0;border-radius:8px">
    <strong style="font-size:15px">今日速览</strong><p style="font-size:14px;line-height:1.65;margin:7px 0 0;color:#374151">{overview}</p>
  </section>
  {body}
  <footer style="padding-top:22px;color:#6b7280;font-size:12px;line-height:1.65">
    来源说明：内容仅基于公开 RSS、GitHub 公共数据与 Hacker News 的近 24 小时条目整理；每条均附原文链接。摘要由模型根据已提供的标题和摘录生成，建议点击原文核验完整上下文。
  </footer>
</main></body></html>'''


def send_email(*, api_key: str, sender: str, recipient: str, subject: str, html_body: str, timeout_seconds: int) -> None:
    response = requests.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"from": sender, "to": [recipient], "subject": subject, "html": html_body},
        timeout=timeout_seconds,
    )
    response.raise_for_status()
