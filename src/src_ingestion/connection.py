from secrets_manager import retrieval, entry
from pg8000.native import Connection
from utils import get_secrets_manager_client


def connect_to_db():
    client = get_secrets_manager_client()
    credentials = retrieval(client)

    if not credentials:
        entry(client)
        credentials = retrieval(client)

    return Connection(
        user=credentials['username'],
        password=credentials['password'],
        database=credentials['database'],
        host=credentials['host']
    )


def close_db_connection(conn):
    conn.close()
