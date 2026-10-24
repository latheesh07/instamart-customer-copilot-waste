from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = ROOT / "data" / "refund_policy.txt"


def load_policy():
    """Load the demo refund policy."""
    if not POLICY_PATH.exists():
        raise FileNotFoundError(
            f"Policy file not found: {POLICY_PATH}"
        )

    return POLICY_PATH.read_text(encoding="utf-8")


def search_policy(question, top_k=3):
    """Find policy sections relevant to the question."""
    text = load_policy()

    sections = [
        section.strip()
        for section in text.split("\n\n")
        if section.strip()
    ]

    if not sections:
        return []

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(sections + [question])

    similarities = cosine_similarity(
        matrix[-1],
        matrix[:-1]
    ).flatten()

    best_indices = similarities.argsort()[::-1][:top_k]

    return [
        sections[i]
        for i in best_indices
        if similarities[i] > 0
    ]
