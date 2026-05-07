from __future__ import annotations
import sys
import pandas as pd

sys.path.insert(0, "src")
from data_load import download, load

EXCLUDE = ["Unnamed: 0", "Показник"]
COLS_2020 = ["Прогноз 2020 сценарій 1", "Прогноз 2020 сценарій 2", "Прогноз 2020 сценарій 3"]
COLS_2021 = ["Прогноз 2021 сценарій 1", "Прогноз 2021 сценарій 2", "Прогноз 2021 сценарій 3"]
SCENARIO_COLS = COLS_2020 + COLS_2021


def _to_numeric_ua(series: pd.Series) -> pd.Series:
    if series.dtype != "object":
        return series
    return pd.to_numeric(
        series.astype(str)
        .str.replace("\u00a0", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False),
        errors="coerce",
    )


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
    c2020 = f"Прогноз 2020 сценарій {scenario}"
    c2021 = f"Прогноз 2021 сценарій {scenario}"
    out = df[["Показник", c2020, c2021]].copy()
    out["abs_change"] = out[c2021] - out[c2020]
    out["pct_change_%"] = ((out[c2021] - out[c2020]) / out[c2020] * 100).round(2)
    return out


def top_uncertain(df: pd.DataFrame, year: int = 2020, n: int = 5) -> pd.DataFrame:
    spread = scenario_spread(df)
    key = f"spread_{year}"
    return spread.nlargest(n, key)[["Показник", key]]


if __name__ == "__main__":
    path = download()
    df = prepare(load(path))

    print("=== ОПИСОВА СТАТИСТИКА ===")
    print(basic_stats(df).to_string())

    print("\n=== 2020 vs 2021 (сценарій 2 — базовий) ===")
    print(year_over_year(df, scenario=2).to_string(index=False))

    print("\n=== ТОП-5 НАЙБІЛЬШ НЕВИЗНАЧЕНИХ ПОКАЗНИКІВ (2020) ===")
    print(top_uncertain(df, year=2020).to_string(index=False))