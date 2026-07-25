from __future__ import annotations

import html
from datetime import datetime, timedelta, timezone

import requests

from .models import DigestItem

CST = timezone(timedelta(hours=8))


def _e(value: str) -> str:
    return html.escape(value, quote=True)


def render_email(items: list[DigestItem]) -> str:
    date = datetime.now(CST).strftime("%Y 骞?%m 鏈?%d 鏃?)
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
  <p style="font-size:13px;line-height:1.5;margin:0;color:#6b7280">鏉ユ簮锛?a href="{_e(article.url)}" style="color:#4b5563">{_e(article.source)}</a> 路 鍙戝竷浜?{published}锛堝寳浜椂闂达級</p>
</article>''')
    if not cards:
        body = '<p style="font-size:15px;line-height:1.7;color:#374151">杩囧幓 24 灏忔椂鍐咃紝娌℃湁鎵惧埌瓒冲鍙俊涓斾笌涓婚鐩稿叧鐨勫叕寮€鎶ラ亾銆傛湰鏈熶笉琛ュ厖鎴栫寽娴嬪唴瀹广€?/p>'
        overview = "浠婃棩鏆傛棤杈惧埌鏀跺綍鏍囧噯鐨勬妧鏈儹鐐广€?
    else:
        body = "".join(cards)
        overview = f"杩囧幓 24 灏忔椂鍏辩瓫閫夊嚭 {len(cards)} 鏉″€煎緱鎶€鏈粠涓氳€呭叧娉ㄧ殑鍔ㄦ€侊紝娑电洊 AI銆佸紑婧愩€佺紪绋嬩笌寮€鍙戣€呭伐鍏枫€?
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;background:#f3f4f6;font-family:Arial,'Microsoft YaHei',sans-serif;color:#111827">
<main style="max-width:700px;margin:0 auto;background:#fff;padding:32px 30px">
  <header style="border-bottom:3px solid #155eef;padding-bottom:20px">
    <p style="font-size:13px;color:#6b7280;margin:0 0 8px">{date} 路 姣忔棩瀹氭椂鎺ㄩ€?/p>
    <h1 style="font-size:28px;margin:0;color:#111827">AI 涓庡紑鍙戣€呯儹鐐规棩鎶?/h1>
  </header>
  <section style="background:#eff6ff;padding:16px 18px;margin:24px 0;border-radius:8px">
    <strong style="font-size:15px">浠婃棩閫熻</strong><p style="font-size:14px;line-height:1.65;margin:7px 0 0;color:#374151">{overview}</p>
  </section>
  {body}
  <footer style="padding-top:22px;color:#6b7280;font-size:12px;line-height:1.65">
    鏉ユ簮璇存槑锛氬唴瀹逛粎鍩轰簬鍏紑 RSS銆丟itHub 鍏叡鏁版嵁涓?Hacker News 鐨勮繎 24 灏忔椂鏉＄洰鏁寸悊锛涙瘡鏉″潎闄勫師鏂囬摼鎺ャ€傛憳瑕佺敱妯″瀷鏍规嵁宸叉彁渚涚殑鏍囬鍜屾憳褰曠敓鎴愶紝寤鸿鐐瑰嚮鍘熸枃鏍搁獙瀹屾暣涓婁笅鏂囥€?  </footer>
</main></body></html>'''


def send_email(*, api_key: str, sender: str, recipient: str, subject: str, html_body: str, timeout_seconds: int) -> None:
    response = requests.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"from": sender, "to": [recipient], "subject": subject, "html": html_body},
        timeout=timeout_seconds,
    )
    response.raise_for_status()
