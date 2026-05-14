from gene_essence_interface.utils.get_database_connection import get_database_connection


def get_data_project(project_type, project_name):
    """
    Get all data for a specific project.

    Args:
        project_type: Type of project (Training, Prediction, or Ensemble)
        project_name: Name of the project

    Returns:
        dict: Dictionary with project data, or None if not found
    """
    try:
        with get_database_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                "SELECT * FROM project WHERE project_type = ? AND project_name = ?",
                (project_type, project_name)
            )

            columns = [description[0] for description in cursor.description]
            project = cursor.fetchone()

            if project:
                return dict(zip(columns, project))
            else:
                return None
    except Exception as e:
        print(f"Error getting project data: {e}")
        return None
