import json

from gene_essence_interface.utils.get_database_connection import get_database_connection


def get_models():
    """
    Get all available models from the database.

    Returns:
        list: List of dictionaries containing model information
    """
    try:
        with get_database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name, description, parameters, url FROM models")

            models = []
            for row in cursor.fetchall():
                parameters = json.loads(row[2])
                models.append({
                    "name": row[0],
                    "description": row[1],
                    "parameters": parameters,
                    "url": row[3]
                })
            return models
    except Exception as e:
        print(f"Error getting models: {e}")
        return []
