import os
import json
from pathlib import Path
from flask import Flask, render_template, send_from_directory
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)

POSTGRES_HOST     = os.environ.get("POSTGRES_HOST", "postgres")
POSTGRES_PORT     = int(os.environ.get("POSTGRES_PORT", 5432))
POSTGRES_DB       = os.environ.get("POSTGRES_DB", "macro")
POSTGRES_USER     = os.environ.get("POSTGRES_USER", "macro_user")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "macro_pass")
PLOTS_PATH        = os.environ.get("PLOTS_PATH", "/app/plots")
REPORTS_PATH      = os.environ.get("REPORTS_PATH", "/app/reports")

_engine = create_engine(
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)


def load_table():
    try:
        df = pd.read_sql("SELECT * FROM macro", _engine)
        df.columns = [c.replace("_", " ") for c in df.columns]
        return {"columns": list(df.columns), "rows": df.values.tolist()}
    except Exception as e:
        print(f"[web] load_table error: {e}")
        return None


def load_json(filename):
    try:
        path = Path(REPORTS_PATH) / filename
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def get_plots():
    try:
        return [f for f in os.listdir(PLOTS_PATH) if f.endswith(".png")]
    except Exception:
        return []


@app.route("/")
def index():
    return render_template(
        "index.html",
        quality=load_json("quality_report.json"),
        table=load_table(),
        research=load_json("research_report.json"),
        plots=get_plots(),
    )


@app.route("/plots/<path:filename>")
def serve_plot(filename):
    return send_from_directory(PLOTS_PATH, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)