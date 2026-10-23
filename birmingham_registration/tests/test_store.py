import threading
from datetime import timedelta

import psycopg2
import pytest

VALUES = {
    "name": "Ada",
    "surname": "Lovelace",
    "email": "ada@example.com",
    "company": "Analytical Engines",
    "position": "Curator",
    "town": "Birmingham",
    "country": "United Kingdom",
    "artwork_slug": "the-star-of-bethlehem",
}


def test_migrate_seeds_both_artworks_at_zero_and_keeps_stock(store):
    artworks = store.list_artworks()
    assert [(row["slug"], row["title"], row["stock"]) for row in artworks] == [
        ("the-star-of-bethlehem", "The Star of Bethlehem", 0),
        ("the-golden-boys", "The Golden Boys", 0),
    ]
    store.set_stock("the-golden-boys", 4)
    store.migrate()
    assert store.get_artwork("the-golden-boys")["stock"] == 4


def test_insert_expires_in_five_minutes_and_purge_removes_only_old_unconfirmed_rows(store):
    registration_id = store.insert_unconfirmed(VALUES, "73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374")
    row = store.get_registration(registration_id)
    assert row["expires_at"] - row["created_at"] == timedelta(minutes=5)
    assert row["status"] == "unconfirmed"
    store.expire_for_tests(registration_id)
    store.purge_expired()
    assert store.get_registration(registration_id) is None


def test_a_second_unconfirmed_insert_for_the_same_pair_is_rejected(store):
    store.insert_unconfirmed(VALUES, "73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374")
    with pytest.raises(psycopg2.errors.UniqueViolation):
        store.insert_unconfirmed(VALUES, "68240addda41562dabc703d040452cbd977e8e52035a4addb58a447b3468caad")


def test_replace_updates_the_hash_and_keeps_one_unconfirmed_row(store):
    registration_id = store.insert_unconfirmed(VALUES, "73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374")
    replaced = {**VALUES, "town": "London"}
    store.replace_unconfirmed(registration_id, replaced, "68240addda41562dabc703d040452cbd977e8e52035a4addb58a447b3468caad")
    row = store.get_registration(registration_id)
    assert row["town"] == "London"
    assert row["token_hash"] == "68240addda41562dabc703d040452cbd977e8e52035a4addb58a447b3468caad"
    assert row["status"] == "unconfirmed"
    assert store.find_pair("ada@example.com", "the-star-of-bethlehem")["id"] == registration_id


def test_purge_expired_deletes_only_the_expired_unconfirmed_row(store):
    grace = {**VALUES, "email": "grace@example.com"}
    star = {**grace, "artwork_slug": "the-star-of-bethlehem"}
    golden = {**grace, "artwork_slug": "the-golden-boys"}
    expired_id = store.insert_unconfirmed(star, "73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374")
    active_id = store.insert_unconfirmed(golden, "68240addda41562dabc703d040452cbd977e8e52035a4addb58a447b3468caad")
    store.expire_for_tests(expired_id)
    store.purge_expired()
    assert store.get_registration(expired_id) is None
    active = store.get_registration(active_id)
    assert active is not None
    assert active["status"] == "unconfirmed"


def test_insert_unconfirmed_rejects_token_hash_that_is_not_sha256_hex(store):
    with pytest.raises(psycopg2.errors.CheckViolation):
        store.insert_unconfirmed(VALUES, "not-a-sha256")


def test_find_pair_prefers_a_confirmed_row_over_an_unconfirmed_one(store):
    confirmed_id = store.insert_unconfirmed(
        VALUES,
        "73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374",
    )
    conn = store._connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE registrations
                SET status = 'confirmed', token_hash = NULL
                WHERE id = %s
                """,
                (confirmed_id,),
            )
        conn.commit()
    finally:
        conn.close()
    unconfirmed_id = store.insert_unconfirmed(
        VALUES,
        "68240addda41562dabc703d040452cbd977e8e52035a4addb58a447b3468caad",
    )
    pair = store.find_pair("ada@example.com", "the-star-of-bethlehem")
    assert pair["id"] == confirmed_id
    assert pair["status"] == "confirmed"
    assert store.get_registration(unconfirmed_id)["status"] == "unconfirmed"


def test_confirm_subtracts_one_and_a_second_hash_lookup_is_invalid(store):
    store.set_stock("the-star-of-bethlehem", 2)
    registration_id = store.insert_unconfirmed(VALUES, "73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374")
    assert store.confirm("73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374") == "confirmed"
    row = store.get_registration(registration_id)
    assert row["status"] == "confirmed"
    assert row["token_hash"] is None
    assert row["confirmed_at"] is not None
    assert store.get_artwork("the-star-of-bethlehem")["stock"] == 1
    assert store.confirm("73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374") == "invalid"
    assert store.get_artwork("the-star-of-bethlehem")["stock"] == 1


def test_confirm_of_an_unknown_or_expired_token_is_invalid(store):
    registration_id = store.insert_unconfirmed(VALUES, "73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374")
    store.set_stock("the-star-of-bethlehem", 1)
    store.expire_for_tests(registration_id)
    assert store.confirm("73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374") == "invalid"
    assert store.confirm("missing") == "invalid"
    assert store.get_artwork("the-star-of-bethlehem")["stock"] == 1


def test_confirm_with_no_stock_leaves_the_token_in_place(store):
    registration_id = store.insert_unconfirmed(VALUES, "73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374")
    assert store.confirm("73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374") == "unavailable"
    row = store.get_registration(registration_id)
    assert row["status"] == "unconfirmed"
    assert row["token_hash"] == "73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374"
    assert store.get_artwork("the-star-of-bethlehem")["stock"] == 0
    store.set_stock("the-star-of-bethlehem", 1)
    assert store.confirm("73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374") == "confirmed"


def test_two_confirmations_cannot_take_the_last_piece(store):
    store.set_stock("the-star-of-bethlehem", 1)
    store.insert_unconfirmed(VALUES, "73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374")
    other = {**VALUES, "email": "grace@example.com"}
    store.insert_unconfirmed(other, "68240addda41562dabc703d040452cbd977e8e52035a4addb58a447b3468caad")
    results = []

    def confirm(token_hash: str) -> None:
        results.append(store.confirm(token_hash))

    threads = [
        threading.Thread(target=confirm, args=("73a370509b33f7d64369bf097335b57c4021bd28e33a3f12c1b622fd62222374",)),
        threading.Thread(target=confirm, args=("68240addda41562dabc703d040452cbd977e8e52035a4addb58a447b3468caad",)),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert sorted(results) == ["confirmed", "unavailable"]
    assert store.get_artwork("the-star-of-bethlehem")["stock"] == 0
