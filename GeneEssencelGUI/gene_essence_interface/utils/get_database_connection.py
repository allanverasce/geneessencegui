import os
import sqlite3

from gene_essence_interface.utils.get_executable_path import get_executable_path


def get_database_connection():
    base_dir = get_executable_path()
    db_path = os.path.join(base_dir, "gene_essence_gui.db")

    connection = sqlite3.connect(db_path, timeout=10.0)
    # Enable WAL mode for better concurrent access
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA busy_timeout=5000")
    return connection
