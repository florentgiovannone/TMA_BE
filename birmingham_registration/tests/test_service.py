import logging

import psycopg2.errors

from birmingham_registration.config import load_settings
from birmingham_registration.service import open_confirmation, submit_contact, submit_registration

SETTINGS = load_settings(
    {
        "DATABASE_URL": "postgresql://localhost/birmingham_registration_test",
        "MAILGUN_SMTP_HOST": "smtp.eu.mailgun.org",
        "MAILGUN_SMTP_USERNAME": "confirmation@mg.example.com",
        "MAILGUN_SMTP_PASSWORD": "secret",
        "MAILGUN_FROM": "Interest <confirmation@mg.example.com>",
        "ADMIN_PASSWORD": "a-long-password",
        "SECRET_KEY": "a-long-secret",
        "PUBLIC_BASE_URL": "http://127.0.0.1:5051",
        "PRIVACY_CONTACT_EMAIL": "privacy@example.com",
    }
)

CONTACT_PAYLOAD = {
    "name": "Ada Lovelace",
    "email": "Ada@Example.com",
    "organisation": "Analytical Engines",
    "message": "We host a sculpture trail.",
}

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
    "artworkSlug": "the-star-of-betlehem",
    "packNumber": "101",
    "consent": True,
}

PACK_TAKEN = {
    "ok": False,
    "error": "pack_taken",
    "errors": {"packNumber": "This pack number is already registered."},
}


class FakeMailer:
    def __init__(self, fail=False, fail_thank_you=False):
        self.fail = fail
        self.fail_thank_you = fail_thank_you
        self.sent = []
        self.contact_service_sent = []
        self.contact_thank_you_sent = []

    def send_confirmation(self, to_email, artwork_title, confirm_url):
        if self.fail:
            raise RuntimeError("mail down")
        self.sent.append((to_email, artwork_title, confirm_url))

    def send_contact_service_email(self, to_email, values):
        if self.fail:
            raise RuntimeError("mail down")
        self.contact_service_sent.append((to_email, dict(values)))

    def send_contact_thank_you(self, to_email, name):
        if self.fail or self.fail_thank_you:
            raise RuntimeError("mail down")
        self.contact_thank_you_sent.append((to_email, name))


class AllowLimiter:
    def allow_registration(self, email, ip):
        return True

    def allow_contact(self, email, ip):
        return True


class InsertUniqueViolationStore:
    def __init__(self, inner):
        self._inner = inner

    def __getattr__(self, name):
        return getattr(self._inner, name)

    def insert_unconfirmed(self, values, token_hash):
        raise psycopg2.errors.UniqueViolation()


def test_insert_unique_violation_returns_please_retry_without_email(store):
    store.set_stock("the-star-of-betlehem", 1)
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
    store.set_stock("the-star-of-betlehem", 2)
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
    assert store.get_artwork("the-star-of-betlehem")["stock"] == 1


def test_first_send_failure_leaves_no_row(store):
    store.set_stock("the-star-of-betlehem", 1)
    status, body = submit_registration(
        store, FakeMailer(fail=True), AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1"
    )
    assert status == 502
    assert body["error"] == "email_failed"
    assert store.find_pair("ada@example.com", "the-star-of-betlehem") is None
    assert store.get_artwork("the-star-of-betlehem")["stock"] == 1


