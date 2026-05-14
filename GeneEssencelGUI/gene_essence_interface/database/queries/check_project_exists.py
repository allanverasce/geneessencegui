from gene_essence_interface.utils.get_database_connection import get_database_connection


def check_project_exists(project_name):
    """
    Check if a project with the given name exists.

    Args:
        project_name: Name of the project to check

    Returns:
        bool: True if project exists, False otherwise
    """
    try:
        with get_database_connection() as connection:
            cursor = connection.cursor()

            query = "SELECT COUNT(*) FROM project WHERE project_name = ?"
            cursor.execute(query, (project_name,))

            result = cursor.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Error checking project existence: {e}")
        return False
