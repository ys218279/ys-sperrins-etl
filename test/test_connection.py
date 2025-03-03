from src.src_ingestion.connection import connect_to_db, close_db_connection
import pytest
from pg8000.native import DatabaseError, InterfaceError, Error
from unittest.mock import patch, MagicMock
import os



def test_connect_to_db_successful():
    try:
        result = connect_to_db()
        close_db_connection(result)
        expected = True
    except:
        expected = False
    assert expected == True   
