from birmingham_registration.app import create_app
from birmingham_registration.rate_limit import MemoryRateLimiter
from birmingham_registration.tests.test_service import PAYLOAD, SETTINGS, FakeMailer


def build(store, mailer=None, limiter=None):
    application = create_app(
        SETTINGS,
        store,
        mailer or FakeMailer(),
        limiter or MemoryRateLimiter(),
    )
    application.config.update(TESTING=True)
    return application


def test_health_and_artworks_hide_nothing_and_expose_the_privacy_contact(store):
    client = build(store).test_client()
    assert client.get("/api/health").get_json() == {"ok": True}
    payload = client.get("/api/artworks").get_json()
    assert payload["privacyContact"] == "privacy@example.com"
    assert payload["artworks"][0]["available"] is False
    assert payload["artworks"][0]["stock"] == 0


def test_post_then_confirm_shows_the_thank_you_page_once(store):
    store.set_stock("the-star-of-bethlehem", 1)
    mailer = FakeMailer()
    client = build(store, mailer).test_client()
    response = client.post("/api/registrations", json=PAYLOAD)
    assert response.status_code == 201
    token = mailer.sent[0][2].split("token=", 1)[1]
    page = client.get(f"/confirm?token={token}")
    assert page.status_code == 200
    assert b"Your interest is registered." in page.data
    assert page.headers["Referrer-Policy"] == "no-referrer"
    assert token.encode() not in page.data
    again = client.get(f"/confirm?token={token}")
    assert b"This link is invalid or has expired." in again.data
    assert store.get_artwork("the-star-of-bethlehem")["stock"] == 0


def test_confirm_without_stock_says_the_artwork_is_unavailable(store):
    store.set_stock("the-star-of-bethlehem", 1)
    mailer = FakeMailer()
    client = build(store, mailer).test_client()
    client.post("/api/registrations", json=PAYLOAD)
    store.set_stock("the-star-of-bethlehem", 0)
    token = mailer.sent[0][2].split("token=", 1)[1]
    page = client.get(f"/confirm?token={token}")
    assert b"This artwork is no longer available." in page.data
    assert store.find_pair("ada@example.com", "the-star-of-bethlehem")["status"] == "unconfirmed"
