from __future__ import annotations
import os
import json
from pathlib import Path
import pandas as pd

USE_DB = os.environ.get("USE_DB", "")
REPORTS_PATH = os.environ.get(
    "REPORTS_PATH",
    str(Path(__file__).resolve().parents[1] / "reports")
)

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
        return df
    else:
        raw = Path(__file__).resolve().parents[1] / "data" / "raw" / "macro_indicators.csv"
        return pd.read_csv(raw)

def quality_report(df: pd.DataFrame) -> dict:
    return {
        "rows": int(len(df)),
        "cols": int(df.shape[1]),
        "missing_total": int(df.isna().sum().sum()),
        "missing_per_col": {c: int(v) for c, v in df.isna().sum().items()},
        "duplicates": int(df.duplicated().sum()),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "memory_kb": round(df.memory_usage(deep=True).sum() / 1024, 2),
    }


def to_numeric_ua(series: pd.Series) -> pd.Series:
    if series.dtype != "object":
        return series
    cleaned = (
        series.astype(str)
        .str.replace("\u00a0", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def coerce_numeric_columns(df: pd.DataFrame, exclude: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if col in exclude:
            continue
        out[col] = to_numeric_ua(out[col])
    return out


def print_report(df: pd.DataFrame) -> None:
    rep = quality_report(df)
    print("=== QUALITY REPORT ===")
    for k, v in rep.items():
        if isinstance(v, dict):
            print(f"{k}:")
            for kk, vv in v.items():
                print(f"  {kk}: {vv}")
        else:
            print(f"{k}: {v}")


if __name__ == "__main__":
    df = load_data()
    report = quality_report(df)
    print_report(df)

    reports_dir = Path(REPORTS_PATH)
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_file = reports_dir / "quality_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n[quality] Звіт збережено: {report_file}")