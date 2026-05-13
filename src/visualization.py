from __future__ import annotations
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

USE_DB = os.environ.get("USE_DB", "")
PLOTS_PATH = os.environ.get(
    "PLOTS_PATH",
    str(Path(__file__).resolve().parents[1] / "reports" / "figures")
)

FIG_DIR = PLOTS_PATH
EXCLUDE = ["Unnamed: 0", "Показник"]
COLS_2020 = ["Прогноз_2020_сценарій_1", "Прогноз_2020_сценарій_2", "Прогноз_2020_сценарій_3"]
COLS_2021 = ["Прогноз_2021_сценарій_1", "Прогноз_2021_сценарій_2", "Прогноз_2021_сценарій_3"]

def load_data() -> pd.DataFrame:
    if USE_DB == "postgres":
        import psycopg2
        conn = psycopg2.connect(
            host=os.environ["POSTGRES_HOST"],
            port=int(os.environ.get("POSTGRES_PORT", 5432)),
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
        )
        df = pd.read_sql("SELECT * FROM macro", conn)
        conn.close()
        print(f"[load] OK, shape={df.shape}")
        return df
    else:
        raw = Path(__file__).resolve().parents[1] / "data" / "raw" / "macro_indicators.csv"
        return pd.read_csv(raw)


def _to_numeric_ua(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return series
    cleaned = (
        series.astype(str)
        .str.strip()
        .str.replace(r"[\u00a0\u2009\u202f\s]", "", regex=True)
        .str.replace(",", ".", regex=False)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if col not in ["Unnamed: 0", "Показник"]:
            out[col] = _to_numeric_ua(out[col])
    return out

def _save(filename: str) -> str:
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, filename)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f"[viz] saved -> {path}")
    return path


def plot_scenario_comparison(df: pd.DataFrame) -> str:
    df_prepared = prepare(df.copy())
    top5 = df_prepared.nlargest(5, "Прогноз_2020_сценарій_2")[["Показник"] + COLS_2020 + COLS_2021]
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
    c2020 = f"Прогноз_2020_сценарій_{scenario}"
    c2021 = f"Прогноз_2021_сценарій_{scenario}"
    ind = "Показник"
    pct = ((df[c2021] - df[c2020]) / df[c2020] * 100).round(2)
    labels = [p[:25] + "..." if len(p) > 25 else p for p in df[ind]]

    colors = ["#2ecc71" if v >= 0 else "#e74c3c" for v in pct]
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(labels, pct, color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title(f"Зміна показників 2020→2021 (сценарій {scenario}), %")
    ax.set_xlabel("% зміна")
    ax.tick_params(axis="y", labelsize=7)
    return _save("yoy_change.png")


if __name__ == "__main__":
    df = prepare(load_data())
    plot_scenario_comparison(df)
    plot_spread(df)
    plot_yoy(df)
    print(f"Всі графіки збережено у {PLOTS_PATH}")