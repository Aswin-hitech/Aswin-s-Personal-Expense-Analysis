import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config


def get_db_connection():
    """
    Creates and returns a PostgreSQL connection.
    """

    try:
        conn = psycopg2.connect(
            Config.DATABASE_URL,
            cursor_factory=RealDictCursor
        )

        return conn

    except Exception as e:
        print("Database Connection Error:", e)
        return None