from gene_essence_engine.normalize_data.normalize_data import normalize_data
from gene_essence_engine.utils.create_csv import create_csv
from gene_essence_engine.utils.create_project_directory import create_project_directory
from gene_essence_engine.utils.predict_model import predict_model
from gene_essence_engine.utils.remove_directory import remove_directory
from gene_essence_engine.utils.remove_file import remove_file
from gene_essence_engine.utils.send_email import send_email
from gene_essence_engine.utils.write_progress import write_progress
from gene_essence_engine.utils.zip_directory import zip_directory


def prediction_analysis(project_name, data, model_ensemble, result_delivery_method, delivery_contact, log_callback):
    write_progress("Normalizing data...", 60, log_callback)
    x_normalized = normalize_data(data, log_callback)

    trained_models = {'Predict Model GUI': model_ensemble}

    write_progress("Making predictions...", 75, log_callback)
    predictions = predict_model(x_normalized, trained_models, log_callback)

    write_progress("Saving the results...", 90, log_callback)
    project_directory = create_project_directory(result_delivery_method, delivery_contact, project_name, 'prediction')
    create_csv(predictions, f"{project_directory}/Prediction/{project_name}.csv")

    if result_delivery_method == 'email':
        output_zip = zip_directory(project_directory, log_callback)
        send_email(delivery_contact, output_zip, log_callback)
        remove_directory(project_directory)
        remove_file(output_zip)
    else:
        write_progress(f"Result saved in: '{project_directory}'.", callback=log_callback)
