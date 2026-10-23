from datetime import timedelta

from flask import Flask, jsonify, make_response, render_template, request
from flask_cors import CORS

from birmingham_registration.service import open_confirmation, submit_registration

CONFIRM_MESSAGES = {
    "confirmed": "Your interest is registered.",
    "invalid": "This link is invalid or has expired.",
    "unavailable": "This artwork is no longer available.",
}


def create_app(settings, store, mailer, limiter) -> Flask:
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
        allow_headers=["Content-Type"],
    )
    application.extensions["settings"] = settings
    application.extensions["store"] = store
    application.extensions["mailer"] = mailer
    application.extensions["limiter"] = limiter

    @application.get("/api/health")
    def health():
        return jsonify({"ok": True})

    @application.get("/api/artworks")
    def artworks():
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

    return application
