import os

from gene_essence_interface.utils.get_database_connection import get_database_connection


def get_projects(project_type):
    """
    Get all projects of a specific type with valid CSV files.

    Args:
        project_type: Type of project (Training, Prediction, or Ensemble)

    Returns:
        list: List of project names with valid CSV files
    """
    try:
        with get_database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT project_name, file_path_csv
                FROM project
                WHERE project_type = ?
            """, (project_type,))
            projects = [row[0] for row in cursor.fetchall() if os.path.isfile(row[1])]
            return projects
    except Exception as e:
        print(f"Error getting projects: {e}")
        return []
