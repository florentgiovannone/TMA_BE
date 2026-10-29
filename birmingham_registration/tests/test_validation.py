from birmingham_registration.validation import validate_contact, validate_registration

VALID_CONTACT = {
    "name": "Ada Lovelace",
    "email": "Ada@Example.com",
    "organisation": "Analytical Engines",
    "message": "We host a sculpture trail.",
}

VALID = {
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
    "packNumber": "001",
    "consent": True,
}


def test_accepts_a_complete_registration_and_lowercases_email():
    result = validate_registration(VALID)
    assert result["ok"] is True
    assert result["values"]["email"] == "ada@example.com"
    assert result["values"]["artwork_slug"] == "the-star-of-betlehem"
    assert validate_registration({**VALID, "artworkSlug": "the-golden-boys", "packNumber": "101"})["ok"] is True
    without_phone = validate_registration({**VALID, "phoneNumber": "", "phoneDialCode": ""})
    assert without_phone["ok"] is True
    assert without_phone["values"]["phone_number"] == ""


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
            "country": "Choose a country.",
            "artworkSlug": "Choose an artwork.",
            "packNumber": "Enter a 3-digit pack number.",
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


def test_rejects_a_pack_number_that_is_not_three_digits():
    for value in ("", "7", "12", "0077", "MACD007"):
        assert validate_registration({**VALID, "packNumber": value})["errors"] == {
            "packNumber": "Enter a 3-digit pack number."
        }


def test_rejects_a_pack_number_outside_the_chosen_artwork_range():
    assert validate_registration({**VALID, "packNumber": "000"})["errors"] == {
        "packNumber": "Enter a pack number from 001 to 100."
    }
    assert validate_registration({**VALID, "packNumber": "101"})["errors"] == {
        "packNumber": "Enter a pack number from 001 to 100."
    }
    assert validate_registration({**VALID, "packNumber": "100"})["ok"] is True
    assert validate_registration(
        {**VALID, "artworkSlug": "the-golden-boys", "packNumber": "101"}
    )["ok"] is True
    assert validate_registration(
        {**VALID, "artworkSlug": "the-golden-boys", "packNumber": "200"}
    )["ok"] is True
    assert validate_registration(
        {**VALID, "artworkSlug": "the-golden-boys", "packNumber": "100"}
    )["errors"] == {"packNumber": "Enter a pack number from 101 to 200."}
    assert validate_registration(
        {**VALID, "artworkSlug": "the-golden-boys", "packNumber": "201"}
    )["errors"] == {"packNumber": "Enter a pack number from 101 to 200."}


def test_stores_the_three_digit_pack_number():
    assert validate_registration(VALID)["values"]["pack_number"] == "001"


def test_validate_contact_accepts_valid_payload_and_optional_organisation():
    result = validate_contact(VALID_CONTACT)
    assert result == {
        "ok": True,
        "values": {
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "organisation": "Analytical Engines",
            "message": "We host a sculpture trail.",
        },
    }
    without_org = validate_contact({**VALID_CONTACT, "organisation": "   "})
    assert without_org["ok"] is True
    assert without_org["values"]["organisation"] == ""


def test_validate_contact_rejects_blank_required_fields_and_bad_email():
    assert validate_contact({}) == {
        "ok": False,
        "errors": {
            "name": "Enter your name.",
            "email": "Enter a valid email.",
            "message": "Enter a message.",
        },
    }
    assert validate_contact({**VALID_CONTACT, "email": "not-an-email"}) == {
        "ok": False,
        "errors": {"email": "Enter a valid email."},
    }


def test_validate_contact_rejects_fields_over_their_limits():
    limits = {
        "name": 100,
        "email": 254,
        "organisation": 200,
        "message": 2000,
    }
    for field, limit in limits.items():
        result = validate_contact({**VALID_CONTACT, field: "a" * (limit + 1)})
        assert result == {
            "ok": False,
            "errors": {field: f"Use {limit} characters or fewer."},
        }
