from birmingham_registration.validation import validate_registration

VALID = {
    "name": "Ada",
    "surname": "Lovelace",
    "email": "Ada@Example.com",
    "company": "Analytical Engines",
    "position": "Curator",
    "town": "Birmingham",
    "country": "United Kingdom",
    "artworkSlug": "the-star-of-bethlehem",
    "consent": True,
}


def test_accepts_a_complete_registration_and_lowercases_email():
    result = validate_registration(VALID)
    assert result["ok"] is True
    assert result["values"]["email"] == "ada@example.com"
    assert result["values"]["artwork_slug"] == "the-star-of-bethlehem"
    assert validate_registration({**VALID, "artworkSlug": "the-golden-boys"})["ok"] is True


def test_reports_every_blank_field_and_a_missing_checkbox():
    result = validate_registration({})
    assert result == {
        "ok": False,
        "errors": {
            "name": "Enter your name.",
            "surname": "Enter your surname.",
            "email": "Enter a valid email.",
            "company": "Enter your company.",
            "position": "Enter your position.",
            "town": "Enter the town.",
            "country": "Enter the country.",
            "artworkSlug": "Choose an artwork.",
            "consent": "Confirm that we may store these details.",
        },
    }


def test_rejects_an_unknown_artwork_an_invalid_email_and_a_false_checkbox():
    assert validate_registration({**VALID, "artworkSlug": "other"})["errors"] == {
        "artworkSlug": "Choose an artwork."
    }
    assert validate_registration({**VALID, "email": "not-an-email"})["errors"] == {
        "email": "Enter a valid email."
    }
    assert validate_registration({**VALID, "consent": False})["errors"] == {
        "consent": "Confirm that we may store these details."
    }


def test_rejects_fields_over_their_limits():
    limits = {
        "name": 100,
        "surname": 100,
        "email": 254,
        "company": 200,
        "position": 200,
        "town": 100,
        "country": 100,
    }
    for field, limit in limits.items():
        result = validate_registration({**VALID, field: "a" * (limit + 1)})
        assert result["errors"] == {field: f"Use {limit} characters or fewer."}
