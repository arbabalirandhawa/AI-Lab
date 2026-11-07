# CS4944 / CA1601400 Artificial Intelligence Lab — Lab 6: NLP Fundamentals

**Student Name:** Rasikh Ali  
**Roll Number:** 42365  
**Lab Title:** NLP Fundamentals: Tokenization, Embeddings & Text Chunking (Tasks 1 & 2)

## 1. Environment Setup

Create and activate a Python virtual environment (Python 3.10+ recommended), then install the required packages:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

python -m pip install -r requirements.txt
```

## 2. File Organization

- `lab6_search.py` — Shared `Retriever` (`tfidf` and `embedding` backends) and `show_hits()` helper.
- `task1_tokens.py` — **Task 1 Main Script**: Compares whitespace splitting, Unicode word-like regex (`r"\b\w+\b"`), and `all-MiniLM-L6-v2` WordPiece subword tokens across 7 inputs (punctuation, contraction, email, CS4944 identifier, empty string, Urdu text, and mixed Urdu/code/punctuation), followed by the expanded 5-item FAQ chatbot evaluation and transcript.
- `task1_chatbot_check.py` — Automated assertions verifying exact canonical answers, empty query handling, unsupported query fallback, and non-exact paraphrase suggestions on the expanded FAQ dataset.
- `guided_chatbot.py` — Interactive CLI FAQ chatbot with 5 FAQs (3 base FAQs + 2 added FAQs with sources `fee_policy.txt` and `network_guide.txt`).
- `task2_chunks.py` — **Task 2 Main Script**: Implements `word_spans()`, `windows()`, `sentence_chunks()`, and `make_chunks()`; evaluates 40-word windows (`overlap=0` and `overlap=10`) vs. sentence-aware packing (`size=40`) on 3 synthetic university policy documents (150–250 words each); runs boundary assertions, abbreviation failure tests, and 3 paraphrased query retrieval comparisons.
- `task2_semantic_check.py` — Verification script comparing `tfidf` and `embedding` backends on sentence-chunked records.
- `scenario1_handbook.py` .. `scenario5_equipment.py` — Guided domain retrieval scenario scripts.
- `guided_tokens.py`, `guided_embeddings.py`, `guided_chunks.py`, `guided_limits.py`, `guided_metrics.py`, `guided_suggestions.py` — Guided lab exercises from Sections 6.1–6.7.
- `Lab6_Report.docx` — Complete Lab 6 report covering Tasks 1 and 2, comparison tables, transcripts, failure analysis, and reflection responses.

## 3. Running Tasks 1 and 2

```bash
# Run Task 1 (Tokenization comparison + FAQ Chatbot transcript & checks)
python task1_tokens.py
python task1_chatbot_check.py

# Run interactive FAQ Chatbot (TF-IDF or Embedding backend)
python guided_chatbot.py --backend tfidf
python guided_chatbot.py --backend embedding

# Run Task 2 (Boundary tests, 3-document chunking comparison, abbreviation test & paraphrased queries)
python task2_chunks.py
python task2_semantic_check.py

# Run Guided Exercises & Scenarios
python guided_tokens.py
python guided_chunks.py
python guided_metrics.py
python guided_suggestions.py
python scenario1_handbook.py
python scenario2_support.py
python scenario3_docs.py
python scenario4_workplace.py
python scenario5_equipment.py
```

## 4. Dataset & Attribution Notice

All handbook, IT security, and tuition fee policy passages in this repository are synthetic teaching datasets constructed specifically for CS4944 Lab 6 following the course lab manual specifications. No personal data, credentials, or confidential university records are included.
