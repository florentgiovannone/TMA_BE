from dataclasses import dataclass
from collections.abc import Mapping


REQUIRED_NAMES = (
    "DATABASE_URL",
    "RESEND_API_KEY",
    "RESEND_FROM",
    "ADMIN_PASSWORD",
    "SECRET_KEY",
    "PUBLIC_BASE_URL",
    "PRIVACY_CONTACT_EMAIL",
)


@dataclass(frozen=True)
class Settings:
    database_url: str
    database_sslmode: str
    resend_api_key: str
    resend_from: str
    admin_password: str
    secret_key: str
    public_base_url: str
    privacy_contact_email: str
    cors_origins: list[str]
    port: int

    @property
    def secure_cookies(self) -> bool:
        return self.public_base_url.startswith("https://")


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
        resend_api_key=environ["RESEND_API_KEY"].strip(),
        resend_from=environ["RESEND_FROM"].strip(),
        admin_password=environ["ADMIN_PASSWORD"].strip(),
        secret_key=environ["SECRET_KEY"].strip(),
        public_base_url=environ["PUBLIC_BASE_URL"].strip().rstrip("/"),
        privacy_contact_email=environ["PRIVACY_CONTACT_EMAIL"].strip(),
        cors_origins=origins,
        port=int(environ.get("PORT", "5051").strip() or "5051"),
    )
