from src.src_ingestion.secrets_manager import retrieval, entry
import pg8000.native


def connect_to_db(client):
    credentials=retrieval(client)

    if credentials is None:
        entry(client)
        credentials = retrieval(client)

    return pg8000.native.Connection(
        user=credentials['username'],
        password=credentials['password'],
        database=credentials['database'],
        host=credentials['host']
    )


def close_db_connection(conn):
    conn.close()
