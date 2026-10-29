from birmingham_registration.app import REGISTRATIONS_READ_HEADER, create_app
from birmingham_registration.rate_limit import MemoryRateLimiter
from birmingham_registration.tests.test_service import PAYLOAD, SETTINGS, DenyLimiter, FakeMailer
from birmingham_registration.tests.test_store import VALUES

READ_HEADERS = {REGISTRATIONS_READ_HEADER: SETTINGS.registrations_read_key}


def build(store, mailer=None, limiter=None):
    application = create_app(
        SETTINGS,
        store,
        mailer or FakeMailer(),
        limiter or MemoryRateLimiter(),
    )
    application.config.update(TESTING=True)
    return application


def test_artworks_purge_removes_expired_unconfirmed_rows_but_keeps_confirmed(store):
    expired_id = store.insert_unconfirmed(
        VALUES,
        "73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374",
    )
    store.expire_for_tests(expired_id)
    confirmed = {
        **VALUES,
        "email": "grace@example.com",
        "artwork_slug": "the-golden-boys",
        "pack_number": "101",
    }
    confirmed_id = store.insert_unconfirmed(
        confirmed,
        "68240addda41562dabc703d040452cbd977e8e52035a4addb58a447b3468caad",
    )
    store.set_stock("the-golden-boys", 1)
    assert store.confirm("68240addda41562dabc703d040452cbd977e8e52035a4addb58a447b3468caad") == "confirmed"
    client = build(store).test_client()
    assert client.get("/api/artworks").status_code == 200
    assert store.get_registration(expired_id) is None
    assert store.get_registration(confirmed_id) is not None


def test_health_and_artworks_hide_nothing_and_expose_the_privacy_contact(store):
    client = build(store).test_client()
    assert client.get("/api/health").get_json() == {"ok": True}
    payload = client.get("/api/artworks").get_json()
    assert payload["privacyContact"] == "privacy@example.com"
    assert payload["artworks"][0]["available"] is False
    assert payload["artworks"][0]["stock"] == 0


def test_post_then_confirm_shows_the_thank_you_page_once(store):
    store.set_stock("the-star-of-betlehem", 1)
    mailer = FakeMailer()
    client = build(store, mailer).test_client()
    response = client.post("/api/registrations", json=PAYLOAD)
    assert response.status_code == 201
    token = mailer.sent[0][2].split("token=", 1)[1]
    page = client.get(f"/confirm?token={token}")
    assert page.status_code == 200
    assert b"Your interest is registered." in page.data
    assert b"Museum Association Conference" in page.data
    assert b"https://takemearound.com/" in page.data
    assert b"Discover more at takemearound.com" in page.data
    assert page.headers["Referrer-Policy"] == "no-referrer"
    assert token.encode() not in page.data
    again = client.get(f"/confirm?token={token}")
    assert b"This link is invalid or has expired." in again.data
    assert store.get_artwork("the-star-of-betlehem")["stock"] == 0


def test_post_contact_sends_service_and_thank_you_emails(store):
    mailer = FakeMailer()
    client = build(store, mailer).test_client()
    response = client.post(
        "/api/contact",
        json={
            "name": "Ada Lovelace",
            "email": "Ada@Example.com",
            "organisation": "Analytical Engines",
            "message": "We host a sculpture trail.",
        },
    )
    assert response.status_code == 201
    assert response.get_json() == {"ok": True}
    assert mailer.contact_service_sent[0][0] == "info@takemearound.com"
    assert mailer.contact_thank_you_sent == [("ada@example.com", "Ada Lovelace")]


CONTACT_JSON = {
    "name": "Ada Lovelace",
    "email": "Ada@Example.com",
    "organisation": "Analytical Engines",
    "message": "We host a sculpture trail.",
}


