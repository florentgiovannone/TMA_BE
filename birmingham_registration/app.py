import logging
import re
import secrets
from datetime import timedelta

from flask import Flask, jsonify, make_response, render_template, request, send_from_directory
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from birmingham_registration.admin import register_admin
from birmingham_registration.redact import RedactTokenFilter
from birmingham_registration.service import (
    list_public_registrations,
    open_confirmation,
    submit_contact,
    submit_registration,
)

CONFIRM_MESSAGES = {
    "confirmed": "Your interest is registered.",
    "invalid": "This link is invalid or has expired.",
    "unavailable": "This artwork is no longer available.",
}

REGISTRATIONS_READ_HEADER = "X-Registrations-Key"
PACK_NUMBER = re.compile(r"^\d{3}$")


def _constant_time_str_equal(left: str, right: str) -> bool:
    left_bytes = left.encode()
    right_bytes = right.encode()
    if len(left_bytes) != len(right_bytes):
        secrets.compare_digest(right_bytes, right_bytes)
        return False
    return secrets.compare_digest(left_bytes, right_bytes)


def _attach_redact_filter(logger_name: str) -> None:
    logger = logging.getLogger(logger_name)
    if not any(isinstance(item, RedactTokenFilter) for item in logger.filters):
        logger.addFilter(RedactTokenFilter())


def create_app(settings, store, mailer, limiter) -> Flask:
    _attach_redact_filter("werkzeug")
    _attach_redact_filter("birmingham_registration")

    application = Flask(__name__)
    application.config.update(
        SECRET_KEY=settings.secret_key,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
        SESSION_COOKIE_SECURE=settings.secure_cookies,
        PERMANENT_SESSION_LIFETIME=timedelta(hours=12),
    )
    CORS(
        application,
        resources={r"/api/*": {"origins": settings.cors_origins}},
        allow_headers=["Content-Type", "ngrok-skip-browser-warning"],
    )
    application.extensions["settings"] = settings
    application.extensions["store"] = store
    application.extensions["mailer"] = mailer
    application.extensions["limiter"] = limiter

    @application.get("/favicon.ico")
    def favicon():
        static_folder = application.static_folder
        if static_folder is None:
            raise RuntimeError("static folder is not configured")
        return send_from_directory(static_folder, "favicon.png", mimetype="image/png")

    @application.get("/api/health")
    def health():
        return jsonify({"ok": True})

    @application.get("/api/artworks")
    def artworks():
        store.purge_expired()
        return jsonify(
            {
                "privacyContact": settings.privacy_contact_email,
                "artworks": [
                    {
                        "slug": row["slug"],
                        "title": row["title"],
                        "stock": row["stock"],
                        "available": row["stock"] > 0,
                    }
                    for row in store.list_artworks()
                ],
            }
        )

    @application.post("/api/contact")
    def contact():
        status, body = submit_contact(
            mailer,
            limiter,
            settings,
            request.get_json(silent=True),
            request.remote_addr or "",
        )
        return jsonify(body), status

    @application.get("/api/registrations")
    def list_registrations():
        sent = request.headers.get(REGISTRATIONS_READ_HEADER, "")
        pack_number = request.args.get("packNumber")
        authorized = _constant_time_str_equal(sent, settings.registrations_read_key)
        if not authorized:
            if not isinstance(pack_number, str) or PACK_NUMBER.fullmatch(pack_number) is None:
                return jsonify({"ok": False, "error": "unauthorized"}), 401
        return jsonify(list_public_registrations(store, pack_number))

    @application.post("/api/registrations")
    def registrations():
        status, body = submit_registration(
            store,
            mailer,
            limiter,
            settings,
            request.get_json(silent=True),
            request.remote_addr or "",
        )
        return jsonify(body), status

    @application.get("/confirm")
    def confirm():
        result = open_confirmation(store, request.args.get("token", ""))
        response = make_response(render_template("confirm.html", message=CONFIRM_MESSAGES[result]))
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    register_admin(application)

    if settings.trusted_proxy_hops > 0:
        hops = settings.trusted_proxy_hops
        application.wsgi_app = ProxyFix(
            application.wsgi_app,
            x_for=hops,
            x_proto=hops,
        )

    return application
