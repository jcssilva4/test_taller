"""First-stage retriever service.

Scores documents in data/ against a query using TF-IDF + cosine similarity,
then filters results down to documents the given role is authorized to view.
Fully local (scikit-learn), no cloud services or external APIs.
"""

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_DIR = Path(__file__).parent / "data"


def _load_documents():
    """Read every .txt file under data/ and extract its Authorized Roles header."""
    documents = []
    for path in sorted(DATA_DIR.rglob("*.txt")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        authorized_roles = []
        for line in text.splitlines():
            if line.strip().startswith("Authorized Roles:"):
                roles_str = line.split("Authorized Roles:", 1)[1]
                authorized_roles = [r.strip() for r in roles_str.split(",") if r.strip()]
                break
        documents.append(
            {
                "path": path,
                "text": text,
                "authorized_roles": authorized_roles,
            }
        )
    return documents


def retrieve(user_query: str, user_role: str) -> list[dict]:
    """Rank documents by relevance to user_query, then re-rank by user_role access.

    1. Score every document against user_query using TF-IDF + cosine similarity.
    2. Filter out documents the user_role is not authorized to see.
    3. Return the remaining documents sorted by relevance score (descending).
    """
    documents = _load_documents()
    if not documents:
        return []

    corpus = [user_query] + [doc["text"] for doc in documents]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    query_vector = tfidf_matrix[0]
    doc_vectors = tfidf_matrix[1:]
    scores = cosine_similarity(query_vector, doc_vectors)[0]

    results = []
    for doc, score in zip(documents, scores):
        if user_role in doc["authorized_roles"]:
            results.append(
                {
                    "path": str(doc["path"].relative_to(DATA_DIR.parent)),
                    "score": float(score),
                    "authorized_roles": doc["authorized_roles"],
                }
            )

    results.sort(key=lambda r: r["score"], reverse=True)
    return results


def main():
    user_query = "What are the rules for data retention and deletion?"
    user_role = "legal"

    print(f"Query: {user_query!r}")
    print(f"Role:  {user_role!r}\n")
    for rank, result in enumerate(retrieve(user_query, user_role), start=1):
        print(f"{rank}. [{result['score']:.4f}] {result['path']}  (roles: {', '.join(result['authorized_roles'])})")


if __name__ == "__main__":
    main()
