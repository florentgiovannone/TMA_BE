import logging

import psycopg2.errors

from birmingham_registration.config import load_settings
from birmingham_registration.service import open_confirmation, submit_registration

SETTINGS = load_settings(
    {
        "DATABASE_URL": "postgresql://localhost/birmingham_registration_test",
        "RESEND_API_KEY": "re_test",
        "RESEND_FROM": "interest@example.com",
        "ADMIN_PASSWORD": "a-long-password",
        "SECRET_KEY": "a-long-secret",
        "PUBLIC_BASE_URL": "http://127.0.0.1:5051",
        "PRIVACY_CONTACT_EMAIL": "privacy@example.com",
    }
)

PAYLOAD = {
    "name": "Ada",
    "surname": "Lovelace",
    "email": "Ada@Example.com",
    "company": "Analytical Engines",
    "position": "Curator",
    "town": "Birmingham",
    "country": "United Kingdom",
    "phoneDialCode": "+44",
    "phoneNumber": "7700900123",
    "phoneExtension": "12",
    "artworkSlug": "the-star-of-bethlehem",
    "consent": True,
}


class FakeMailer:
    def __init__(self, fail=False):
        self.fail = fail
        self.sent = []

    def send_confirmation(self, to_email, artwork_title, confirm_url):
        if self.fail:
            raise RuntimeError("resend down")
        self.sent.append((to_email, artwork_title, confirm_url))


class AllowLimiter:
    def allow_registration(self, email, ip):
        return True


class InsertUniqueViolationStore:
    def __init__(self, inner):
        self._inner = inner

    def __getattr__(self, name):
        return getattr(self._inner, name)

    def insert_unconfirmed(self, values, token_hash):
        raise psycopg2.errors.UniqueViolation()


def test_insert_unique_violation_returns_please_retry_without_email(store):
    store.set_stock("the-star-of-bethlehem", 1)
    mailer = FakeMailer()
    status, body = submit_registration(
        InsertUniqueViolationStore(store),
        mailer,
        AllowLimiter(),
        SETTINGS,
        PAYLOAD,
        "10.0.0.1",
    )
    assert status == 409
    assert body == {
        "ok": False,
        "error": "please_retry",
        "message": "Please try again later.",
    }
    assert mailer.sent == []


def test_first_submit_saves_a_hashed_token_and_emails_the_raw_token(store, caplog):
    store.set_stock("the-star-of-bethlehem", 2)
    mailer = FakeMailer()
    caplog.set_level(logging.INFO)
    status, body = submit_registration(
        store, mailer, AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1"
    )
    assert status == 201
    assert body == {"ok": True}
    assert mailer.sent[0][0] == "ada@example.com"
    assert "token=" in mailer.sent[0][2]
    token = mailer.sent[0][2].split("token=", 1)[1]
    assert token not in caplog.text
    assert "ada@example.com" not in caplog.text
    assert open_confirmation(store, token) == "confirmed"
    assert store.get_artwork("the-star-of-bethlehem")["stock"] == 1


def test_first_send_failure_leaves_no_row(store):
    store.set_stock("the-star-of-bethlehem", 1)
    status, body = submit_registration(
        store, FakeMailer(fail=True), AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1"
    )
    assert status == 502
    assert body["error"] == "email_failed"
    assert store.find_pair("ada@example.com", "the-star-of-bethlehem") is None
    assert store.get_artwork("the-star-of-bethlehem")["stock"] == 1


def test_repeat_replace_miss_returns_502_and_keeps_the_previous_link(store, monkeypatch):
    store.set_stock("the-star-of-bethlehem", 1)
    first = FakeMailer()
    submit_registration(store, first, AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1")
    first_token = first.sent[0][2].split("token=", 1)[1]
    monkeypatch.setattr(store, "replace_unconfirmed", lambda *args, **kwargs: False)
    status, body = submit_registration(
        store, FakeMailer(), AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1"
    )
    assert status == 502
    assert body == {
        "ok": False,
        "error": "email_failed",
        "message": "Please try again later.",
    }
    assert open_confirmation(store, first_token) == "confirmed"


def test_repeat_send_failure_keeps_the_previous_link(store):
    store.set_stock("the-star-of-bethlehem", 1)
    first = FakeMailer()
    submit_registration(store, first, AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1")
    first_token = first.sent[0][2].split("token=", 1)[1]
    status, body = submit_registration(
        store, FakeMailer(fail=True), AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1"
    )
    assert status == 502
    assert open_confirmation(store, first_token) == "confirmed"


def test_repeat_success_retires_the_previous_token(store):
    store.set_stock("the-star-of-bethlehem", 2)
    first = FakeMailer()
    submit_registration(store, first, AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1")
    first_token = first.sent[0][2].split("token=", 1)[1]
    second = FakeMailer()
    submit_registration(store, second, AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1")
    second_token = second.sent[0][2].split("token=", 1)[1]
    assert open_confirmation(store, first_token) == "invalid"
    assert open_confirmation(store, second_token) == "confirmed"
    assert store.get_artwork("the-star-of-bethlehem")["stock"] == 1


def test_one_email_can_register_for_only_one_artwork(store):
    store.set_stock("the-star-of-bethlehem", 2)
    store.set_stock("the-golden-boys", 2)
    mailer = FakeMailer()
    submit_registration(store, mailer, AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1")
    pending = FakeMailer()
    status, body = submit_registration(
        store,
        pending,
        AllowLimiter(),
        SETTINGS,
        {**PAYLOAD, "artworkSlug": "the-golden-boys"},
        "10.0.0.1",
    )
    assert status == 409
    assert body == {
        "ok": False,
        "error": "already_registered",
        "message": "This email is already registered.",
    }
    assert pending.sent == []
    open_confirmation(store, mailer.sent[0][2].split("token=", 1)[1])
    again = FakeMailer()
    status, body = submit_registration(
        store,
        again,
        AllowLimiter(),
        SETTINGS,
        {**PAYLOAD, "artworkSlug": "the-golden-boys"},
        "10.0.0.1",
    )
    assert status == 409
    assert body["error"] == "already_registered"
    assert again.sent == []
    assert store.get_artwork("the-golden-boys")["stock"] == 2


def test_confirmed_pair_and_zero_stock_do_not_send_mail(store):
    store.set_stock("the-star-of-bethlehem", 1)
    mailer = FakeMailer()
    submit_registration(store, mailer, AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1")
    open_confirmation(store, mailer.sent[0][2].split("token=", 1)[1])
    status, body = submit_registration(
        store, FakeMailer(), AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1"
    )
    assert status == 409
    assert body["error"] == "already_registered"
    other = {**PAYLOAD, "email": "grace@example.com"}
    status, body = submit_registration(
        store, FakeMailer(), AllowLimiter(), SETTINGS, other, "10.0.0.1"
    )
    assert status == 409
    assert body["error"] == "unavailable"


class DenyLimiter:
    def allow_registration(self, email, ip):
        return False


def test_over_the_limit_saves_nothing(store):
    store.set_stock("the-star-of-bethlehem", 1)
    status, body = submit_registration(
        store, FakeMailer(), DenyLimiter(), SETTINGS, PAYLOAD, "10.0.0.1"
    )
    assert status == 429
    assert body["error"] == "too_many_requests"
    assert store.find_pair("ada@example.com", "the-star-of-bethlehem") is None


def test_blank_fields_save_nothing(store):
    status, body = submit_registration(
        store, FakeMailer(), AllowLimiter(), SETTINGS, {}, "10.0.0.1"
    )
    assert status == 400
    assert body["errors"]["name"] == "Enter your name."
    assert store.list_confirmed() == []
