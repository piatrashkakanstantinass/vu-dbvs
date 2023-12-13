from contextlib import contextmanager
import psycopg2

CONNECTION_STRING = ""


@contextmanager
def get_cursor():
    try:
        connection = psycopg2.connect()
        with connection.cursor() as cursor:
            yield cursor
    finally:
        connection.close()
