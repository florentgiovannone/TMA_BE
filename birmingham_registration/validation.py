import re

from birmingham_registration.countries import COUNTRY_NAMES, DIAL_CODES

EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PHONE_DIGITS = re.compile(r"^[0-9]{4,15}$")
EXTENSION_DIGITS = re.compile(r"^[0-9]{1,10}$")
LIMITS = {
    "name": 100,
    "surname": 100,
    "email": 254,
    "company": 200,
    "position": 200,
    "town": 100,
    "country": 100,
}
BLANK = {
    "name": "Enter your name.",
    "surname": "Enter your surname.",
    "email": "Enter a valid email.",
    "company": "Enter your company.",
    "position": "Enter your position.",
    "town": "Enter the town.",
    "country": "Choose a country.",
}
ARTWORK_SLUGS = ("the-star-of-bethlehem", "the-golden-boys")
CONTACT_LIMITS = {
    "name": 100,
    "email": 254,
    "organisation": 200,
    "message": 2000,
}
CONTACT_BLANK = {
    "name": "Enter your name.",
    "email": "Enter a valid email.",
    "message": "Enter a message.",
}


def validate_contact(payload: object) -> dict:
    data = payload if isinstance(payload, dict) else {}
    errors: dict[str, str] = {}
    values: dict[str, str] = {}
    for field, limit in CONTACT_LIMITS.items():
        raw = data.get(field, "")
        text = raw.strip() if isinstance(raw, str) else ""
        if len(text) > limit:
            errors[field] = f"Use {limit} characters or fewer."
            continue
        if field == "email":
            if not EMAIL.match(text):
                errors[field] = CONTACT_BLANK[field]
            else:
                values[field] = text.lower()
            continue
        if field == "organisation":
            values[field] = text
            continue
        if not text:
            errors[field] = CONTACT_BLANK[field]
        else:
            values[field] = text
    if errors:
        return {"ok": False, "errors": errors}
    return {"ok": True, "values": values}


def validate_registration(payload: object) -> dict:
    data = payload if isinstance(payload, dict) else {}
    errors: dict[str, str] = {}
    values: dict[str, object] = {}
    for field, limit in LIMITS.items():
        raw = data.get(field, "")
        text = raw.strip() if isinstance(raw, str) else ""
        if len(text) > limit:
            errors[field] = f"Use {limit} characters or fewer."
            continue
        if field == "email":
            if not EMAIL.match(text):
                errors[field] = BLANK[field]
            else:
                values[field] = text.lower()
            continue
        if field == "country":
            if text not in COUNTRY_NAMES:
                errors[field] = BLANK[field]
            else:
                values[field] = text
            continue
        if not text:
            errors[field] = BLANK[field]
        else:
            values[field] = text
    dial = data.get("phoneDialCode", "")
    dial = dial.strip() if isinstance(dial, str) else ""
    raw_phone = data.get("phoneNumber", "")
    phone = raw_phone.strip() if isinstance(raw_phone, str) else ""
    digits = re.sub(r"[\s-]", "", phone)
    if not digits:
        values["phone_dial_code"] = ""
        values["phone_number"] = ""
    elif not PHONE_DIGITS.match(digits):
        errors["phoneNumber"] = "Enter a valid phone number."
    elif dial not in DIAL_CODES:
        errors["phoneDialCode"] = "Choose a country code."
    else:
        values["phone_dial_code"] = dial
        values["phone_number"] = digits
    raw_extension = data.get("phoneExtension", "")
    extension = raw_extension.strip() if isinstance(raw_extension, str) else ""
    if extension and not EXTENSION_DIGITS.match(extension):
        errors["phoneExtension"] = "Enter a valid extension."
    else:
        values["phone_extension"] = extension
    raw_slug = data.get("artworkSlug", "")
    slug = raw_slug.strip() if isinstance(raw_slug, str) else ""
    if slug not in ARTWORK_SLUGS:
        errors["artworkSlug"] = "Choose an artwork."
    else:
        values["artwork_slug"] = slug
    if data.get("consent") is not True:
        errors["consent"] = "Confirm that we may store these details."
    else:
        values["consent"] = True
    if errors:
        return {"ok": False, "errors": errors}
    return {"ok": True, "values": values}
