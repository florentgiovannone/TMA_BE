import re

EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
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
    "country": "Enter the country.",
}
ARTWORK_SLUGS = ("the-star-of-bethlehem", "the-golden-boys")


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
        if not text:
            errors[field] = BLANK[field]
        else:
            values[field] = text
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