def test_post_contact_returns_400_429_and_502_on_errors(store):
    client = build(store).test_client()
    bad = client.post("/api/contact", json={"name": ""})
    assert bad.status_code == 400
    assert bad.get_json()["errors"]["name"] == "Enter your name."

    limited = build(store, limiter=DenyLimiter()).test_client()
    too_many = limited.post("/api/contact", json=CONTACT_JSON)
    assert too_many.status_code == 429
    assert too_many.get_json()["error"] == "too_many_requests"

    failing = build(store, mailer=FakeMailer(fail=True)).test_client()
    mail_error = failing.post("/api/contact", json=CONTACT_JSON)
    assert mail_error.status_code == 502
    assert mail_error.get_json()["error"] == "email_failed"


def test_get_registrations_without_the_read_key_hides_personal_data(store):
    store.set_stock("the-star-of-betlehem", 1)
    mailer = FakeMailer()
    client = build(store, mailer).test_client()
    client.post("/api/registrations", json=PAYLOAD)
    token = mailer.sent[0][2].split("token=", 1)[1]
    client.get(f"/confirm?token={token}")
    listed = client.get("/api/registrations")
    assert listed.status_code == 401
    body = listed.get_data(as_text=True)
    assert "ada@example.com" not in body
    assert "Ada" not in body
    assert listed.get_json() == {"ok": False, "error": "unauthorized"}
    wrong = client.get("/api/registrations", headers={REGISTRATIONS_READ_HEADER: "nope"})
    assert wrong.status_code == 401
    assert "ada@example.com" not in wrong.get_data(as_text=True)


def test_get_registrations_returns_confirmed_rows_only(store):
    store.set_stock("the-star-of-betlehem", 2)
    mailer = FakeMailer()
    client = build(store, mailer).test_client()
    client.post("/api/registrations", json=PAYLOAD)
    hidden = {
        **PAYLOAD,
        "email": "hidden@example.com",
        "packNumber": "002",
    }
    client.post("/api/registrations", json=hidden)
    token = mailer.sent[0][2].split("token=", 1)[1]
    client.get(f"/confirm?token={token}")

    listed = client.get("/api/registrations", headers=READ_HEADERS)
    assert listed.status_code == 200
    body = listed.get_json()
    assert "token_hash" not in listed.get_data(as_text=True)
    assert body == {
        "registrations": [
            {
                "name": "Ada",
                "surname": "Lovelace",
                "email": "ada@example.com",
                "phoneDialCode": "+44",
                "phoneNumber": "7700900123",
                "phoneExtension": "12",
                "company": "Analytical Engines",
                "position": "Curator",
                "town": "Birmingham",
                "country": "United Kingdom",
                "artworkSlug": "the-star-of-betlehem",
                "artworkTitle": "The Star of Betlehem",
                "packNumber": "001",
            }
        ]
    }

    by_pack = client.get("/api/registrations?packNumber=001", headers=READ_HEADERS)
    assert by_pack.get_json() == body
    missing = client.get("/api/registrations?packNumber=002", headers=READ_HEADERS)
    assert missing.get_json() == {"registrations": []}
    unknown = client.get("/api/registrations?packNumber=199", headers=READ_HEADERS)
    assert unknown.get_json() == {"registrations": []}


def test_post_registrations_is_unchanged(store):
    store.set_stock("the-star-of-betlehem", 1)
    mailer = FakeMailer()
    client = build(store, mailer).test_client()
    response = client.post("/api/registrations", json=PAYLOAD)
    assert response.status_code == 201
    assert response.get_json() == {"ok": True}


def test_confirm_without_stock_says_the_artwork_is_unavailable(store):
    store.set_stock("the-star-of-betlehem", 1)
    mailer = FakeMailer()
    client = build(store, mailer).test_client()
    client.post("/api/registrations", json=PAYLOAD)
    store.set_stock("the-star-of-betlehem", 0)
    token = mailer.sent[0][2].split("token=", 1)[1]
    page = client.get(f"/confirm?token={token}")
    assert b"This artwork is no longer available." in page.data
    assert store.find_pair("ada@example.com", "the-star-of-betlehem")["status"] == "unconfirmed"
