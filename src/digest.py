from __future__ import annotations

import json
import logging
import re

from openai import OpenAI

from .models import Article, DigestItem

LOGGER = logging.getLogger(__name__)

SYSTEM_INSTRUCTIONS = """浣犳槸涓ヨ皑鐨勪腑鏂囨妧鏈柊闂荤紪杈戙€傚彧鑳芥牴鎹緭鍏ヤ腑鐨勬爣棰樸€佹潵婧愩€佸彂甯冩椂闂村拰鎽樺綍鍐欎綔锛屼笉鑳借ˉ鍏呮湭缁忔彁渚涚殑鏁版嵁銆佸姛鑳姐€佹椂闂存垨缁撹銆傝緭鍑虹畝娲併€佷笓涓氥€侀潰鍚戞妧鏈粠涓氳€呯殑绠€浣撲腑鏂囥€傛妧鏈悕璇嶅拰椤圭洰鍚嶅彲浠ヤ繚鐣欒嫳鏂囥€傛瘡椤规憳瑕佷负 2 鑷?4 涓畬鏁翠腑鏂囧彞瀛愶紝蹇呴』鍚屾椂璇存竻鍙戠敓浜嗕粈涔堝強鍏堕噸瑕佹€с€傝嫢淇℃伅涓嶈冻锛屽彧濡傚疄璇存槑杈撳叆鍙‘璁ょ殑浜嬪疄銆?""


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
        "excerpt": article.excerpt or "锛堟潵婧愭湭鎻愪緵鎽樺綍锛?,
    } for article in articles]
    prompt = """璇蜂负浠ヤ笅宸叉牳楠屽€欓€夋柊闂荤敓鎴愭憳瑕併€傛瘡涓€涓緭鍏?id 閮藉繀椤绘伆濂界敓鎴愪竴椤广€傚彧杩斿洖鍚堟硶 JSON锛屼笉瑕?Markdown 鎴栧叾浠栨枃瀛楋紝鏍煎紡蹇呴』鏄細
{"items":[{"id":"杈撳叆涓殑 id","chinese_title":"涓枃鏍囬","summary":"2-4 鍙ヤ腑鏂囨憳瑕?,"tags":["AI"]}]}
鏍囩浠?AI銆佸紑婧愩€佺紪绋嬨€佸畨鍏ㄣ€佺‖浠躲€佸紑鍙戣€呭伐鍏枫€佷簯鍘熺敓銆佽涓?涓€夋嫨 1-3 涓€備笉瑕佽繑鍥炰换浣曟湭鍦ㄨ緭鍏ヤ腑鍑虹幇鐨?id锛屼篃涓嶈鍐欓摼鎺ユ垨鏉ユ簮瀛楁銆?
鍊欓€夋柊闂伙細
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
        summary=article.excerpt or "璇ユ潯鐩殑鍘熷鏉ユ簮鏈彁渚涜冻澶熸憳瑕侊紱璇锋墦寮€鍘熸枃鏍搁獙璇︽儏銆?,
        tags=["鎶€鏈姩鎬?],
    )) for article in articles]


def fallback_items(articles: list[Article]) -> list[DigestItem]:
    """Fail open using only source content if the model is unavailable."""
    LOGGER.warning("Using source-only fallback; no model-generated editorial summary will be sent.")
    return [DigestItem(
        article=article,
        chinese_title=article.title,
        summary=article.excerpt or "璇ユ潯鐩殑鍘熷鏉ユ簮鏈彁渚涜冻澶熸憳瑕侊紱璇锋墦寮€鍘熸枃鏍搁獙璇︽儏銆?,
        tags=["鎶€鏈姩鎬?],
    ) for article in articles]
