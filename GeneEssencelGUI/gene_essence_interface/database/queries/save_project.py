import sqlite3
import json

from gene_essence_interface.utils.get_database_connection import get_database_connection


def save_project(project_name, project_type, model_file, file_path_csv, selected_models, selected_metrics, status,
                 result_delivery_method, delivery_contact=None, model_directory_path=None,
                 test_size=0.3, model_parameters=None):
    """
    Save a new project to the database.

    Returns:
        str: Success message or error message
    """
    try:
        selected_models_str = json.dumps(selected_models)
        selected_metrics_str = json.dumps(selected_metrics)
        model_parameters_str = json.dumps(model_parameters) if model_parameters else None

        with get_database_connection() as connection:
            cursor = connection.cursor()

            cursor.execute('''
                INSERT INTO project (
                    project_name, project_type, model_file, file_path_csv, selected_models, selected_metrics,
                    status, result_delivery_method, delivery_contact, model_directory_path,
                    test_size, model_parameters
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                project_name, project_type, model_file, file_path_csv, selected_models_str, selected_metrics_str,
                status, result_delivery_method, delivery_contact, model_directory_path,
                test_size, model_parameters_str
            ))

            connection.commit()

        return "Project saved successfully."

    except sqlite3.Error as e:
        return f"An error occurred while saving the project: {e}"
    except Exception as e:
        return f"Unexpected error saving project: {e}"
