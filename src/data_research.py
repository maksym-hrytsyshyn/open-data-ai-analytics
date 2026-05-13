from __future__ import annotations
import os
import json
import sys
import pandas as pd
from pathlib import Path

USE_DB = os.environ.get("USE_DB", "")
REPORTS_PATH = os.environ.get(
    "REPORTS_PATH",
    str(Path(__file__).resolve().parents[1] / "reports")
)

EXCLUDE = ["Unnamed: 0", "Показник"]
COLS_2020 = ["Прогноз_2020_сценарій_1", "Прогноз_2020_сценарій_2", "Прогноз_2020_сценарій_3"]
COLS_2021 = ["Прогноз_2021_сценарій_1", "Прогноз_2021_сценарій_2", "Прогноз_2021_сценарій_3"]
SCENARIO_COLS = COLS_2020 + COLS_2021

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
        .str.replace(r"[\u00a0\u2009\u202f\u2000-\u200b\s]", "", regex=True)
        .str.replace(",", ".", regex=False)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if col not in EXCLUDE:
            out[col] = _to_numeric_ua(out[col])
    return out


def basic_stats(df: pd.DataFrame) -> pd.DataFrame:
    return df[SCENARIO_COLS].describe().T


def scenario_spread(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame({"Показник": df["Показник"]})
    out["min_2020"] = df[COLS_2020].min(axis=1)
    out["max_2020"] = df[COLS_2020].max(axis=1)
    out["spread_2020"] = out["max_2020"] - out["min_2020"]
    out["min_2021"] = df[COLS_2021].min(axis=1)
    out["max_2021"] = df[COLS_2021].max(axis=1)
    out["spread_2021"] = out["max_2021"] - out["min_2021"]
    return out


def year_over_year(df: pd.DataFrame, scenario: int = 2) -> pd.DataFrame:
    c2020 = f"Прогноз_2020_сценарій_{scenario}"
    c2021 = f"Прогноз_2021_сценарій_{scenario}"
    ind = "Показник"
    out = df[[ind, c2020, c2021]].copy()
    out["abs_change"] = out[c2021] - out[c2020]
    out["pct_change_%"] = ((out[c2021] - out[c2020]) / out[c2020] * 100).round(2)
    out["abs_change"] = out["abs_change"].round(2)
    return out


def top_uncertain(df: pd.DataFrame, year: int = 2020, n: int = 5) -> pd.DataFrame:
    spread = scenario_spread(df)
    key = f"spread_{year}"
    return spread.nlargest(n, key)[["Показник", key]]


if __name__ == "__main__":
    df = prepare(load_data())

    print("=== ОПИСОВА СТАТИСТИКА ===")
    print(basic_stats(df).to_string())

    print("\n=== 2020 vs 2021 (сценарій 2 — базовий) ===")
    print(year_over_year(df, scenario=2).to_string(index=False))

    print("\n=== ТОП-5 НАЙБІЛЬШ НЕВИЗНАЧЕНИХ ПОКАЗНИКІВ (2020) ===")
    print(top_uncertain(df, year=2020).to_string(index=False))

    reports_dir = Path(REPORTS_PATH)
    reports_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "year_over_year": year_over_year(df).to_dict(orient="records"),
        "top_uncertain_2020": top_uncertain(df, year=2020).to_dict(orient="records"),
    }
    report_file = reports_dir / "research_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n[research] Звіт збережено: {report_file}")