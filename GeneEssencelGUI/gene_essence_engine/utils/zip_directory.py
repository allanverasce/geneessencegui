import os
import zipfile
from typing import Optional

from gene_essence_engine.utils.write_progress import write_progress


def zip_directory(source_folder: str, log_callback: Optional[callable] = None) -> Optional[str]:
    """
    Create a ZIP archive of a directory.

    Args:
        source_folder: Path to directory to zip
        log_callback: Optional callback function for logging

    Returns:
        Path to created ZIP file if successful, None otherwise
    """
    if not os.path.exists(source_folder):
        write_progress(f"[ERROR] Source folder not found: {source_folder}", callback=log_callback)
        return None

    if not os.path.isdir(source_folder):
        write_progress(f"[ERROR] Path is not a directory: {source_folder}", callback=log_callback)
        return None

    parent_directory = os.path.dirname(source_folder)
    folder_name = os.path.basename(source_folder.rstrip(os.sep))
    output_zip = os.path.join(parent_directory, f"{folder_name}.zip")

    try:
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, source_folder)
                    zipf.write(full_path, arcname)

        if os.path.exists(output_zip):
            write_progress(f"[INFO] ZIP created successfully: {output_zip}", callback=log_callback)
            return output_zip
        else:
            write_progress("[ERROR] ZIP file was not created", callback=log_callback)
            return None

    except PermissionError as e:
        write_progress(f"[ERROR] Permission denied creating ZIP: {e}", callback=log_callback)
        return None
    except OSError as e:
        write_progress(f"[ERROR] OS error creating ZIP: {e}", callback=log_callback)
        return None
    except zipfile.BadZipFile as e:
        write_progress(f"[ERROR] Bad ZIP file: {e}", callback=log_callback)
        return None
    except Exception as e:
        write_progress(f"[ERROR] Unexpected error creating ZIP: {e}", callback=log_callback)
        return None

