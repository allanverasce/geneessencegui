import shutil
import os
import time
from typing import Optional

from gene_essence_engine.utils.write_progress import write_progress


def remove_directory(directory_path: str, retries: int = 3, log_callback: Optional[callable] = None) -> bool:
    """
    Remove a directory and all its contents with retry logic.

    Args:
        directory_path: Path to directory to remove
        retries: Number of retry attempts for permission errors (default: 3)
        log_callback: Optional callback function for logging

    Returns:
        True if directory was removed successfully or doesn't exist, False otherwise
    """
    if not os.path.exists(directory_path):
        return True

    for attempt in range(retries):
        try:
            shutil.rmtree(directory_path)
            return not os.path.exists(directory_path)
        except PermissionError:
            if attempt < retries - 1:
                time.sleep(0.5)
                write_progress(f"[WARNING] Permission denied, retrying... (attempt {attempt + 1}/{retries})",
                             callback=log_callback)
            else:
                write_progress(f"[ERROR] Failed to remove directory after {retries} attempts: {directory_path}",
                             callback=log_callback)
                return False
        except OSError as e:
            write_progress(f"[ERROR] Cannot remove directory: {e}", callback=log_callback)
            return False
        except Exception as e:
            write_progress(f"[ERROR] Unexpected error removing directory: {e}", callback=log_callback)
            return False

    return False
