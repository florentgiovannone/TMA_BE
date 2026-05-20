"""Flask API for fetching items from PostgreSQL."""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import re
import secrets

import psycopg2
from psycopg2 import sql
from psycopg2.sql import Literal as SqlLiteral
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DEFAULT_DASHBOARD_PASSWORD = "tma-dashboard"

CORS_ALLOW_HEADERS = [
    "Content-Type",
    "Authorization",
    "X-API-Key",
    "X-Dashboard-Password",
    "ngrok-skip-browser-warning",
]


def _cors_allowed_origins() -> list[str]:
    """Origins and patterns for Access-Control-Allow-Origin (flask-cors)."""
    origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "https://takemearound.museum",
        "https://takemearound.gallery",
        "https://www.takemearound.museum",
        "https://www.takemearound.gallery",
        # Netlify deploy previews and branch deploys
        r"https://.*\.netlify\.app",
    ]
    for extra in os.getenv("CORS_EXTRA_ORIGINS", "").split(","):
        extra = extra.strip()
        if extra:
            origins.append(extra)
    if os.getenv("ALLOW_NGROK_CORS", "").lower() in ("1", "true", "yes"):
        origins.extend(
            [
                r"https://.*\.ngrok-free\.app",
                r"https://.*\.ngrok-free\.dev",
                r"https://.*\.ngrok\.io",
            ]
        )
    return origins


def _origin_allowed(origin: str) -> bool:
    for pattern in _cors_allowed_origins():
        if ".*" in pattern:
            if re.fullmatch(pattern, origin):
                return True
        elif origin == pattern:
            return True
    return False


_cors = _cors_allowed_origins()
CORS(
    app,
    origins=_cors,
    methods=["GET", "OPTIONS"],
    allow_headers=CORS_ALLOW_HEADERS,
    expose_headers=[
        "X-DB-Error",
        "X-Poise-Limit",
        "X-Poise-Offset",
        "X-Poise-Returned",
    ],
    supports_credentials=False,
    max_age=86400,
)


def _apply_cors_headers(response):
    origin = request.headers.get("Origin")
    if not origin or not _origin_allowed(origin):
        return response
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Vary"] = "Origin"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = ", ".join(CORS_ALLOW_HEADERS)
    response.headers["Access-Control-Max-Age"] = "86400"
    response.headers["Access-Control-Expose-Headers"] = (
        "X-DB-Error, X-Poise-Limit, X-Poise-Offset, X-Poise-Returned"
    )
    return response


@app.before_request
def cors_preflight():
    if request.method != "OPTIONS":
        return None
    response = app.make_response("")
    response.status_code = 204
    return _apply_cors_headers(response)


@app.after_request
def ensure_cors_headers(response):
    return _apply_cors_headers(response)


def db_config():
    return {
        "host": os.getenv("PGHOST", "localhost"),
        "port": int(os.getenv("PGPORT", "55432")),
        "dbname": os.getenv("PGDATABASE", "aba_cards"),
        "user": os.getenv("PGUSER", "poise"),
        "password": os.getenv("PGPASSWORD", ""),
    }


def _dashboard_password() -> str:
    """Matches VITE_DASHBOARD_PASSWORD; override with DASHBOARD_PASSWORD in production."""
    v = (os.getenv("DASHBOARD_PASSWORD") or DEFAULT_DASHBOARD_PASSWORD).strip()
    return v or DEFAULT_DASHBOARD_PASSWORD


def _password_header_ok(expected: str) -> bool:
    given = request.headers.get("X-Dashboard-Password", "").strip()
    if not given:
        return False
    return secrets.compare_digest(given, expected)


