"""Flask admin routes for login, listings, CSV export, and stock updates."""

import csv
import io
import secrets
from functools import wraps

import psycopg2
from flask import make_response, redirect, render_template, request, session, url_for

from birmingham_registration.countries import COUNTRIES
from birmingham_registration.service import PACK_TAKEN
from birmingham_registration.validation import validate_registration

_CSV_FORMULA_PREFIXES = frozenset("=+-@\t\r")


def _constant_time_str_equal(left: str, right: str) -> bool:
    return secrets.compare_digest(left.encode(), right.encode())


def _csv_safe_cell(value) -> str:
    text = value if isinstance(value, str) else str(value)
    if text and text[0] in _CSV_FORMULA_PREFIXES:
        return f"'{text}"
    return text


def _pack_label(row: dict) -> str:
    number = row.get("pack_number") or ""
    return f"MACD{number}" if number else ""


def _form_draft(form) -> dict:
    return {
        "name": form.get("name", ""),
        "surname": form.get("surname", ""),
        "email": form.get("email", ""),
        "company": form.get("company", ""),
        "position": form.get("position", ""),
        "town": form.get("town", ""),
        "country": form.get("country", ""),
        "phoneDialCode": form.get("phoneDialCode", ""),
        "phoneNumber": form.get("phoneNumber", ""),
        "phoneExtension": form.get("phoneExtension", ""),
        "artworkSlug": form.get("artworkSlug", ""),
        "packNumber": form.get("packNumber", ""),
        "consent": True,
    }


def _phone_label(row: dict) -> str:
    number = row.get("phone_number") or ""
    if not number:
        return ""
    label = f"{row.get('phone_dial_code') or ''} {number}".strip()
    extension = row.get("phone_extension") or ""
    if extension:
        label = f"{label} ext. {extension}"
    return label


