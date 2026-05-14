import os
import shutil
import tempfile
import atexit

_temp_directories = []


def _cleanup_temp_dirs():
    """Clean up all temporary directories registered for cleanup."""
    for temp_dir in _temp_directories:
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass


atexit.register(_cleanup_temp_dirs)


def create_project_directory(result_delivery_method, delivery_contact, project_name, type_analyse):
    """
    Create project directory structure for analysis results.

    Args:
        result_delivery_method: 'local' or 'email'
        delivery_contact: Path for local delivery or email address
        project_name: Name of the project
        type_analyse: Type of analysis ('training', 'prediction', or 'ensemble')

    Returns:
        Path to created project directory
    """
    if result_delivery_method == 'local':
        base_directory = os.path.join(delivery_contact, 'GeneEssenceGUI')
    else:
        base_directory = tempfile.mkdtemp(prefix="GeneEssenceGUI_")
        _temp_directories.append(base_directory)

    os.makedirs(base_directory, exist_ok=True)

    project_directory = os.path.join(base_directory, project_name)

    if os.path.exists(project_directory):
        shutil.rmtree(project_directory)

    os.makedirs(project_directory)

    subdirs = ['Prediction']
    if type_analyse in ['training', 'ensemble']:
        subdirs.extend(['Models', 'Graphics'])

    for subdir in subdirs:
        subdir_path = os.path.join(project_directory, subdir)
        os.makedirs(subdir_path, exist_ok=True)

    return project_directory
