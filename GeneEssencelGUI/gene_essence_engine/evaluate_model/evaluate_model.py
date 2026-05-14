from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef, \
    cohen_kappa_score

from gene_essence_engine.utils.write_progress import write_progress


def evaluate_model(y_true, y_pred, metrics, log_callback=None):
    results = {}

    def calculate_and_log(metric_name, metric_function, *args, **kwargs):
        try:
            result = metric_function(*args, **kwargs)
            results[metric_name] = float(result)
        except Exception as e:
            write_progress(f"[ERROR] Error calculating the metric {metric_name}: {e}", callback=log_callback)

    if 'accuracy' in metrics:
        calculate_and_log('Accuracy', accuracy_score, y_true, y_pred)

    if 'precision' in metrics:
        calculate_and_log('Precision', precision_score, y_true, y_pred, average='macro')

    if 'recall' in metrics:
        calculate_and_log('Recall', recall_score, y_true, y_pred, average='macro')

    if 'f1 score' in metrics:
        calculate_and_log('F1 Score', f1_score, y_true, y_pred, average='macro')

    if 'matthews corrcoef' in metrics:
        calculate_and_log('Matthews Corrcoef', matthews_corrcoef, y_true, y_pred)

    if 'kappa' in metrics:
        calculate_and_log('Kappa', cohen_kappa_score, y_true, y_pred)

    return results
