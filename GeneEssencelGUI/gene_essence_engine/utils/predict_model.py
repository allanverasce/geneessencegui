import sys

from gene_essence_engine.utils.write_progress import write_progress


def predict_model(x, trained_models, log_callback):
    predictions = {}

    for model_name, model in trained_models.items():
        try:
            predictions[model_name] = model.predict(x)
            write_progress(f"[INFO] Prediction completed successfully for the model {model_name}", callback=log_callback)
        except Exception as e:
            write_progress(f"[ERROR] Prediction failed for the model {model_name}: {e}", callback=log_callback)

    return predictions
