from dataclasses import dataclass
from collections.abc import Mapping

from birmingham_registration.mailer import mailgun_smtp_host, mailgun_smtp_port


REQUIRED_NAMES = (
    "DATABASE_URL",
    "MAILGUN_SMTP_HOST",
    "MAILGUN_SMTP_USERNAME",
    "MAILGUN_SMTP_PASSWORD",
    "MAILGUN_FROM",
    "ADMIN_PASSWORD",
    "SECRET_KEY",
    "PUBLIC_BASE_URL",
    "PRIVACY_CONTACT_EMAIL",
)


@dataclass(frozen=True)
class Settings:
    database_url: str
    database_sslmode: str
    mailgun_smtp_host: str
    mailgun_smtp_port: int
    mailgun_smtp_username: str
    mailgun_smtp_password: str
    mailgun_from: str
    admin_password: str
    secret_key: str
    public_base_url: str
    privacy_contact_email: str
    cors_origins: list[str]
    port: int
    trusted_proxy_hops: int
    contact_recipient_email: str = "info@takemearound.com"

    @property
    def secure_cookies(self) -> bool:
        return self.public_base_url.startswith("https://")


def _non_negative_int_setting(environ: Mapping[str, str], name: str, default: str) -> int:
    raw = environ.get(name, default).strip() or default
    if not raw.isascii() or not raw.isdigit():
        raise RuntimeError(f"{name} must be a non-negative integer")
    return int(raw)


def load_settings(environ: Mapping[str, str]) -> Settings:
    missing = [name for name in REQUIRED_NAMES if not environ.get(name, "").strip()]
    if missing:
        raise RuntimeError("Missing required settings: " + ", ".join(missing))
    origins = [
        item.strip()
        for item in environ.get(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if item.strip()
    ]
    return Settings(
        database_url=environ["DATABASE_URL"].strip(),
        database_sslmode=environ.get("DATABASE_SSLMODE", "prefer").strip() or "prefer",
        mailgun_smtp_host=mailgun_smtp_host(environ["MAILGUN_SMTP_HOST"]),
        mailgun_smtp_port=mailgun_smtp_port(environ.get("MAILGUN_SMTP_PORT", "587")),
        mailgun_smtp_username=environ["MAILGUN_SMTP_USERNAME"].strip(),
        mailgun_smtp_password=environ["MAILGUN_SMTP_PASSWORD"].strip(),
        mailgun_from=environ["MAILGUN_FROM"].strip(),
        admin_password=environ["ADMIN_PASSWORD"].strip(),
        secret_key=environ["SECRET_KEY"].strip(),
        public_base_url=environ["PUBLIC_BASE_URL"].strip().rstrip("/"),
        privacy_contact_email=environ["PRIVACY_CONTACT_EMAIL"].strip(),
        cors_origins=origins,
        port=int(environ.get("PORT", "5051").strip() or "5051"),
        trusted_proxy_hops=_non_negative_int_setting(environ, "TRUSTED_PROXY_HOPS", "0"),
        contact_recipient_email=(
            environ.get("CONTACT_RECIPIENT_EMAIL", "info@takemearound.com").strip()
            or "info@takemearound.com"
        ),
    )
