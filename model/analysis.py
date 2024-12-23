from typing import Tuple

import matplotlib.pyplot as plt
from pandas import DataFrame
from ydata_profiling import ProfileReport


def get_profiling(data: DataFrame) -> None:
    profile = ProfileReport(data, title="Profiling Report")
    profile.to_file("./data/base_data_report.html")


def plot_graph(data: DataFrame, thresholds: Tuple[float, float]) -> None:
    plt.hist(data['pred'], bins=30, edgecolor='black', alpha=0.7)

    threshold_low, threshold_high = thresholds
    plt.axvline(threshold_low, color='r', linestyle='dashed', linewidth=1)
    plt.axvline(threshold_high, color='r', linestyle='dashed', linewidth=1)

    plt.xlabel('Данные')
    plt.ylabel('Значения P(A)')
    plt.title('Распределение нашей псевдо-вероятности')

    plt.savefig('graph_proba.png')
