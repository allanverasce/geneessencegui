import os
import psutil


def check_system_resources_for_model(model_file_path, safety_multiplier=3.0):
    """
    Check if the system has sufficient resources to load and run a model file.

    Args:
        model_file_path (str): Path to the .pkl model file
        safety_multiplier (float): Multiplier to estimate memory usage (default: 3.0)
                                   Models typically use 2-3x their file size when loaded

    Returns:
        tuple: (bool, str) - (is_sufficient, message)
               is_sufficient: True if resources are sufficient, False otherwise
               message: Detailed message explaining the resource status
    """
    try:
        if not os.path.exists(model_file_path):
            return False, "Model file not found."

        model_size_bytes = os.path.getsize(model_file_path)
        model_size_mb = model_size_bytes / (1024 * 1024)

        estimated_memory_required_mb = model_size_mb * safety_multiplier

        memory = psutil.virtual_memory()
        available_memory_mb = memory.available / (1024 * 1024)

        if available_memory_mb < estimated_memory_required_mb:
            return False, (
                f"Insufficient memory to load the model.\n\n"
                f"Model file size: {model_size_mb:.2f} MB\n"
                f"Estimated memory required: {estimated_memory_required_mb:.2f} MB\n"
                f"Available memory: {available_memory_mb:.2f} MB\n\n"
                f"Please close some applications to free up memory or use a smaller model."
            )

        disk = psutil.disk_usage(os.path.dirname(model_file_path))
        available_disk_mb = disk.free / (1024 * 1024)

        if available_disk_mb < 500:
            return False, (
                f"Insufficient disk space.\n\n"
                f"Available disk space: {available_disk_mb:.2f} MB\n"
                f"Recommended: at least 500 MB\n\n"
                f"Please free up some disk space before proceeding."
            )

        return True, (
            f"System resources are sufficient.\n\n"
            f"Model file size: {model_size_mb:.2f} MB\n"
            f"Available memory: {available_memory_mb:.2f} MB\n"
            f"Available disk space: {available_disk_mb:.2f} MB"
        )

    except Exception as e:
        return False, f"Error checking system resources: {str(e)}"