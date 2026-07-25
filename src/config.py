from __future__ import annotations

import os
from dataclasses import dataclass


class ConfigurationError(RuntimeError):
    """Raised when a required deployment setting is missing."""


@dataclass(frozen=True)
class Settings:
    deepseek_api_key: str
    deepseek_model: str
    resend_api_key: str
    sender_email: str
    recipient_email: str
    max_items: int
    timeout_seconds: int

    @classmethod
    def from_environment(cls) -> "Settings":
        # OPENAI_API_KEY is retained only as a temporary compatibility alias for
        # older workflow files.  Its value is still sent exclusively to DeepSeek.
        deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "").strip() or os.getenv("OPENAI_API_KEY", "").strip()
        required = ("RESEND_API_KEY", "SENDER_EMAIL", "RECIPIENT_EMAIL")
        missing = [name for name in required if not os.getenv(name, "").strip()]
        if not deepseek_api_key:
            missing.insert(0, "DEEPSEEK_API_KEY")
        if missing:
            raise ConfigurationError("Missing required environment variables: " + ", ".join(missing))
        return cls(
            deepseek_api_key=deepseek_api_key,
            deepseek_model=os.getenv("DEEPSEEK_MODEL", "").strip() or "deepseek-v4-flash",
            resend_api_key=os.environ["RESEND_API_KEY"],
            sender_email=os.environ["SENDER_EMAIL"],
            recipient_email=os.environ["RECIPIENT_EMAIL"],
            max_items=max(1, min(int(os.getenv("MAX_ITEMS", "12")), 12)),
            timeout_seconds=max(5, min(int(os.getenv("REQUEST_TIMEOUT_SECONDS", "20")), 60)),
        )