def _fetch_poise_log_columns(cur) -> set[str]:
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = current_schema()
          AND table_name = 'poise_log'
        """
    )
    return {r[0] for r in cur.fetchall()}


def _first_value(row: dict, *keys: str):
    for k in keys:
        if k in row and row[k] is not None:
            return row[k]
    return None


def _normalize_poise_row(row: dict) -> dict:
    ts = _first_value(row, "dtm_timestamp", "timestamp", "created_at", "dtm_created")
    if ts is not None and hasattr(ts, "isoformat"):
        ts = ts.isoformat()
    elif ts is not None:
        ts = str(ts)

    tname = _first_value(row, "text_name", "txt_name", "str_name")
    if tname is not None and not isinstance(tname, str):
        tname = str(tname)

    iid = _first_value(row, "int_id", "id", "log_id")
    if iid is not None:
        try:
            iid = int(iid)
        except (TypeError, ValueError):
            pass

    mtype = _first_value(row, "txt_message_type", "str_message_type", "message_type")
    if mtype is not None:
        mtype = str(mtype)

    msg = _first_value(
        row,
        "txt_message",
        "str_message",
        "message",
        "txt_msg",
        "log_message",
    )
    if msg is not None and not isinstance(msg, str):
        msg = str(msg)

    return {
        "int_id": iid,
        "dtm_timestamp": ts,
        "txt_message_type": mtype,
        "txt_message": msg,
        "text_name": tname,
    }


def _poise_log_default_limit() -> int:
    return max(1, min(100_000, int(os.getenv("POISE_LOG_LIMIT", "25000"))))


def _poise_log_max_limit() -> int:
    return max(1, min(200_000, int(os.getenv("POISE_LOG_MAX_LIMIT", "100000"))))


def _parse_limit_offset() -> tuple[int, int]:
    """From query string: ?limit= & ?offset= with safe bounds."""
    default = _poise_log_default_limit()
    cap = _poise_log_max_limit()
    try:
        limit = int(request.args.get("limit", default))
    except (TypeError, ValueError):
        limit = default
    try:
        offset = int(request.args.get("offset", 0))
    except (TypeError, ValueError):
        offset = 0
    limit = max(1, min(cap, limit))
    offset = max(0, offset)
    return limit, offset


def query_poise_log_items(limit: int, offset: int):
    """Returns (list of row dicts, None) or (None, db_error_line)."""
    try:
        conn = psycopg2.connect(**db_config())
        meta_cur = conn.cursor()
        cols = _fetch_poise_log_columns(meta_cur)
        meta_cur.close()
        if not cols:
            conn.close()
            return None, "table poise_log not found in current_schema() or has no columns"

        order_col = next(
            (c for c in ("int_id", "id", "log_id") if c in cols),
            None,
        )
        if not order_col:
            conn.close()
            return None, "poise_log has no int_id/id/log_id column for ordering"

        query = sql.SQL(
            "SELECT * FROM poise_log ORDER BY {oc} DESC NULLS LAST LIMIT {lim} OFFSET {off}"
        ).format(
            oc=sql.Identifier(order_col),
            lim=SqlLiteral(limit),
            off=SqlLiteral(offset),
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except psycopg2.Error as exc:
        return None, str(exc).splitlines()[0][:250]

    data = [_normalize_poise_row(dict(r)) for r in rows]
    return data, None


def _items_response():
    """Build JSON response for poise_log rows (200, or 200 with empty list + X-DB-Error)."""
    limit, offset = _parse_limit_offset()
    data, err = query_poise_log_items(limit, offset)
    if err is not None:
        response = jsonify([])
        response.headers["X-DB-Error"] = err
        return response, 200
    response = jsonify(data)
    response.headers["X-Poise-Limit"] = str(limit)
    response.headers["X-Poise-Offset"] = str(offset)
    response.headers["X-Poise-Returned"] = str(len(data))
    return response


@app.get("/api/health")
def health():
    cfg = db_config()
    return jsonify(
        {
            "status": "ok",
            "db": {
                "host": cfg["host"],
                "port": cfg["port"],
                "dbname": cfg["dbname"],
                "user": cfg["user"],
            },
        }
    )


@app.get("/api/items")
def get_items():
    """Log data; requires X-Dashboard-Password (same as dashboard).

    Query: ?limit= (default POISE_LOG_LIMIT env, cap POISE_LOG_MAX_LIMIT) & ?offset=
    for paging (newest first). Example: ?limit=500&offset=500 for the next page.
    """
    expected = _dashboard_password()
    if not _password_header_ok(expected):
        return jsonify({"error": "unauthorized"}), 401
    return _items_response()


@app.get("/api/secure/items")
def get_items_secure():
    """Alias of /api/items for backwards compatibility."""
    return get_items()


if __name__ == "__main__":
    cfg = db_config()
    print(
        "Starting API with DB config "
        f"host={cfg['host']} port={cfg['port']} dbname={cfg['dbname']} user={cfg['user']}"
    )
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5050")), debug=True)
