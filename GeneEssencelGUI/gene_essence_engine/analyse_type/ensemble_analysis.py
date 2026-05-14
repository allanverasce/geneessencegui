import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier

from gene_essence_engine.evaluate_model.evaluate_model import evaluate_model
from gene_essence_engine.graphics.plot_ensemble_analysis import plot_ensemble_analysis
from gene_essence_engine.normalize_data.normalize_data import normalize_data
from gene_essence_engine.utils.create_csv import create_csv
from gene_essence_engine.utils.create_project_directory import create_project_directory
from gene_essence_engine.utils.predict_model import predict_model
from gene_essence_engine.utils.remove_directory import remove_directory
from gene_essence_engine.utils.remove_file import remove_file
from gene_essence_engine.utils.send_email import send_email
from gene_essence_engine.utils.write_progress import write_progress
from gene_essence_engine.utils.zip_directory import zip_directory


def ensemble_analysis(project_name, metrics, data, model_info, test_size, result_delivery_method, delivery_contact, log_callback):
    write_progress("Normalizing data...", 25, log_callback)

    x_normalized = normalize_data(data.iloc[:, :-1], log_callback)

    write_progress("Stratifying data...", 30, log_callback)

    x_train, x_test, y_train, y_test = train_test_split(x_normalized, data.iloc[:, -1], test_size=test_size,
                                                        random_state=42)
    write_progress("Data stratified successfully.", callback=log_callback)

    write_progress("Starting model aggregation...", 50, log_callback)

    classifier = VotingClassifier(estimators=model_info, voting='hard')

    write_progress("Training the models...", 60, log_callback)

    classifier.fit(x_train, y_train)

    write_progress("Making predictions...", 70, log_callback)

    predictions = predict_model(x_test, {'Ensemble': classifier}, log_callback)

    write_progress("Evaluating the model...", 80, log_callback)

    evaluation_results = {}
    for model_name, y_pred in predictions.items():
        evaluation_results[model_name] = evaluate_model(y_test, y_pred, metrics)

    write_progress("Saving the results...", 90, log_callback)

    project_directory = create_project_directory(result_delivery_method, delivery_contact, project_name, 'ensemble')

    create_csv(predictions, f"{project_directory}/Prediction/{project_name}.csv")
    plot_ensemble_analysis(evaluation_results, project_directory)

    model_path = f"{project_directory}/Models/{project_name}.pkl"
    joblib.dump(classifier, model_path)

    if result_delivery_method == 'email':
        output_zip = zip_directory(project_directory, log_callback)
        send_email(delivery_contact, output_zip, log_callback)
        remove_directory(project_directory)
        remove_file(output_zip)

    else:
        write_progress(f"Result saved in: '{project_directory}'.", callback=log_callback)
