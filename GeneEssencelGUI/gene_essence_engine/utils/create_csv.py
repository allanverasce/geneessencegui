import pandas as pd
from typing import Dict, Any, Optional

from gene_essence_engine.utils.write_progress import write_progress


def create_csv(data_dict: Dict[str, Any], filename: str, log_callback: Optional[callable] = None) -> bool:
    """
    Create a CSV file from a dictionary of data.

    Args:
        data_dict: Dictionary containing column names as keys and data as values
        filename: Output file path for the CSV file
        log_callback: Optional callback function for logging

    Returns:
        True if CSV was created successfully, False otherwise
    """
    try:
        df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data_dict.items()]))
        df.to_csv(filename, index=False, encoding='utf-8')
        return True
    except (IOError, OSError) as e:
        write_progress(f"[ERROR] Failed to write CSV file: {e}", callback=log_callback)
        return False
    except (ValueError, KeyError) as e:
        write_progress(f"[ERROR] Invalid data for CSV creation: {e}", callback=log_callback)
        return False
    except Exception as e:
        write_progress(f"[ERROR] Unexpected error creating CSV: {e}", callback=log_callback)
        return False