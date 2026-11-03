import re

from birmingham_registration.countries import COUNTRY_NAMES, DIAL_CODES

EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PHONE_DIGITS = re.compile(r"^[0-9]{4,15}$")
EXTENSION_DIGITS = re.compile(r"^[0-9]{1,10}$")
PACK_DIGITS = re.compile(r"^[0-9]{3}$")
PACK_RANGES = {
    "the-star-of-betlehem": ("001", "100", "Enter a pack number from 001 to 100."),
    "the-golden-boys": ("101", "200", "Enter a pack number from 101 to 200."),
}
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
ARTWORK_SLUGS = ("the-star-of-betlehem", "the-golden-boys")
STAR_ARTWORK_URL = "https://takemearound.gallery/the-star-of-bethlehem"
GOLDEN_ARTWORK_URL = "https://takemearound.museum/the-golden-boys"
TAG_PREFIX = re.compile(r"^(MACTSOB|MACTGB|MACD)(\d{1,6})$")
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


def canonical_pack_tag(value: object) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    trimmed = value.strip()
    if trimmed.startswith("{") or trimmed.startswith("["):
        return None
    compact = re.sub(r"[^A-Z0-9]", "", trimmed.upper())
    match = TAG_PREFIX.fullmatch(compact)
    if not match:
        return None
    serial = int(match.group(2))
    if serial < 1:
        return None
    padded = f"{serial:03d}" if serial < 1000 else str(serial)
    return f"{match.group(1)}{padded}"


def pack_claim_from_tag(value: object) -> dict | None:
    code = canonical_pack_tag(value)
    if code is None:
        return None
    if code.startswith("MACTSOB"):
        serial = int(code[7:])
        if serial < 1 or serial > 100:
            return None
        return {
            "tag_code": code,
            "pack_number": f"{serial:03d}",
            "artwork_slug": "the-star-of-betlehem",
            "kind": "artwork",
            "destination_url": STAR_ARTWORK_URL,
        }
    if code.startswith("MACTGB"):
        serial = int(code[6:])
        if serial < 1 or serial > 100:
            return None
        return {
            "tag_code": code,
            "pack_number": f"{serial + 100:03d}",
            "artwork_slug": "the-golden-boys",
            "kind": "artwork",
            "destination_url": GOLDEN_ARTWORK_URL,
        }
    if code.startswith("MACD"):
        serial = int(code[4:])
        if serial < 1 or serial > 200:
            return None
        star = serial <= 100
        return {
            "tag_code": code,
            "pack_number": f"{serial:03d}",
            "artwork_slug": "the-star-of-betlehem" if star else "the-golden-boys",
            "kind": "dashboard",
            "destination_url": "/dashboard",
        }
    return None


def claimed_redirect_url(source_tag: str, conference_public_url: str) -> str | None:
    claim = pack_claim_from_tag(source_tag)
    if claim is None:
        return None
    if claim["kind"] == "dashboard":
        return conference_public_url.rstrip("/") + "/dashboard"
    return claim["destination_url"]


def validate_pack_claim(payload: object) -> dict:
    data = payload if isinstance(payload, dict) else {}
    errors: dict[str, str] = {}
    values: dict[str, object] = {}
    claim = pack_claim_from_tag(data.get("tagCode"))
    if claim is None:
        errors["tagCode"] = "Enter a valid pack tag."
    else:
        values["source_tag"] = claim["tag_code"]
        values["pack_number"] = claim["pack_number"]
        values["artwork_slug"] = claim["artwork_slug"]
    for field in ("name", "surname", "email", "company"):
        raw = data.get(field, "")
        text = raw.strip() if isinstance(raw, str) else ""
        limit = LIMITS[field]
        if len(text) > limit:
            errors[field] = f"Use {limit} characters or fewer."
            continue
        if field == "email":
            if not EMAIL.match(text):
                errors[field] = BLANK[field]
            else:
                values[field] = text.lower()
            continue
        if not text:
            errors[field] = BLANK[field]
        else:
            values[field] = text
    if data.get("consent") is not True:
        errors["consent"] = "Confirm that we may store these details."
    else:
        values["consent"] = True
    values["position"] = ""
    values["town"] = ""
    values["country"] = ""
    values["phone_dial_code"] = ""
    values["phone_number"] = ""
    values["phone_extension"] = ""
    if errors:
        return {"ok": False, "errors": errors}
    return {"ok": True, "values": values}


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


def validate_registration(payload: object, *, email_required: bool = True) -> dict:
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
            if not text:
                if email_required:
                    errors[field] = BLANK[field]
                else:
                    values[field] = ""
            elif not EMAIL.match(text):
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
    raw_pack = data.get("packNumber", "")
    pack = raw_pack.strip() if isinstance(raw_pack, str) else ""
    if not PACK_DIGITS.match(pack):
        errors["packNumber"] = "Enter a 3-digit pack number."
    else:
        pack_range = PACK_RANGES.get(slug)
        if pack_range and (pack < pack_range[0] or pack > pack_range[1]):
            errors["packNumber"] = pack_range[2]
        else:
            values["pack_number"] = pack
    if data.get("consent") is not True:
        errors["consent"] = "Confirm that we may store these details."
    else:
        values["consent"] = True
    if errors:
        return {"ok": False, "errors": errors}
    return {"ok": True, "values": values}