def test_repeat_replace_miss_returns_502_and_keeps_the_previous_link(store, monkeypatch):
    store.set_stock("the-star-of-betlehem", 1)
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
    store.set_stock("the-star-of-betlehem", 1)
    first = FakeMailer()
    submit_registration(store, first, AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1")
    first_token = first.sent[0][2].split("token=", 1)[1]
    status, body = submit_registration(
        store, FakeMailer(fail=True), AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1"
    )
    assert status == 502
    assert open_confirmation(store, first_token) == "confirmed"


def test_repeat_success_retires_the_previous_token(store):
    store.set_stock("the-star-of-betlehem", 2)
    first = FakeMailer()
    submit_registration(store, first, AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1")
    first_token = first.sent[0][2].split("token=", 1)[1]
    second = FakeMailer()
    submit_registration(store, second, AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1")
    second_token = second.sent[0][2].split("token=", 1)[1]
    assert open_confirmation(store, first_token) == "invalid"
    assert open_confirmation(store, second_token) == "confirmed"
    assert store.get_artwork("the-star-of-betlehem")["stock"] == 1


def test_an_unconfirmed_email_can_resubmit_for_another_artwork_immediately(store):
    store.set_stock("the-star-of-betlehem", 2)
    store.set_stock("the-golden-boys", 2)
    mailer = FakeMailer()
    submit_registration(store, mailer, AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1")
    first_token = mailer.sent[0][2].split("token=", 1)[1]
    pending = FakeMailer()
    status, body = submit_registration(
        store,
        pending,
        AllowLimiter(),
        SETTINGS,
        {**PAYLOAD, "artworkSlug": "the-golden-boys", "packNumber": "001"},
        "10.0.0.1",
    )
    assert status == 201
    assert body == {"ok": True}
    second_token = pending.sent[0][2].split("token=", 1)[1]
    assert open_confirmation(store, first_token) == "invalid"
    assert open_confirmation(store, second_token) == "confirmed"
    assert store.get_artwork("the-star-of-betlehem")["stock"] == 2
    assert store.get_artwork("the-golden-boys")["stock"] == 1
    again = FakeMailer()
    status, body = submit_registration(
        store,
        again,
        AllowLimiter(),
        SETTINGS,
        {**PAYLOAD, "artworkSlug": "the-star-of-betlehem"},
        "10.0.0.1",
    )
    assert status == 409
    assert body["error"] == "already_registered"
    assert again.sent == []


def test_confirmed_pair_and_zero_stock_do_not_send_mail(store):
    store.set_stock("the-star-of-betlehem", 1)
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


def test_a_second_submit_for_the_same_pack_number_is_rejected(store):
    store.set_stock("the-star-of-betlehem", 2)
    first = FakeMailer()
    status, body = submit_registration(
        store, first, AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1"
    )
    assert status == 201
    status, body = submit_registration(
        store,
        FakeMailer(),
        AllowLimiter(),
        SETTINGS,
        {**PAYLOAD, "email": "grace@example.com"},
        "10.0.0.1",
    )
    assert status == 409
    assert body == PACK_TAKEN
    assert store.find_pair("grace@example.com", "the-star-of-betlehem") is None


def test_replacing_an_unconfirmed_row_may_change_to_a_free_pack_number(store):
    store.set_stock("the-star-of-betlehem", 2)
    first = FakeMailer()
    submit_registration(store, first, AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1")
    status, body = submit_registration(
        store,
        FakeMailer(),
        AllowLimiter(),
        SETTINGS,
        {**PAYLOAD, "packNumber": "150"},
        "10.0.0.1",
    )
    assert status == 201
    assert body == {"ok": True}
    row = store.find_pack("150")
    assert row is not None
    assert store.find_pack("101") is None


def test_deleting_a_confirmed_row_frees_its_pack_number(store):
    store.set_stock("the-star-of-betlehem", 2)
    mailer = FakeMailer()
    submit_registration(store, mailer, AllowLimiter(), SETTINGS, PAYLOAD, "10.0.0.1")
    open_confirmation(store, mailer.sent[0][2].split("token=", 1)[1])
    registration_id = store.list_confirmed()[0]["id"]
    store.delete_confirmed(registration_id)
    status, body = submit_registration(
        store,
        FakeMailer(),
        AllowLimiter(),
        SETTINGS,
        {**PAYLOAD, "email": "grace@example.com"},
        "10.0.0.1",
    )
    assert status == 201
    assert body == {"ok": True}


class DenyLimiter:
    def allow_registration(self, email, ip):
        return False

    def allow_contact(self, email, ip):
        return False


def test_over_the_limit_saves_nothing(store):
    store.set_stock("the-star-of-betlehem", 1)
    status, body = submit_registration(
        store, FakeMailer(), DenyLimiter(), SETTINGS, PAYLOAD, "10.0.0.1"
    )
    assert status == 429
    assert body["error"] == "too_many_requests"
    assert store.find_pair("ada@example.com", "the-star-of-betlehem") is None


def test_blank_fields_save_nothing(store):
    status, body = submit_registration(
        store, FakeMailer(), AllowLimiter(), SETTINGS, {}, "10.0.0.1"
    )
    assert status == 400
    assert body["errors"]["name"] == "Enter your name."
    assert store.list_confirmed() == []


def test_submit_contact_sends_service_and_thank_you_emails_without_logging_pii(caplog):
    mailer = FakeMailer()
    caplog.set_level(logging.INFO)
    status, body = submit_contact(mailer, AllowLimiter(), SETTINGS, CONTACT_PAYLOAD, "10.0.0.1")
    assert status == 201
    assert body == {"ok": True}
    assert mailer.contact_service_sent == [
        (
            "info@takemearound.com",
            {
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "organisation": "Analytical Engines",
                "message": "We host a sculpture trail.",
            },
        )
    ]
    assert mailer.contact_thank_you_sent == [("ada@example.com", "Ada Lovelace")]
    assert "ada@example.com" not in caplog.text
    assert "Ada Lovelace" not in caplog.text
    assert "sculpture trail" not in caplog.text


def test_submit_contact_returns_400_on_invalid_fields_and_sends_no_mail():
    mailer = FakeMailer()
    status, body = submit_contact(mailer, AllowLimiter(), SETTINGS, {"name": ""}, "10.0.0.1")
    assert status == 400
    assert body["ok"] is False
    assert body["errors"]["name"] == "Enter your name."
    assert body["errors"]["email"] == "Enter a valid email."
    assert body["errors"]["message"] == "Enter a message."
    assert mailer.contact_service_sent == []
    assert mailer.contact_thank_you_sent == []


def test_submit_contact_returns_429_when_rate_limited():
    mailer = FakeMailer()
    status, body = submit_contact(mailer, DenyLimiter(), SETTINGS, CONTACT_PAYLOAD, "10.0.0.1")
    assert status == 429
    assert body == {
        "ok": False,
        "error": "too_many_requests",
        "message": "Please try again later.",
    }
    assert mailer.contact_service_sent == []


def test_submit_contact_returns_502_when_service_or_thank_you_email_fails():
    status, body = submit_contact(
        FakeMailer(fail=True), AllowLimiter(), SETTINGS, CONTACT_PAYLOAD, "10.0.0.1"
    )
    assert status == 502
    assert body == {
        "ok": False,
        "error": "email_failed",
        "message": "We could not send your message. Please try again later.",
    }
    status_second, body_second = submit_contact(
        FakeMailer(fail_thank_you=True), AllowLimiter(), SETTINGS, CONTACT_PAYLOAD, "10.0.0.1"
    )
    assert status_second == 502
    assert body_second["error"] == "email_failed"
