import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
matplotlib.get_cachedir()

def plot_training_analysis(training_result, save_path):
    models = list(training_result.keys())
    metrics = list(training_result[models[0]].keys())

    data = {
        metric: [training_result[model][metric] * 100 for model in models]
        for metric in metrics
    }

    ind = np.arange(len(models))
    width = 0.12

    plt.figure(figsize=(14, 8))

    bars_by_metric = []

    for i, metric in enumerate(metrics):
        bars = plt.bar(ind + i * width, data[metric], width, label=metric)
        bars_by_metric.append(bars)

    for bars in bars_by_metric:
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f'{int(round(height))}%',
                     ha='center', va='bottom', fontsize=9)

    if len(models) == 1:
        plt.title(f'Training Analysis Results for {models[0]}')
        plt.xlabel('Model')
    else:
        plt.title('Training Analysis Results for Multiple Models')
        plt.xlabel('Models')

    plt.ylabel('Values (%)')
    plt.xticks(ind + width * (len(metrics) / 2), models, rotation=45)

    all_values = [value for values in data.values() for value in values]
    plt.ylim(min(all_values) - 2, 100)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.legend(loc='best')
    plt.tight_layout()

    if save_path:
        plt.savefig(f"{save_path}/Graphics/training_analysis.png", dpi=300)
