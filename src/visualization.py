from __future__ import annotations
import sys
import os
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, "src")
from data_load import download, load
from data_quality_analysis import coerce_numeric_columns

FIG_DIR = "reports/figures"
EXCLUDE = ["Unnamed: 0", "Показник"]
COLS_2020 = ["Прогноз 2020 сценарій 1", "Прогноз 2020 сценарій 2", "Прогноз 2020 сценарій 3"]
COLS_2021 = ["Прогноз 2021 сценарій 1", "Прогноз 2021 сценарій 2", "Прогноз 2021 сценарій 3"]


def _save(filename: str) -> str:
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, filename)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f"[viz] saved -> {path}")
    return path


def plot_scenario_comparison(df: pd.DataFrame) -> str:
    top5 = df.nlargest(5, "Прогноз 2020 сценарій 2")[["Показник"] + COLS_2020 + COLS_2021]
    labels = [p[:30] + "..." if len(p) > 30 else p for p in top5["Показник"]]
    x = range(len(labels))
    width = 0.15

    fig, ax = plt.subplots(figsize=(12, 6))
    for i, col in enumerate(COLS_2020 + COLS_2021):
        ax.bar([xi + i * width for xi in x], top5[col], width=width, label=col)

    ax.set_xticks([xi + width * 2.5 for xi in x])
    ax.set_xticklabels(labels, rotation=15, ha="right", fontsize=8)
    ax.set_title("Порівняння сценаріїв: топ-5 показників")
    ax.set_ylabel("Значення")
    ax.legend(fontsize=7)
    return _save("scenario_comparison.png")


def plot_spread(df: pd.DataFrame) -> str:
    spread_2020 = df[COLS_2020].max(axis=1) - df[COLS_2020].min(axis=1)
    spread_2021 = df[COLS_2021].max(axis=1) - df[COLS_2021].min(axis=1)
    labels = [p[:25] + "..." if len(p) > 25 else p for p in df["Показник"]]

    fig, ax = plt.subplots(figsize=(10, 7))
    x = range(len(labels))
    ax.barh([xi + 0.2 for xi in x], spread_2020, height=0.4, label="2020")
    ax.barh([xi - 0.2 for xi in x], spread_2021, height=0.4, label="2021")
    ax.set_yticks(list(x))
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_title("Розкид між сценаріями по показниках")
    ax.set_xlabel("max - min")
    ax.legend()
    return _save("scenario_spread.png")


def plot_yoy(df: pd.DataFrame, scenario: int = 2) -> str:
    """Зміна показників 2020→2021 для базового сценарію."""
    c2020 = f"Прогноз 2020 сценарій {scenario}"
    c2021 = f"Прогноз 2021 сценарій {scenario}"
    pct = ((df[c2021] - df[c2020]) / df[c2020] * 100).round(2)
    labels = [p[:25] + "..." if len(p) > 25 else p for p in df["Показник"]]

    colors = ["#2ecc71" if v >= 0 else "#e74c3c" for v in pct]
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(labels, pct, color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title(f"Зміна показників 2020→2021 (сценарій {scenario}), %")
    ax.set_xlabel("% зміна")
    ax.tick_params(axis="y", labelsize=7)
    return _save("yoy_change.png")


if __name__ == "__main__":
    path = download()
    df = coerce_numeric_columns(load(path), exclude=EXCLUDE)

    plot_scenario_comparison(df)
    plot_spread(df)
    plot_yoy(df)
    print("Всі графіки збережено у reports/figures/")