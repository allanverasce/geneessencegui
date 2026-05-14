import os
import joblib
from typing import List, Tuple, Any, Optional

from gene_essence_engine.utils.write_progress import write_progress


def load_models_from_path(models_path: str, log_callback: Optional[callable] = None) -> List[Tuple[str, Any]]:
    """
    Load machine learning models from .pkl files in a directory.

    Args:
        models_path: Path to directory containing .pkl model files
        log_callback: Optional callback function for logging

    Returns:
        List of tuples containing (model_name, model_object)
    """
    if not os.path.exists(models_path):
        write_progress(f"[ERROR] Model directory not found: {models_path}", callback=log_callback)
        return []

    if not os.path.isdir(models_path):
        write_progress(f"[ERROR] Path is not a directory: {models_path}", callback=log_callback)
        return []

    model_info = []

    try:
        files = os.listdir(models_path)
    except PermissionError:
        write_progress(f"[ERROR] Permission denied accessing: {models_path}", callback=log_callback)
        return []
    except OSError as e:
        write_progress(f"[ERROR] Cannot read directory: {e}", callback=log_callback)
        return []

    for model_filename in files:
        if model_filename.endswith('.pkl'):
            model_name = model_filename.split('.')[0]
            model_path = os.path.join(models_path, model_filename)

            try:
                model = joblib.load(model_path)
                model_info.append((model_name, model))
                write_progress(f"[INFO] Loaded model: {model_name}", callback=log_callback)
            except EOFError:
                write_progress(f"[ERROR] Corrupt model file: {model_filename}", callback=log_callback)
            except Exception as e:
                write_progress(f"[ERROR] Failed to load {model_filename}: {e}", callback=log_callback)

    if not model_info:
        write_progress("[WARNING] No valid models found in directory", callback=log_callback)

    return model_info
