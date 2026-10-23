import csv
import io
import secrets
from functools import wraps

from flask import make_response, redirect, render_template, request, session, url_for

_CSV_FORMULA_PREFIXES = frozenset("=+-@\t\r")


def _csv_safe_cell(value) -> str:
    text = value if isinstance(value, str) else str(value)
    if text and text[0] in _CSV_FORMULA_PREFIXES:
        return f"'{text}"
    return text


def register_admin(application) -> None:
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
        return bool(expected) and secrets.compare_digest(sent, expected)

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
        if not secrets.compare_digest(password, settings.admin_password):
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

    @application.get("/admin")
    @require_admin
    def admin_home():
        return render_template(
            "admin_home.html",
            csrf_token=current_csrf(),
            artworks=store.list_artworks(),
            registrations=store.list_confirmed(),
        )

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
                "company",
                "position",
                "town",
                "country",
                "artwork",
                "confirmed_at",
            ]
        )
        for row in store.list_confirmed():
            writer.writerow(
                [
                    _csv_safe_cell(row["name"]),
                    _csv_safe_cell(row["surname"]),
                    _csv_safe_cell(row["email"]),
                    _csv_safe_cell(row["company"]),
                    _csv_safe_cell(row["position"]),
                    _csv_safe_cell(row["town"]),
                    _csv_safe_cell(row["country"]),
                    _csv_safe_cell(row["artwork_title"]),
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
                store.set_stock(slug, int(raw))
        return redirect(url_for("admin_home"))
