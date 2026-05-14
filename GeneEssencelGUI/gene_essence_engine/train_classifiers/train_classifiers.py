from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from gene_essence_engine.utils.write_progress import write_progress


def train_classifiers(x_train, y_train, models, parameters, log_callback):
    trained_models = {}

    model_classes = {
        'Logistic Regression': LogisticRegression,
        'Linear Discriminant Analysis': LinearDiscriminantAnalysis,
        'Decision Tree': DecisionTreeClassifier,
        'KNN': KNeighborsClassifier,
        'Gaussian Naive Bayes': GaussianNB,
        'MLP Classifier': MLPClassifier,
        'Random Forest': RandomForestClassifier,
        'SVC': SVC,
    }

    for model_name in models:
        try:
            if model_name in model_classes:
                model_class = model_classes[model_name]
                params = parameters.get(model_name, {})
                model = model_class(**params)
                model.fit(x_train, y_train)
                trained_models[model_name] = model
                write_progress(f"[INFO] Training completed successfully for the model {model_name}", callback=log_callback)
            else:
                write_progress(f"[ERROR] Model {model_name} is not recognized and will be ignored.", callback=log_callback)
        except Exception as e:
            write_progress(f"[ERROR] Training failed for the model {model_name}: {e}", callback=log_callback)
    return trained_models
