from task2_chunks import make_chunks
from lab6_search import Retriever, show_hits

texts = {
    "it": "A forgotten password can be reset using the recovery link.",
    "assessment": "Assignments are uploaded through the learning portal.",
}
records = make_chunks(texts, "sentence")
for backend in ["tfidf", "embedding"]:
    try:
        engine = Retriever(records, backend)
        print("Backend:", backend)
        show_hits(engine.search("How can I regain access to my account?", k=2))
    except Exception as exc:
        print(f"Backend {backend} skipped ({exc})")
