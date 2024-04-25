
from os import _Environ, environ

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extensions import connection


def get_db_conn(config: _Environ) -> connection:
    """Returns a db connection."""

    return connect(
        user=config["DB_USER"],
        host=config["DB_HOST"],
        database=config["DB_NAME"]
    )


def is_username_taken(conn: connection, username: str) -> bool:
    """Checks whether the username is taken or not."""

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE username = (%s);", (username,))
        results = cur.fetchall()

        if results:
            return True
        return False


def is_email_taken(conn: connection, email: str) -> bool:
    """Checks whether the email is taken or not."""

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = (%s);", (email,))
        results = cur.fetchall()

        if results:
            return True
        return False


def get_hashpw(conn: connection, email: str) -> str:
    """Returns the hashed password from an email."""

    with conn.cursor() as cur:
        cur.execute("SELECT password FROM users WHERE email = (%s)", (email,))
        hashpw = cur.fetchone()[0]

        return hashpw


if __name__ == "__main__":

    load_dotenv()

    conn = get_db_conn(environ)

    print(is_email_taken(conn, "zandersnow144@gmail.com"))
