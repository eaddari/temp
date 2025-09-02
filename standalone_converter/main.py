from source.evaluation import EvaluatorClass
import matplotlib.pyplot as plt
import numpy as np

def plot_single_defendant(data: dict, model: str) -> None:
    judges = list(data[model].keys())
    metrics = list(data[model][judges[0]].keys())

    values = {metric: [data[model][judge][metric] for judge in judges] for metric in metrics}
    x = np.arange(len(judges))
    width = 0.2

    plt.figure(figsize=(10, 6))
    for i, metric in enumerate(metrics):
        bar = plt.bar(x + i*width, values[metric], width, label=metric.capitalize())
        for rect, val in zip(bar, values[metric]):
            plt.text(rect.get_x() + rect.get_width()/2, rect.get_height() + 0.02, f'{val:.2f}', ha='center', va='bottom', fontsize=9)

    plt.xticks(x + width*1.5, judges)
    plt.ylabel('Score')
    plt.title(f'Metric Scores for {model}')
    plt.ylim(0, 4.2)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_average_metrics_for_defendats(data: dict) -> None:
    models = list(data.keys())
    metrics = list(next(iter(data.values())).keys())
    x = np.arange(len(models))
    width = 0.2

    plt.figure(figsize=(10, 6))
    for i, metric in enumerate(metrics):
        values = [data[model][metric] for model in models]
        bar = plt.bar(x + i*width, values, width, label=metric.capitalize())
        for rect, val in zip(bar, values):
            plt.text(rect.get_x() + rect.get_width()/2, rect.get_height() + 0.02, f'{val:.2f}', ha='center', va='bottom', fontsize=9)

    plt.xticks(x + width*1.5, models)
    plt.ylabel('Score')
    plt.title('Average Metrics per Model')
    plt.ylim(0, 4)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    
    defendats = ["gpt-4.1-nano", "gpt-4.1", "gpt-4o", "gpt-4.1-mini"]
    judges = ["gpt-4.1", "grok-3", "Phi-4"]

    evclass = EvaluatorClass("standalone_converter/data/explained_code.parquet", defendats, judges)

    result = evclass.create_final_df()
    avg_final_df = evclass.average_metrics(result)

    plot_single_defendant(result, "gpt-4.1-nano")
    plot_average_metrics_for_defendats(avg_final_df)
    