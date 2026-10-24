from pathlib import Path

import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "ticket_classifier.joblib"
TICKETS_PATH = DATA_DIR / "support_tickets.csv"


def train_model():
    if not TICKETS_PATH.exists():
        raise FileNotFoundError(
            f"Support tickets dataset not found: {TICKETS_PATH}"
        )

    df = pd.read_csv(TICKETS_PATH)

    required_columns = {"ticket_text", "category"}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            "support_tickets.csv must contain ticket_text and category columns."
        )

    df = df.dropna(subset=["ticket_text", "category"])
    df["ticket_text"] = df["ticket_text"].astype(str)
    df["category"] = df["category"].astype(str)

    if df["category"].nunique() < 2:
        raise ValueError("At least two ticket categories are required.")

    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("classifier", LogisticRegression(max_iter=1000)),
    ])

    model.fit(df["ticket_text"], df["category"])

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
