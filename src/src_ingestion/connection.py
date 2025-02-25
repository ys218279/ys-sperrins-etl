import os
from dotenv import load_dotenv
import pg8000.native


load_dotenv(override=True)


def connect_to_db():
    # credentials=retrieve()
    return pg8000.native.Connection(
        user=os.getenv("RDS_USER"), 
        password=os.getenv("RDS_PASSWORD"),
        database=os.getenv("RDS_DATABASE"),
        host=os.getenv("RDS_HOST")
    )


def close_db_connection(conn):
    conn.close()