from sklearn.preprocessing import StandardScaler

from gene_essence_engine.utils.write_progress import write_progress


def normalize_data(data, log_callback):
    try:
        scaler = StandardScaler()
        normalized_data = scaler.fit_transform(data)
        write_progress("Data normalized successfully'.\n", callback=log_callback)
        return normalized_data
    except Exception as e:
        if log_callback:
            log_callback(f"[ERROR] Failed to normalize data: {e}\n")
