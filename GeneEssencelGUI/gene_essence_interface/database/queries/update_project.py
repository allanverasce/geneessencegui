import sqlite3
import json

from gene_essence_interface.utils.get_database_connection import get_database_connection


def update_project(project_name, project_type, model_file, file_path_csv, selected_models, selected_metrics, status,
                   result_delivery_method, delivery_contact=None, model_directory_path=None, test_size=0.3,
                   model_parameters=None):
    """
    Update an existing project in the database.

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
                UPDATE project
                SET file_path_csv = ?,
                    model_file = ?,
                    selected_models = ?,
                    selected_metrics = ?,
                    status = ?,
                    result_delivery_method = ?,
                    delivery_contact = ?,
                    model_directory_path = ?,
                    test_size = ?,
                    model_parameters = ?
                WHERE project_name = ? AND project_type = ?
            ''', (
                file_path_csv, model_file, selected_models_str, selected_metrics_str, status, result_delivery_method,
                delivery_contact, model_directory_path, test_size, model_parameters_str, project_name, project_type
            ))

            if cursor.rowcount == 0:
                return "No project found with the given name and type."

            connection.commit()

        return "Project updated successfully."

    except sqlite3.Error as e:
        return f"An error occurred while updating the project: {e}"
    except Exception as e:
        return f"Unexpected error updating project: {e}"