def register_admin(application) -> None:
    """Register admin login, listing, CSV export, and stock routes."""
    settings = application.extensions["settings"]
    store = application.extensions["store"]
    limiter = application.extensions["limiter"]

    def current_csrf() -> str:
        token = session.get("csrf_token")
        if not token:
            token = secrets.token_urlsafe(32)
            session["csrf_token"] = token
        return token

    def csrf_ok() -> bool:
        expected = session.get("csrf_token", "")
        sent = request.form.get("csrf_token", "")
        return bool(expected) and _constant_time_str_equal(sent, expected)

    def require_admin(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if session.get("admin") is not True:
                return redirect(url_for("login"))
            return view(*args, **kwargs)

        return wrapped

    @application.get("/admin/login")
    def login():
        return render_template("admin_login.html", csrf_token=current_csrf(), error="")

    @application.post("/admin/login")
    def login_submit():
        ip = request.remote_addr or ""
        if not csrf_ok():
            return render_template(
                "admin_login.html",
                csrf_token=current_csrf(),
                error="The form expired. Try again.",
            ), 400
        if not limiter.allow_login(ip):
            return render_template(
                "admin_login.html",
                csrf_token=current_csrf(),
                error="Try again later.",
            ), 429
        password = request.form.get("password", "")
        if not _constant_time_str_equal(password, settings.admin_password):
            limiter.record_login_failure(ip)
            return render_template(
                "admin_login.html",
                csrf_token=current_csrf(),
                error="The password is incorrect.",
            ), 401
        limiter.record_login_success(ip)
        session.clear()
        session["admin"] = True
        session["csrf_token"] = secrets.token_urlsafe(32)
        session.permanent = True
        return redirect(url_for("admin_home"))

    @application.post("/admin/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    def admin_page(errors=None, draft=None, status=200):
        store.purge_expired()
        artworks = store.list_artworks()
        return render_template(
            "admin_home.html",
            csrf_token=current_csrf(),
            artworks=artworks,
            registrations=store.list_confirmed(),
            countries=COUNTRIES,
            admin_options={
                "countries": [name for _code, name, _dial in COUNTRIES],
                "artworks": [{"slug": row["slug"], "title": row["title"]} for row in artworks],
            },
            errors=errors or {},
            draft=draft or {},
        ), status

    def save_registration(registration_id: str | None = None):
        if not csrf_ok():
            return redirect(url_for("admin_home"))
        draft = _form_draft(request.form)
        checked = validate_registration(draft, email_required=False)
        if not checked["ok"]:
            return admin_page(checked["errors"], draft, 400)
        values = checked["values"]
        if values["email"]:
            existing = store.find_pair(values["email"], values["artwork_slug"])
            if (
                existing
                and existing["status"] == "confirmed"
                and str(existing["id"]) != str(registration_id or "")
            ):
                return admin_page({"email": "This email is already registered."}, draft, 409)
        holder = store.find_pack(values["pack_number"])
        if holder and str(holder["id"]) != str(registration_id or ""):
            return admin_page(PACK_TAKEN["errors"], draft, 409)
        if registration_id is None:
            artwork = store.get_artwork(values["artwork_slug"])
            if artwork is None or artwork["stock"] <= 0:
                return admin_page(
                    {"artworkSlug": "That artwork is no longer available."},
                    draft,
                    409,
                )
            try:
                created = store.insert_confirmed(values)
            except psycopg2.errors.UniqueViolation:
                return admin_page(PACK_TAKEN["errors"], draft, 409)
            if not created:
                return admin_page(
                    {"artworkSlug": "That artwork is no longer available."},
                    draft,
                    409,
                )
            return redirect(url_for("admin_home"))
        try:
            updated = store.update_confirmed(registration_id, values)
        except psycopg2.errors.UniqueViolation:
            return admin_page(PACK_TAKEN["errors"], draft, 409)
        if updated == "missing":
            return redirect(url_for("admin_home"))
        if updated == "unavailable":
            return admin_page(
                {"artworkSlug": "That artwork is no longer available."},
                draft,
                409,
            )
        return redirect(url_for("admin_home"))

    @application.get("/admin")
    @require_admin
    def admin_home():
        return admin_page()

    @application.post("/admin/registrations")
    @require_admin
    def create_registration():
        return save_registration()

    @application.post("/admin/registrations/<registration_id>")
    @require_admin
    def update_registration(registration_id: str):
        return save_registration(registration_id)

    @application.get("/admin/registrations.csv")
    @require_admin
    def registrations_csv():
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(
            [
                "name",
                "surname",
                "email",
                "phone",
                "company",
                "position",
                "town",
                "country",
                "artwork",
                "pack_number",
                "confirmed_at",
            ]
        )
        for row in store.list_confirmed():
            writer.writerow(
                [
                    _csv_safe_cell(row["name"]),
                    _csv_safe_cell(row["surname"]),
                    _csv_safe_cell(row["email"]),
                    _csv_safe_cell(_phone_label(row)),
                    _csv_safe_cell(row["company"]),
                    _csv_safe_cell(row["position"]),
                    _csv_safe_cell(row["town"]),
                    _csv_safe_cell(row["country"]),
                    _csv_safe_cell(row["artwork_title"]),
                    _csv_safe_cell(_pack_label(row)),
                    _csv_safe_cell(row["confirmed_at"].isoformat()),
                ]
            )
        response = make_response(buffer.getvalue())
        response.mimetype = "text/csv"
        response.headers["Content-Disposition"] = "attachment; filename=registrations.csv"
        return response

    @application.post("/admin/registrations/<registration_id>/delete")
    @require_admin
    def delete_registration(registration_id: str):
        if csrf_ok():
            store.delete_confirmed(registration_id)
        return redirect(url_for("admin_home"))

    @application.post("/admin/artworks/<slug>/stock")
    @require_admin
    def update_stock(slug: str):
        if csrf_ok():
            raw = request.form.get("stock", "")
            if raw and raw.isascii() and raw.isdigit():
                try:
                    store.set_stock(slug, int(raw))
                except ValueError:
                    pass
        return redirect(url_for("admin_home"))
