import joblib
from sklearn.model_selection import train_test_split

from gene_essence_engine.evaluate_model.evaluate_model import evaluate_model
from gene_essence_engine.graphics.plot_training_analysis import plot_training_analysis
from gene_essence_engine.normalize_data.normalize_data import normalize_data
from gene_essence_engine.train_classifiers.train_classifiers import train_classifiers
from gene_essence_engine.utils.create_csv import create_csv
from gene_essence_engine.utils.create_project_directory import create_project_directory
from gene_essence_engine.utils.predict_model import predict_model
from gene_essence_engine.utils.remove_directory import remove_directory
from gene_essence_engine.utils.remove_file import remove_file
from gene_essence_engine.utils.send_email import send_email
from gene_essence_engine.utils.write_progress import write_progress
from gene_essence_engine.utils.zip_directory import zip_directory


def training_analysis(project_name, models, metrics, data, test_size, parameters, result_delivery_method,
                      delivery_contact, log_callback):
    write_progress("Normalizing data...", 25, log_callback)
    x_normalized = normalize_data(data.iloc[:, :-1], log_callback)

    write_progress("Performing stratification of the data...", 30, log_callback)
    x_train, x_test, y_train, y_test = train_test_split(x_normalized, data.iloc[:, -1], test_size=test_size,
                                                        random_state=42)
    write_progress("Data stratified successfully.", 40, log_callback)

    write_progress("Starting model training...", 60, log_callback)
    trained_models = train_classifiers(x_train, y_train, models, parameters, log_callback)

    write_progress("Making predictions with the models...", 70, log_callback)
    predictions = predict_model(x_test, trained_models, log_callback)

    write_progress("Evaluating the models...", 80, log_callback)
    evaluation_results = {}
    for model_name, y_pred in predictions.items():
        evaluation_results[model_name] = evaluate_model(y_test, y_pred, metrics)

    write_progress("Saving the results...", 90, log_callback)
    project_directory = create_project_directory(result_delivery_method, delivery_contact, project_name, 'training')
    create_csv(predictions, f"{project_directory}/Prediction/{project_name}.csv")
    plot_training_analysis(evaluation_results, project_directory)

    for model_name, model in trained_models.items():
        model_path = f"{project_directory}/Models/{model_name}_model.pkl"
        joblib.dump(model, model_path)

    if result_delivery_method == 'email':
        output_zip = zip_directory(project_directory, log_callback)
        send_email(delivery_contact, output_zip, log_callback)
        remove_directory(project_directory)
        remove_file(output_zip)
    else:
        write_progress(f"Result saved in: '{project_directory}'.", callback=log_callback)
