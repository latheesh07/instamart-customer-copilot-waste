from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = ROOT / "data" / "refund_policy.txt"


def search_policy(question, top_k=3):
    if not POLICY_PATH.exists():
        raise FileNotFoundError(
            f"Policy file not found: {POLICY_PATH}"
        )

    text = POLICY_PATH.read_text(encoding="utf-8")

    # Split the policy into useful sections
    sections = [
        section.strip()
        for section in text.split("\n\n")
        if section.strip()
    ]

    if not sections:
        return ["No policy content found."]

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
