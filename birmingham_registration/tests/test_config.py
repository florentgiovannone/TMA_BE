import pytest

from birmingham_registration.config import load_settings

REQUIRED = {
    "DATABASE_URL": "postgresql://localhost/birmingham_registration",
    "MAILGUN_SMTP_HOST": "smtp.eu.mailgun.org",
    "MAILGUN_SMTP_USERNAME": "confirmation@mg.example.com",
    "MAILGUN_SMTP_PASSWORD": "secret",
    "MAILGUN_FROM": "Interest <confirmation@mg.example.com>",
    "ADMIN_PASSWORD": "a-long-password",
    "SECRET_KEY": "a-long-secret",
    "PUBLIC_BASE_URL": "https://interest.example.com",
    "PRIVACY_CONTACT_EMAIL": "privacy@example.com",
}


def test_load_settings_applies_defaults_and_https_cookie_flag():
    settings = load_settings(REQUIRED)
    assert settings.database_sslmode == "prefer"
    assert settings.cors_origins == [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    assert settings.port == 5051
    assert settings.trusted_proxy_hops == 0
    assert settings.public_base_url == "https://interest.example.com"
    assert settings.mailgun_smtp_host == "smtp.eu.mailgun.org"
    assert settings.mailgun_smtp_port == 587
    assert settings.secure_cookies is True


def test_load_settings_strips_the_public_url_and_lists_every_missing_name():
    with pytest.raises(RuntimeError) as error:
        load_settings({"PUBLIC_BASE_URL": "http://127.0.0.1:5051/"})
    message = str(error.value)
    for name in REQUIRED:
        if name != "PUBLIC_BASE_URL":
            assert name in message
    settings = load_settings({**REQUIRED, "PUBLIC_BASE_URL": "http://127.0.0.1:5051/"})
    assert settings.public_base_url == "http://127.0.0.1:5051"
    assert settings.secure_cookies is False


def test_load_settings_reads_trusted_proxy_hops():
    settings = load_settings({**REQUIRED, "TRUSTED_PROXY_HOPS": "2"})
    assert settings.trusted_proxy_hops == 2


def test_load_settings_rejects_invalid_trusted_proxy_hops():
    with pytest.raises(RuntimeError):
        load_settings({**REQUIRED, "TRUSTED_PROXY_HOPS": "no"})


def test_load_settings_reads_the_mailgun_smtp_port():
    settings = load_settings({**REQUIRED, "MAILGUN_SMTP_PORT": "465"})
    assert settings.mailgun_smtp_port == 465


def test_load_settings_rejects_a_bad_mailgun_host_or_port():
    with pytest.raises(RuntimeError):
        load_settings({**REQUIRED, "MAILGUN_SMTP_HOST": "smtp.example.com"})
    with pytest.raises(RuntimeError):
        load_settings({**REQUIRED, "MAILGUN_SMTP_PORT": "25"})
