import logging

import psycopg2

from birmingham_registration.tokens import hash_token, new_token
from birmingham_registration.validation import validate_registration

LOGGER = logging.getLogger("birmingham_registration")


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
            "message": "This email is already registered for that artwork.",
        }
    artwork = store.get_artwork(values["artwork_slug"])
    if artwork is None or artwork["stock"] <= 0:
        return 409, {
            "ok": False,
            "error": "unavailable",
            "message": "That artwork is no longer available.",
        }
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
        store.replace_unconfirmed(existing["id"], values, token_digest)
        LOGGER.info("registration replaced id=%s", existing["id"])
        return 201, {"ok": True}
    try:
        registration_id = store.insert_unconfirmed(values, token_digest)
    except psycopg2.errors.UniqueViolation:
        return 201, {"ok": True}
    try:
        mailer.send_confirmation(values["email"], artwork["title"], confirm_url)
    except Exception:
        store.delete_registration(registration_id)
        LOGGER.info("confirmation email failed id=%s", registration_id)
        return 502, {
            "ok": False,
            "error": "email_failed",
            "message": "We could not send the confirmation email. Nothing was saved.",
        }
    LOGGER.info("registration saved id=%s", registration_id)
    return 201, {"ok": True}


def open_confirmation(store, token: str) -> str:
    store.purge_expired()
    if not token:
        return "invalid"
    return store.confirm(hash_token(token))
