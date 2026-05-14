from gene_essence_interface.utils.get_database_connection import get_database_connection


def get_metrics():
    """
    Get all available metrics from the database.

    Returns:
        list: List of dictionaries containing metric information
    """
    try:
        with get_database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name, description, url FROM metrics")

            metrics = []
            for row in cursor.fetchall():
                metrics.append({
                    "name": row[0],
                    "description": row[1],
                    "url": row[2]
                })

            return metrics
    except Exception as e:
        print(f"Error getting metrics: {e}")
        return []
