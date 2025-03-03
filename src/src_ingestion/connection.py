import os
from dotenv import load_dotenv
import pg8000.native

load_dotenv(override=True)

def connect_to_db():
    """Establish connection to totesys database
    
    Keyword arguments for getenv:
    - RDS_USER -- Database username
    - RDS_PASSWORD -- Database password
    - RDS_DATABASE -- Database name
    - RDS_HOST -- Database host
    
    Return:
    - pg8000.native.Connection (connection to totesys database)
    """
    return pg8000.native.Connection(
        user=os.getenv("RDS_USER"),
        password=os.getenv("RDS_PASSWORD"),
        database=os.getenv("RDS_DATABASE"),
        host=os.getenv("RDS_HOST")
    )
    
def close_db_connection(conn):
    """Close connection to totesys database
    
    Keyword arguements:
    - conn -- connection to totesys database"""
    conn.close()