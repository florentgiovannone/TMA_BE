import os
from pathlib import Path

from dotenv import load_dotenv

from birmingham_registration.app import create_app
from birmingham_registration.config import load_settings
from birmingham_registration.mailer import MailgunMailer
from birmingham_registration.rate_limit import MemoryRateLimiter
from birmingham_registration.store import Store

load_dotenv(Path(__file__).with_name(".env"))
settings = load_settings(os.environ)
store = Store(settings.database_url, settings.database_sslmode)
store.migrate()
application = create_app(
    settings,
    store,
    MailgunMailer(
        settings.mailgun_smtp_host,
        settings.mailgun_smtp_port,
        settings.mailgun_smtp_username,
        settings.mailgun_smtp_password,
        settings.mailgun_from,
    ),
    MemoryRateLimiter(),
)


def main() -> None:
    application.run(host="127.0.0.1", port=settings.port)


if __name__ == "__main__":
    main()
