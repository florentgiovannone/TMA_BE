import uuid
from contextlib import contextmanager
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor

SCHEMA = Path(__file__).with_name("schema.sql").read_text()


class _StockUnavailable(Exception):
    pass


class Store:
    def __init__(self, database_url: str, sslmode: str):
        self._database_url = database_url
        self._sslmode = sslmode

    def _connect(self):
        return psycopg2.connect(
            self._database_url,
            sslmode=self._sslmode,
            cursor_factory=RealDictCursor,
        )

    @contextmanager
    def _session(self):
        conn = self._connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def migrate(self) -> None:
        with self._session() as conn:
            with conn.cursor() as cur:
                for statement in SCHEMA.split(";"):
                    sql = statement.strip()
                    if sql:
                        cur.execute(sql)

    def reset_for_tests(self) -> None:
        with self._session() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM registrations")
                cur.execute("UPDATE artworks SET stock = 0")

    def list_artworks(self) -> list[dict]:
        with self._session() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT slug, title, stock FROM artworks ORDER BY title DESC")
                return list(cur.fetchall())

    def get_artwork(self, slug: str) -> dict | None:
        with self._session() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT slug, title, stock FROM artworks WHERE slug = %s",
                    (slug,),
                )
                return cur.fetchone()

    def set_stock(self, slug: str, stock: int) -> bool:
        if (
            not isinstance(stock, int)
            or isinstance(stock, bool)
            or stock < 0
            or stock > 2147483647
        ):
            return False
        with self._session() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE artworks SET stock = %s WHERE slug = %s",
                    (stock, slug),
                )
                return cur.rowcount == 1

    def purge_expired(self) -> None:
        with self._session() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM registrations
                    WHERE status = 'unconfirmed' AND expires_at <= now()
                    """
                )

    def expire_for_tests(self, registration_id: str) -> None:
        with self._session() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE registrations
                    SET expires_at = now() - interval '1 second'
                    WHERE id = %s
                    """,
                    (registration_id,),
                )

    def get_registration(self, registration_id: str) -> dict | None:
        with self._session() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM registrations WHERE id = %s", (registration_id,))
                return cur.fetchone()

    def find_pair(self, email: str, artwork_slug: str) -> dict | None:
        with self._session() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, status, token_hash, artwork_slug
                    FROM registrations
                    WHERE email = %s AND artwork_slug = %s
                    ORDER BY CASE status WHEN 'confirmed' THEN 0 ELSE 1 END
                    LIMIT 1
                    """,
                    (email, artwork_slug),
                )
                return cur.fetchone()

    def insert_unconfirmed(self, values: dict, token_hash: str) -> str:
        registration_id = str(uuid.uuid4())
        with self._session() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO registrations (
                      id, name, surname, email, company, position, town, country,
                      artwork_slug, status, consent_at, created_at, confirmed_at,
                      expires_at, token_hash
                    ) VALUES (
                      %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, 'unconfirmed', now(), now(), NULL,
                      now() + interval '5 minutes', %s
                    )
                    """,
                    (
                        registration_id,
                        values["name"],
                        values["surname"],
                        values["email"],
                        values["company"],
                        values["position"],
                        values["town"],
                        values["country"],
                        values["artwork_slug"],
                        token_hash,
                    ),
                )
        return registration_id

    def replace_unconfirmed(self, registration_id: str, values: dict, token_hash: str) -> bool:
        with self._session() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE registrations SET
                      name = %s,
                      surname = %s,
                      email = %s,
                      company = %s,
                      position = %s,
                      town = %s,
                      country = %s,
                      artwork_slug = %s,
                      consent_at = now(),
                      created_at = now(),
                      expires_at = now() + interval '5 minutes',
                      token_hash = %s
                    WHERE id = %s AND status = 'unconfirmed'
                    """,
                    (
                        values["name"],
                        values["surname"],
                        values["email"],
                        values["company"],
                        values["position"],
                        values["town"],
                        values["country"],
                        values["artwork_slug"],
                        token_hash,
                        registration_id,
                    ),
                )
                return cur.rowcount == 1

    def delete_registration(self, registration_id: str) -> None:
        with self._session() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM registrations WHERE id = %s", (registration_id,))

    def delete_confirmed(self, registration_id: str) -> bool:
        with self._session() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM registrations WHERE id = %s AND status = 'confirmed'",
                    (registration_id,),
                )
                return cur.rowcount == 1

    def list_confirmed(self) -> list[dict]:
        with self._session() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT r.id, r.name, r.surname, r.email, r.company, r.position,
                           r.town, r.country, a.title AS artwork_title, r.confirmed_at
                    FROM registrations r
                    JOIN artworks a ON a.slug = r.artwork_slug
                    WHERE r.status = 'confirmed'
                    ORDER BY r.confirmed_at DESC
                    """
                )
                return list(cur.fetchall())

    def confirm(self, token_hash: str) -> str:
        conn = self._connect()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, artwork_slug
                        FROM registrations
                        WHERE token_hash = %s
                          AND status = 'unconfirmed'
                          AND expires_at > now()
                        FOR UPDATE
                        """,
                        (token_hash,),
                    )
                    row = cur.fetchone()
                    if row is None:
                        return "invalid"
                    cur.execute(
                        """
                        UPDATE artworks
                        SET stock = stock - 1
                        WHERE slug = %s AND stock > 0
                        RETURNING stock
                        """,
                        (row["artwork_slug"],),
                    )
                    if cur.fetchone() is None:
                        raise _StockUnavailable()
                    cur.execute(
                        """
                        UPDATE registrations
                        SET status = 'confirmed',
                            confirmed_at = now(),
                            token_hash = NULL
                        WHERE id = %s
                        """,
                        (row["id"],),
                    )
            return "confirmed"
        except _StockUnavailable:
            return "unavailable"
        finally:
            conn.close()
