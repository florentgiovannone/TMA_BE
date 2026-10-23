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
    registration_id = store.insert_unconfirmed(VALUES, "hash-1")
    row = store.get_registration(registration_id)
    assert row["expires_at"] - row["created_at"] == timedelta(minutes=5)
    assert row["status"] == "unconfirmed"
    store.expire_for_tests(registration_id)
    store.purge_expired()
    assert store.get_registration(registration_id) is None


def test_a_second_unconfirmed_insert_for_the_same_pair_is_rejected(store):
    store.insert_unconfirmed(VALUES, "hash-1")
    with pytest.raises(psycopg2.errors.UniqueViolation):
        store.insert_unconfirmed(VALUES, "hash-2")


def test_replace_updates_the_hash_and_keeps_one_unconfirmed_row(store):
    registration_id = store.insert_unconfirmed(VALUES, "hash-1")
    replaced = {**VALUES, "town": "London"}
    store.replace_unconfirmed(registration_id, replaced, "hash-2")
    row = store.get_registration(registration_id)
    assert row["town"] == "London"
    assert row["token_hash"] == "hash-2"
    assert row["status"] == "unconfirmed"
    assert store.find_pair("ada@example.com", "the-star-of-bethlehem")["id"] == registration_id
