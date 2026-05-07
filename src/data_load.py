from __future__ import annotations

from pathlib import Path
import sys
import requests
import pandas as pd

DATA_URL = (
    "https://data.gov.ua/dataset/175386f8-fbce-4352-8ec9-44fc8c436aa9/"
    "resource/6c67d91d-6455-472f-aeb1-f81fadd2cb37/download/"
    "nabir-16-2020-2021-roki_03-12-2018.csv"
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
DEFAULT_FILENAME = "macro_indicators.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def download(url: str = DATA_URL, filename: str = DEFAULT_FILENAME) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / filename

    print(f"[download] GET {url}")
    response = requests.get(url, headers=HEADERS, timeout=60)
    response.raise_for_status()

    path.write_bytes(response.content)
    print(f"[download] saved {len(response.content)} bytes -> {path}")
    return path


def load(path: Path) -> pd.DataFrame:
    encodings = ["utf-8", "utf-8-sig", "cp1251", "windows-1251"]
    separators = [",", ";", "\t"]

    last_error: Exception | None = None
    for enc in encodings:
        for sep in separators:
            try:
                df = pd.read_csv(path, encoding=enc, sep=sep)
                if df.shape[1] >= 2:
                    print(
                        f"[load] ok: encoding={enc}, sep='{sep}', "
                        f"shape={df.shape}"
                    )
                    return df
            except Exception as exc:
                last_error = exc
                continue

    raise RuntimeError(f"Не вдалося прочитати CSV: {last_error}")


if __name__ == "__main__":
    try:
        csv_path = download()
    except requests.HTTPError as exc:
        print(f"[error] HTTP {exc.response.status_code}: {exc}")
        print(
            "Якщо завантаження не спрацювало, скачай файл вручну з браузера "
            f"і поклади у {RAW_DIR / DEFAULT_FILENAME}"
        )
        sys.exit(1)

    df = load(csv_path)
    print("\n=== HEAD ===")
    print(df.head())
    print("\n=== COLUMNS ===")
    print(list(df.columns))
    print("\n=== DTYPES ===")
    print(df.dtypes)