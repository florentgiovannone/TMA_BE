import uuid
from contextlib import contextmanager
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor

SCHEMA = Path(__file__).with_name("schema.sql").read_text()


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
        if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
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

    def replace_unconfirmed(self, registration_id: str, values: dict, token_hash: str) -> None:
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

    def delete_registration(self, registration_id: str) -> None:
        with self._session() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM registrations WHERE id = %s", (registration_id,))
