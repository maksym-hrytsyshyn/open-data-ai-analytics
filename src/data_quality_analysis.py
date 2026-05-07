from __future__ import annotations
import pandas as pd

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
    """Конвертує рядки типу '5 045,30' у float."""
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
    """Конвертує всі колонки крім exclude у числові."""
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
    import sys
    sys.path.insert(0, "src")
    from data_load import download, load

    path = download()
    df = load(path)
    print_report(df)

    print("\n=== ПІСЛЯ КОНВЕРТАЦІЇ ===")
    df_num = coerce_numeric_columns(df, exclude=["Unnamed: 0", "Показник"])
    print(df_num.dtypes)
    print(df_num.head())