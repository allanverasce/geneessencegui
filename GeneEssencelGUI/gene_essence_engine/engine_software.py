import warnings
import joblib
import pandas as pd

from gene_essence_engine.analyse_type.prediction_analysis import prediction_analysis
from gene_essence_engine.analyse_type.training_analysis import training_analysis
from gene_essence_engine.analyse_type.ensemble_analysis import ensemble_analysis
from gene_essence_engine.utils.load_models_from_path import load_models_from_path
from gene_essence_engine.utils.write_progress import write_progress

warnings.filterwarnings('ignore')


def engine_software(data, log_callback=None):
    project_name = data.get('project_name')
    analysis_type = data.get('analysis_type')

    try:
        csv_file = pd.read_csv(data.get('file_path_csv'), encoding='utf-8')
        write_progress(f"[INFO] CSV file '{data.get('file_path_csv')}' successfully loaded.\n", 15, log_callback)
    except FileNotFoundError:
        if log_callback:
            log_callback(f"[ERROR] CSV file not found: {data.get('file_path_csv')}", None)
        return
    except pd.errors.ParserError as e:
        if log_callback:
            log_callback(f"[ERROR] CSV parsing error: {e}", None)
        return
    except PermissionError:
        if log_callback:
            log_callback(f"[ERROR] Permission denied reading CSV file: {data.get('file_path_csv')}", None)
        return
    except Exception as e:
        if log_callback:
            log_callback(f"[ERROR] Error loading CSV file: {e}", None)
        return

    metrics = data.get('selected_metrics')
    result_delivery_method = data.get('result_delivery_method')
    delivery_contact = data.get('delivery_contact')
    test_size = data.get('test_size')

    try:
        if analysis_type == 'training':
            parameters = data.get('model_parameters')
            models = data.get('selected_models')
            write_progress(f"[INFO] Starting training analysis for project '{project_name}'.\n", 20, log_callback)
            training_analysis(project_name, models, metrics, csv_file, test_size, parameters, result_delivery_method,
                              delivery_contact, log_callback)

        elif analysis_type == 'prediction':
            model_file = data.get('model_file')
            if not model_file:
                if log_callback:
                    log_callback("[ERROR] No model file provided for prediction analysis.", None)
                return

            try:
                write_progress(f"[INFO] Loading the model {model_file}", 30, log_callback)
                model_ensemble = joblib.load(model_file)
                write_progress(f"[INFO] Loaded model {model_file}", 40, log_callback)
            except Exception as e:
                if log_callback:
                    log_callback(f"[ERROR] Error loading model: {e}", None)
                return
            prediction_analysis(project_name, csv_file, model_ensemble, result_delivery_method, delivery_contact,
                                log_callback)

        elif analysis_type == 'ensemble':
            model_info = load_models_from_path(data.get('model_directory_path'), log_callback)
            write_progress(f"[INFO] Starting ensemble analysis for project '{project_name}'.\n", 20, log_callback)
            ensemble_analysis(project_name, metrics, csv_file, model_info, test_size, result_delivery_method,
                              delivery_contact, log_callback)
        else:
            if log_callback:
                log_callback(f"[ERROR] Analysis type '{analysis_type}' not recognized.", None)

    except Exception as e:
        if log_callback:
            log_callback(f"[ERROR] Error during analysis execution: {e}", None)
