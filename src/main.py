from __future__ import annotations

import logging
import sys
from datetime import datetime, timedelta, timezone

from .config import ConfigurationError, Settings
from .digest import fallback_items, summarize_articles
from .emailing import render_email, send_email
from .sources import collect_articles

CST = timezone(timedelta(hours=8))


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    try:
        settings = Settings.from_environment()
        articles = collect_articles(settings.timeout_seconds, settings.max_items)
        logging.info("Selected %d articles for the digest", len(articles))
        try:
            items = summarize_articles(articles, settings.openai_api_key, settings.openai_model)
        except Exception:
            logging.exception("OpenAI summarization failed; sending source-derived fallback")
            items = fallback_items(articles)
        today = datetime.now(CST).strftime("%Y-%m-%d")
        send_email(
            api_key=settings.resend_api_key,
            sender=settings.sender_email,
            recipient=settings.recipient_email,
            subject=f"AI 涓庡紑鍙戣€呯儹鐐规棩鎶ワ綔{today}",
            html_body=render_email(items),
            timeout_seconds=settings.timeout_seconds,
        )
        logging.info("Digest email accepted by Resend")
        return 0
    except ConfigurationError as exc:
        logging.error("Configuration error: %s", exc)
    except Exception:
        logging.exception("Digest run failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
