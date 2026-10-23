from pathlib import Path

import pytest
from dotenv import dotenv_values

from birmingham_registration.store import Store

PACKAGE = Path(__file__).resolve().parents[1]


def database_urls() -> tuple[str, str]:
    test_url = (dotenv_values(PACKAGE / ".env.test").get("DATABASE_URL") or "").strip()
    dev_url = (dotenv_values(PACKAGE / ".env").get("DATABASE_URL") or "").strip()
    if not test_url:
        pytest.exit("DATABASE_URL is missing from birmingham_registration/.env.test", returncode=1)
    if dev_url and test_url == dev_url:
        pytest.exit("Refusing to run tests against the development DATABASE_URL", returncode=1)
    return test_url, dev_url


@pytest.fixture
def store():
    test_url, _dev_url = database_urls()
    subject = Store(test_url, "prefer")
    subject.migrate()
    subject.reset_for_tests()
    yield subject
