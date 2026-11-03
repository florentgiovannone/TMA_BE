from birmingham_registration.validation import (
    claimed_redirect_url,
    pack_claim_from_tag,
    validate_contact,
    validate_pack_claim,
    validate_registration,
)

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


def test_admin_registration_allows_a_blank_email_but_rejects_an_invalid_one():
    result = validate_registration({**VALID, "email": ""}, email_required=False)
    assert result["ok"] is True
    assert result["values"]["email"] == ""
    assert validate_registration({**VALID, "email": "   "}, email_required=False)["values"]["email"] == ""
    assert validate_registration({**VALID, "email": "not-an-email"}, email_required=False)["errors"] == {
        "email": "Enter a valid email."
    }


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


CLAIM = {
    "tagCode": "mactgb-3",
    "name": "Ada",
    "surname": "Lovelace",
    "email": "Ada@Example.com",
    "company": "Analytical Engines",
    "consent": True,
    "packNumber": "001",
    "artworkSlug": "the-star-of-betlehem",
}


def test_pack_claim_from_tag_maps_the_three_prefixes():
    assert pack_claim_from_tag("MACTSOB014")["pack_number"] == "014"
    assert pack_claim_from_tag("MACTSOB014")["artwork_slug"] == "the-star-of-betlehem"
    assert pack_claim_from_tag("MACTGB003") == {
        "tag_code": "MACTGB003",
        "pack_number": "103",
        "artwork_slug": "the-golden-boys",
        "kind": "artwork",
        "destination_url": "https://takemearound.museum/the-golden-boys",
    }
    assert pack_claim_from_tag("MACD150")["kind"] == "dashboard"
    assert pack_claim_from_tag("MACD150")["pack_number"] == "150"
    assert pack_claim_from_tag("MACF001") is None
    assert pack_claim_from_tag("MACTGB101") is None


def test_validate_pack_claim_derives_pack_and_ignores_body_pack_and_artwork():
    result = validate_pack_claim(CLAIM)
    assert result["ok"] is True
    assert result["values"]["email"] == "ada@example.com"
    assert result["values"]["pack_number"] == "103"
    assert result["values"]["artwork_slug"] == "the-golden-boys"
    assert result["values"]["source_tag"] == "MACTGB003"
    assert result["values"]["position"] == ""
    assert result["values"]["town"] == ""
    assert result["values"]["country"] == ""
    assert result["values"]["phone_number"] == ""


def test_validate_pack_claim_rejects_blank_fields_and_a_bad_tag():
    assert validate_pack_claim({})["errors"]["name"] == "Enter your name."
    assert validate_pack_claim({})["errors"]["consent"] == "Confirm that we may store these details."
    assert validate_pack_claim({**CLAIM, "tagCode": "hello"})["errors"] == {
        "tagCode": "Enter a valid pack tag."
    }


def test_claimed_redirect_url_uses_artwork_or_conference_dashboard():
    assert claimed_redirect_url("MACTSOB014", "http://127.0.0.1:5173") == (
        "https://takemearound.gallery/the-star-of-bethlehem"
    )
    assert claimed_redirect_url("MACD103", "http://127.0.0.1:5173/") == (
        "http://127.0.0.1:5173/dashboard"
    )
    assert claimed_redirect_url("hello", "http://127.0.0.1:5173") is None
