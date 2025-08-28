import sqlite3
from typing import Optional
from src.data.schemas import create_tables

CONNECTION: Optional[sqlite3.Connection] = None


def get_database() -> sqlite3.Connection:
    """
    Returns a singleton SQLite connection with row access by column name.
    Ensures tables are created on first connection.
    """
    global CONNECTION
    if CONNECTION is None:
        CONNECTION = sqlite3.connect("data.db")
        CONNECTION.row_factory = sqlite3.Row
        create_tables(CONNECTION)
        return CONNECTION

    return CONNECTION
