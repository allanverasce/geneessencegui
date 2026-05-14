import json
import sqlite3
from tkinter import messagebox

from gene_essence_interface.utils.get_database_connection import get_database_connection

models = [
    {
        "name": "Decision Tree",
        "description": "Decision Tree classifier.",
        "parameters": {
            "criterion": "gini",
            "splitter": "best",
            "max_depth": None,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "min_weight_fraction_leaf": 0.0,
            "max_features": None,
            "random_state": None,
            "max_leaf_nodes": None,
            "min_impurity_decrease": 0.0,
            "class_weight": None,
            "ccp_alpha": 0.0
        },
        "url": "https://scikit-learn.org/1.5/modules/tree.html"
    },
    {
        "name": "Gaussian Naive Bayes",
        "description": "Naive Bayes classifier assuming Gaussian distribution.",
        "parameters": {
            "priors": None,
            "var_smoothing": 1e-9
        },
        "url": "https://scikit-learn.org/1.5/modules/naive_bayes.html"
    },
    {
        "name": "KNN",
        "description": "K-Nearest Neighbors classifier.",
        "parameters": {
            "n_neighbors": 5,
            "weights": "uniform",
            "algorithm": "auto",
            "leaf_size": 30,
            "p": 2,
            "metric": "minkowski",
            "metric_params": None,
            "n_jobs": None
        },
        "url": "https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html"
    },
    {
        "name": "Linear Discriminant Analysis",
        "description": "Linear Discriminant Analysis classifier.",
        "parameters": {
            "solver": "svd",
            "shrinkage": None,
            "priors": None,
            "n_components": None,
            "store_covariance": False,
            "tol": 1e-4
        },
        "url": "https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.LinearDiscriminantAnalysis.html"
    },
    {
        "name": "Logistic Regression",
        "description": "Logistic Regression classifier.",
        "parameters": {
            "penalty": "l2",
            "dual": False,
            "tol": 1e-4,
            "C": 1.0,
            "fit_intercept": True,
            "intercept_scaling": 1,
            "class_weight": None,
            "random_state": None,
            "solver": "lbfgs",
            "max_iter": 100,
            "multi_class": "auto",
            "verbose": 0,
            "warm_start": False,
            "n_jobs": None,
            "l1_ratio": None
        },
        "url": "https://scikit-learn.org/1.5/modules/generated/sklearn.linear_model.LogisticRegression.html"
    },
    {
        "name": "MLP Classifier",
        "description": "Multi-layer Perceptron classifier.",
        "parameters": {
            "hidden_layer_sizes": [100],
            "activation": "relu",
            "solver": "adam",
            "alpha": 0.0001,
            "batch_size": "auto",
            "learning_rate": "constant",
            "learning_rate_init": 0.001,
            "power_t": 0.5,
            "max_iter": 200,
            "shuffle": True,
            "random_state": None,
            "tol": 1e-4,
            "verbose": False,
            "warm_start": False,
            "momentum": 0.9,
            "nesterovs_momentum": True,
            "early_stopping": False,
            "validation_fraction": 0.1,
            "beta_1": 0.9,
            "beta_2": 0.999,
            "epsilon": 1e-8,
            "n_iter_no_change": 10,
            "max_fun": 15000
        },
        "url": "https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html"
    },
    {
        "name": "Random Forest",
        "description": "Random Forest classifier with decision trees.",
        "parameters": {
            "n_estimators": 100,
            "criterion": "gini",
            "max_depth": None,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "min_weight_fraction_leaf": 0.0,
            "max_features": "sqrt",
            "max_leaf_nodes": None,
            "min_impurity_decrease": 0.0,
            "bootstrap": True,
            "oob_score": False,
            "n_jobs": None,
            "random_state": None,
            "verbose": 0,
            "warm_start": False,
            "class_weight": None,
            "ccp_alpha": 0.0,
            "max_samples": None
        },
        "url": "https://scikit-learn.org/1.5/modules/generated/sklearn.ensemble.RandomForestClassifier.html"
    },
    {
        "name": "SVC",
        "description": "C-Support Vector Classification.",
        "parameters": {
            "C": 1.0,
            "kernel": "rbf",
            "degree": 3,
            "gamma": "scale",
            "coef0": 0.0,
            "shrinking": True,
            "probability": False,
            "tol": 0.001,
            "cache_size": 200,
            "class_weight": None,
            "verbose": False,
            "max_iter": -1,
            "decision_function_shape": "ovr",
            "break_ties": False,
            "random_state": None
        },
        "url": "https://scikit-learn.org/dev/modules/generated/sklearn.svm.SVC.html"
    }
]


def models_data():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        for model in models:
            cursor.execute('''
            INSERT INTO models (name, description, parameters, url)
            VALUES (?, ?, ?, ?)
            ''', (model["name"], model["description"], json.dumps(model["parameters"]), model["url"]))

        connection.commit()

        connection.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
