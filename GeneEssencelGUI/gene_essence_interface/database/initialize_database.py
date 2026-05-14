import os
import sqlite3

from gene_essence_interface.database.fixtures.metrics_data import metrics_data
from gene_essence_interface.database.fixtures.models_data import models_data
from gene_essence_interface.utils.get_executable_path import get_executable_path


def initialize_database():
    try:
        base_dir = get_executable_path()
        os.makedirs(base_dir, exist_ok=True)

        old_db_path = os.path.join(base_dir, "predict_model_gui.db")
        new_db_path = os.path.join(base_dir, "gene_essence_gui.db")

        if os.path.exists(old_db_path) and not os.path.exists(new_db_path):
            os.rename(old_db_path, new_db_path)
            print("[INFO] Database migrated from predict_model_gui.db to gene_essence_gui.db")

        db_path = new_db_path
        is_new_database = not os.path.exists(db_path)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        if is_new_database:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS project (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT NOT NULL,
                    project_type TEXT NOT NULL,
                    model_file TEXT,
                    file_path_csv TEXT NOT NULL,
                    selected_models TEXT NOT NULL,
                    selected_metrics TEXT NOT NULL,
                    status TEXT NOT NULL,
                    result_delivery_method TEXT NOT NULL,
                    delivery_contact TEXT,
                    model_directory_path TEXT,
                    test_size REAL DEFAULT 0.3,
                    model_parameters TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS models (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    parameters TEXT NOT NULL,
                    url TEXT NOT NULL  
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    url TEXT NOT NULL  
                )
            ''')

        cursor.execute('SELECT COUNT(*) FROM models')
        if cursor.fetchone()[0] == 0:
            models_data()

        cursor.execute('SELECT COUNT(*) FROM metrics')
        if cursor.fetchone()[0] == 0:
            metrics_data()

        connection.commit()
        cursor.close()
        connection.close()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
