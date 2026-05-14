import matplotlib
import matplotlib.pyplot as plt
matplotlib.get_cachedir()


def plot_ensemble_analysis(prediction_result, save_path):
    model_name = list(prediction_result.keys())[0]
    metrics = list(prediction_result[model_name].keys())

    values = [v * 100 for v in prediction_result[model_name].values()]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(metrics, values, color='skyblue')

    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, value + 0.5, f'{int(round(value))}%',
                 ha='center', va='bottom', fontsize=10)

    plt.title('Ensemble Analysis Results')
    plt.xlabel('Metrics')
    plt.ylabel('Values (%)')
    plt.ylim(min(values) - 5, 100)
    plt.xticks(rotation=45)
    plt.tight_layout()

    if save_path:
        plt.savefig(f"{save_path}/Graphics/ensemble_analysis_{model_name}.png", dpi=300)
