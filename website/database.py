
from os import _Environ, environ

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor, RealDictRow


USER_PLANTS_QUERY = """
    SELECT DISTINCT ON (prices.plant_id) plants.*, prices.price AS cur_price
    FROM plants
    JOIN subscriptions AS sub ON sub.plant_id = plants.plant_id
    LEFT JOIN prices ON plants.plant_id = prices.plant_id
    WHERE sub.user_id = (%s)
    ORDER BY prices.plant_id, prices.updated_at DESC;
    """

"""SELECT plants.* FROM plants JOIN subscriptions AS sub ON sub.plant_id = plants.plant_id WHERE sub.user_id = (%s);"""


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


def insert_plant_data(db_conn: connection, plant_data: dict) -> None:
    """Inserts plant data into the database."""

    with db_conn.cursor() as cur:
        cur.execute(
            """INSERT INTO plants(plant_name, original_price, url, image_url, in_stock) VALUES (%s, %s, %s, %s, %s);""",
            (plant_data['plant_name'], plant_data['og_price'], plant_data['url'], plant_data['image_url'], plant_data['in_stock']))
        db_conn.commit()


def insert_subscription(db_conn: connection, plant_data: dict, user_id: int) -> None:
    """Inserts a subscription into the database."""

    with db_conn.cursor() as cur:
        cur.execute("""SELECT plant_id FROM plants WHERE plant_name = (%s);""",
                    (plant_data['plant_name'],))
        plant_id = cur.fetchone()[0]

        cur.execute(
            """INSERT INTO subscriptions(user_id, plant_id) VALUES (%s, %s);""", (user_id, plant_id))

        db_conn.commit()


def is_plant_in_db(db_conn: connection, plant_data: dict) -> bool:
    """Checks whether a plant is already in the database."""

    with db_conn.cursor() as cur:
        cur.execute("""SELECT * FROM plants WHERE plant_name = (%s);""",
                    (plant_data['plant_name'],))

        results = cur.fetchall()

        if results:
            return True
        return False


def get_user_plants(db_conn: connection, user_id: int) -> list[RealDictRow]:
    """Returns all the plant data for a given user."""

    with db_conn.cursor(cursor_factory=RealDictCursor) as cur:

        cur.execute(USER_PLANTS_QUERY, (user_id,))
        results = cur.fetchall()[::-1]

        return results


def is_user_subbed(db_conn: connection, user_id: int, plant_data: dict) -> bool:
    """Checks if the user is already subbed to the plant."""

    with db_conn.cursor() as cur:
        cur.execute(
            """SELECT sub_id from subscriptions WHERE user_id = (%s) AND plant_id = (SELECT plant_id FROM plants WHERE plant_name = (%s));""", (user_id, plant_data['plant_name']))
        res = cur.fetchall()
        if res:
            return True
        return False


def insert_price(db_conn: connection, plant_data: dict) -> None:
    """Inserts the current price of a plant into the database."""

    with db_conn.cursor() as cur:
        cur.execute("""SELECT plant_id FROM plants WHERE plant_name = %s;""",
                    (plant_data['plant_name'],))
        plant_id = int(cur.fetchone()[0])
        cur.execute("""INSERT INTO prices(price, plant_id) VALUES (%s, %s);""",
                    (plant_data['current_price'], plant_id))
        db_conn.commit()


def remove_sub(db_conn: connection, user_id: int, plant_id: int) -> None:
    """Removes a users subscription to a plant from the database."""

    with db_conn.cursor() as cur:
        cur.execute(
            """DELETE FROM subscriptions WHERE user_id = %s AND plant_id = %s;""", (user_id, plant_id))

        db_conn.commit()


if __name__ == "__main__":

    load_dotenv()

    conn = get_db_conn(environ)

    plant_data = {'plant_name': "Monstera ads Thai Constellation 6cm Pot", 'og_price': 12.68,
                  'url': 'test_url', 'image_url': 'test_image', 'in_stock': True}
    print(is_user_subbed(conn, 1, plant_data))
