import sqlite3
from tkinter import messagebox

from gene_essence_interface.utils.get_database_connection import get_database_connection


def metrics_data():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        data = [
            ('Accuracy', 'Proportion of correct predictions to the total number of predictions.',
             'https://scikit-learn.org/dev/modules/generated/sklearn.metrics.accuracy_score.html'),
            ('F1 Score', 'Harmonic mean of precision and recall.',
             'https://scikit-learn.org/1.5/modules/generated/sklearn.metrics.f1_score.html#sklearn.metrics.f1_score'),
            ('Kappa', 'Cohen\'s kappa coefficient, a measure of agreement between classifiers.',
             'https://scikit-learn.org/1.5/modules/generated/sklearn.metrics.cohen_kappa_score.html#sklearn.metrics'
             '.cohen_kappa_score'),
            ('Matthews Corrcoef',
             'Matthews correlation coefficient, a measure of the quality of binary classification.',
             'https://scikit-learn.org/1.5/modules/generated/sklearn.metrics.matthews_corrcoef.html#sklearn.metrics'
             '.matthews_corrcoef'),
            ('Precision', 'The model\'s ability to correctly predict positive cases.',
             'https://scikit-learn.org/1.5/modules/generated/sklearn.metrics.precision_score.html#sklearn.metrics'
             '.precision_score'),
            ('Recall', 'The model\'s ability to correctly identify all positive cases.',
             'https://scikit-learn.org/1.5/modules/generated/sklearn.metrics.recall_score.html#sklearn.metrics'
             '.recall_score')
        ]

        cursor.executemany('''
            INSERT INTO metrics (name, description, url) VALUES (?, ?, ?)
        ''', data)

        connection.commit()
        connection.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
