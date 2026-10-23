from birmingham_registration.tests.test_api import build
from birmingham_registration.tests.test_service import PAYLOAD, FakeMailer


def log_in(client, password="a-long-password"):
    page = client.get("/admin/login")
    token = page.get_data(as_text=True).split('name="csrf_token" value="', 1)[1].split('"', 1)[0]
    return client.post(
        "/admin/login",
        data={"password": password, "csrf_token": token},
        follow_redirects=True,
    )


def test_wrong_password_does_not_open_the_admin_list(store):
    client = build(store).test_client()
    page = log_in(client, password="wrong")
    assert b"The password is incorrect." in page.data
    assert client.get("/admin").status_code == 302


def test_admin_lists_and_exports_only_confirmed_people(store):
    store.set_stock("the-star-of-bethlehem", 1)
    mailer = FakeMailer()
    client = build(store, mailer).test_client()
    client.post("/api/registrations", json=PAYLOAD)
    token = mailer.sent[0][2].split("token=", 1)[1]
    client.get(f"/confirm?token={token}")
    store.insert_unconfirmed(
        {
            "name": "Hidden",
            "surname": "Person",
            "email": "hidden@example.com",
            "company": "Secret Co",
            "position": "Guest",
            "town": "Birmingham",
            "country": "United Kingdom",
            "artwork_slug": "the-golden-boys",
        },
        "923928026d5d143618c25a098db0c86677cc1994439d66ff8ed71904e10d8339",
    )
    page = log_in(client)
    assert b"Ada" in page.data
    assert b"Hidden" not in page.data
    assert b"The Star of Bethlehem" in page.data
    csv_response = client.get("/admin/registrations.csv")
    text = csv_response.get_data(as_text=True)
    assert "ada@example.com" in text
    assert "hidden@example.com" not in text
    assert csv_response.mimetype == "text/csv"


def test_delete_removes_the_person_and_leaves_stock_alone(store):
    store.set_stock("the-star-of-bethlehem", 2)
    mailer = FakeMailer()
    client = build(store, mailer).test_client()
    client.post("/api/registrations", json=PAYLOAD)
    token = mailer.sent[0][2].split("token=", 1)[1]
    client.get(f"/confirm?token={token}")
    log_in(client)
    registration_id = store.list_confirmed()[0]["id"]
    page = client.get("/admin")
    csrf = page.get_data(as_text=True).split('name="csrf_token" value="', 1)[1].split('"', 1)[0]
    client.post(
        f"/admin/registrations/{registration_id}/delete",
        data={"csrf_token": csrf},
        follow_redirects=True,
    )
    assert store.list_confirmed() == []
    assert store.get_artwork("the-star-of-bethlehem")["stock"] == 1


def test_stock_rejects_a_negative_number_and_accepts_zero(store):
    client = build(store).test_client()
    log_in(client)
    page = client.get("/admin")
    csrf = page.get_data(as_text=True).split('name="csrf_token" value="', 1)[1].split('"', 1)[0]
    client.post(
        "/admin/artworks/the-golden-boys/stock",
        data={"csrf_token": csrf, "stock": "-1"},
        follow_redirects=True,
    )
    assert store.get_artwork("the-golden-boys")["stock"] == 0
    client.post(
        "/admin/artworks/the-golden-boys/stock",
        data={"csrf_token": csrf, "stock": "3"},
        follow_redirects=True,
    )
    assert store.get_artwork("the-golden-boys")["stock"] == 3
