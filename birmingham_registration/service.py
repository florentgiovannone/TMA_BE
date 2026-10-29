import logging

import psycopg2

from birmingham_registration.tokens import hash_token, new_token
from birmingham_registration.validation import validate_contact, validate_registration

LOGGER = logging.getLogger("birmingham_registration")

PACK_TAKEN = {
    "ok": False,
    "error": "pack_taken",
    "errors": {"packNumber": "This pack number is already registered."},
}


def _pack_unique_violation(exc: BaseException) -> bool:
    name = getattr(getattr(exc, "diag", None), "constraint_name", "") or ""
    return "pack_number" in name


def submit_registration(store, mailer, limiter, settings, payload, ip: str) -> tuple[int, dict]:
    store.purge_expired()
    email = ""
    if isinstance(payload, dict) and isinstance(payload.get("email"), str):
        email = payload["email"].strip().lower()
    if not limiter.allow_registration(email, ip):
        return 429, {
            "ok": False,
            "error": "too_many_requests",
            "message": "Please try again later.",
        }
    checked = validate_registration(payload)
    if not checked["ok"]:
        return 400, {"ok": False, "errors": checked["errors"]}
    values = checked["values"]
    existing = store.find_pair(values["email"], values["artwork_slug"])
    if existing and existing["status"] == "confirmed":
        return 409, {
            "ok": False,
            "error": "already_registered",
            "message": "This email is already registered.",
        }
    artwork = store.get_artwork(values["artwork_slug"])
    if artwork is None or artwork["stock"] <= 0:
        return 409, {
            "ok": False,
            "error": "unavailable",
            "message": "That artwork is no longer available.",
        }
    holder = store.find_pack(values["pack_number"])
    exclude_id = existing["id"] if existing and existing["status"] == "unconfirmed" else None
    if holder and holder["id"] != exclude_id:
        return 409, PACK_TAKEN
    token = new_token()
    confirm_url = f"{settings.public_base_url}/confirm?token={token}"
    token_digest = hash_token(token)
    if existing and existing["status"] == "unconfirmed":
        try:
            mailer.send_confirmation(values["email"], artwork["title"], confirm_url)
        except Exception:
            LOGGER.info("confirmation email failed id=%s", existing["id"])
            return 502, {
                "ok": False,
                "error": "email_failed",
                "message": "We could not send the confirmation email. Nothing was saved.",
            }
        try:
            replaced = store.replace_unconfirmed(existing["id"], values, token_digest)
        except psycopg2.errors.UniqueViolation as exc:
            if _pack_unique_violation(exc):
                return 409, PACK_TAKEN
            LOGGER.info("confirmation email failed id=%s", existing["id"])
            return 502, {
                "ok": False,
                "error": "email_failed",
                "message": "Please try again later.",
            }
        if not replaced:
            LOGGER.info("confirmation email failed id=%s", existing["id"])
            return 502, {
                "ok": False,
                "error": "email_failed",
                "message": "Please try again later.",
            }
        LOGGER.info("registration replaced id=%s", existing["id"])
        return 201, {"ok": True}
    try:
        registration_id = store.insert_unconfirmed(values, token_digest)
    except psycopg2.errors.UniqueViolation as exc:
        if _pack_unique_violation(exc):
            return 409, PACK_TAKEN
        return 409, {
            "ok": False,
            "error": "please_retry",
            "message": "Please try again later.",
        }
    try:
        mailer.send_confirmation(values["email"], artwork["title"], confirm_url)
    except Exception:
        try:
            store.delete_registration(registration_id)
        except Exception:
            pass
        LOGGER.info("confirmation email failed id=%s", registration_id)
        return 502, {
            "ok": False,
            "error": "email_failed",
            "message": "We could not send the confirmation email. Nothing was saved.",
        }
    LOGGER.info("registration saved id=%s", registration_id)
    return 201, {"ok": True}


def submit_contact(mailer, limiter, settings, payload, ip: str) -> tuple[int, dict]:
    email = ""
    if isinstance(payload, dict) and isinstance(payload.get("email"), str):
        email = payload["email"].strip().lower()
    if not limiter.allow_contact(email, ip):
        return 429, {
            "ok": False,
            "error": "too_many_requests",
            "message": "Please try again later.",
        }
    checked = validate_contact(payload)
    if not checked["ok"]:
        return 400, {"ok": False, "errors": checked["errors"]}
    values = checked["values"]
    try:
        mailer.send_contact_service_email(settings.contact_recipient_email, values)
        mailer.send_contact_thank_you(values["email"], values["name"])
    except Exception:
        LOGGER.info("contact email failed")
        return 502, {
            "ok": False,
            "error": "email_failed",
            "message": "We could not send your message. Please try again later.",
        }
    LOGGER.info("contact message sent")
    return 201, {"ok": True}


def _blank(value) -> str:
    return value if isinstance(value, str) else ""


def public_registration(row: dict) -> dict:
    return {
        "name": row["name"],
        "surname": row["surname"],
        "email": row["email"],
        "phoneDialCode": _blank(row.get("phone_dial_code")),
        "phoneNumber": _blank(row.get("phone_number")),
        "phoneExtension": _blank(row.get("phone_extension")),
        "company": row["company"],
        "position": row["position"],
        "town": row["town"],
        "country": row["country"],
        "artworkSlug": row["artwork_slug"],
        "artworkTitle": row["artwork_title"],
        "packNumber": row.get("pack_number") or "",
    }


def list_public_registrations(store, pack_number: str | None) -> dict:
    if pack_number is None:
        store.purge_expired()
        rows = store.list_confirmed()
    else:
        rows = store.list_confirmed(pack_number)
    return {"registrations": [public_registration(row) for row in rows]}


def open_confirmation(store, token: str) -> str:
    store.purge_expired()
    if not token:
        return "invalid"
    return store.confirm(hash_token(token))
