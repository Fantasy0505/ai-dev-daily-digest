from __future__ import annotations

import os
from dataclasses import dataclass


class ConfigurationError(RuntimeError):
    """Raised when a required deployment setting is missing."""


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_model: str
    resend_api_key: str
    sender_email: str
    recipient_email: str
    max_items: int
    timeout_seconds: int

    @classmethod
    def from_environment(cls) -> "Settings":
        required = ("OPENAI_API_KEY", "RESEND_API_KEY", "SENDER_EMAIL", "RECIPIENT_EMAIL")
        missing = [name for name in required if not os.getenv(name, "").strip()]
        if missing:
            raise ConfigurationError("Missing required environment variables: " + ", ".join(missing))
        return cls(
            openai_api_key=os.environ["OPENAI_API_KEY"],
            openai_model=os.getenv("OPENAI_MODEL", "").strip() or "gpt-4.1-mini",
            resend_api_key=os.environ["RESEND_API_KEY"],
            sender_email=os.environ["SENDER_EMAIL"],
            recipient_email=os.environ["RECIPIENT_EMAIL"],
            max_items=max(1, min(int(os.getenv("MAX_ITEMS", "12")), 12)),
            timeout_seconds=max(5, min(int(os.getenv("REQUEST_TIMEOUT_SECONDS", "20")), 60)),
        )
