from gene_essence_interface.utils.get_database_connection import get_database_connection


def update_project_status(project_name, analysis_type, status):
    """
    Update the status of a project.

    Args:
        project_name: Name of the project
        analysis_type: Type of analysis
        status: New status value
    """
    try:
        with get_database_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE project
                SET status = ?, project_type = ?
                WHERE project_name = ?
            """, (status, analysis_type, project_name))
            connection.commit()
    except Exception as e:
        print(f"Error updating project status: {e}")
