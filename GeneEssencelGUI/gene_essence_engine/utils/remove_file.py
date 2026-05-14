import os
from typing import Optional

from gene_essence_engine.utils.write_progress import write_progress


def remove_file(file_path: str, log_callback: Optional[callable] = None) -> bool:
    """
    Remove a file from the filesystem.

    Args:
        file_path: Path to file to remove
        log_callback: Optional callback function for logging

    Returns:
        True if file was removed successfully or doesn't exist, False otherwise
    """
    if not os.path.exists(file_path):
        return True

    try:
        os.remove(file_path)
        return True
    except PermissionError:
        write_progress(f"[ERROR] Permission denied removing file: {file_path}", callback=log_callback)
        return False
    except OSError as e:
        write_progress(f"[ERROR] Cannot remove file: {e}", callback=log_callback)
        return False
    except Exception as e:
        write_progress(f"[ERROR] Unexpected error removing file: {e}", callback=log_callback)
        return False
