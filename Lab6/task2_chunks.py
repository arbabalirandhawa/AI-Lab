import re
from lab6_search import Retriever, show_hits


def word_spans(text):
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]


def windows(text, size=40, overlap=10, offset=0):
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Require size > 0 and 0 <= overlap < size")
    spans = word_spans(text)
    result = []
    for i in range(0, len(spans), size - overlap):
        j = min(i + size, len(spans))
        result.append((offset + spans[i][0], offset + spans[j - 1][1]))
        if j == len(spans):
            break
    return result


def sentence_chunks(text, size=40):
    if size <= 0:
        raise ValueError("size must be positive")
    # Teaching splitter: punctuation followed by whitespace.
    cuts = (
        [0]
        + [m.end() for m in re.finditer(r"[.!?]\s+", text)]
        + [len(text)]
    )
    out, pending, count = [], None, 0
    for a, b in zip(cuts, cuts[1:]):
        segment = text[a:b]
        n = len(segment.split())
        if not n:
            continue
        if n > size:
            if pending is not None:
                out.append(pending)
            out.extend(windows(segment, size, 0, a))
            pending, count = None, 0
        elif pending is not None and count + n <= size:
            pending, count = (pending[0], b), count + n
        else:
            if pending is not None:
                out.append(pending)
            pending, count = (a, b), n
    if pending is not None:
        out.append(pending)
    return out


def make_chunks(docs, strategy):
    result = []
    for doc_id, text in docs.items():
        spans = (
            sentence_chunks(text)
            if strategy == "sentence"
            else windows(text, 40, int(strategy))
        )
        for i, (a, b) in enumerate(spans):
            result.append(
                dict(
                    id=f"{doc_id}:{i}",
                    doc=doc_id,
                    start=a,
                    end=b,
                    text=text[a:b],
                )
            )
    return result


# Three synthetic documents (150-250 words each), each containing:
# 1) A specific policy rule + exception clause (EVIDENCE_RULES)
# 2) A single long sentence (>40 words) that triggers the fallback window split
# 3) Abbreviation examples (Prof., Dr., v2.1) to test sentence-boundary failure cases
DOCS = {
    "handbook_late": (
        "All undergraduate coursework for CS4944 must be uploaded through the official learning portal before 11:59 PM on the published due date. "
        "Submissions sent by email or delivered on USB flash drives are automatically rejected by the department office. "
        "Late submission is normally penalized at ten percent per day, except students with documented illness who submit signed medical evidence before the deadline. "
        "When an enrolled student experiences an unexpected hospitalization or severe medical emergency during the semester, the course coordinator may grant a seven-day deferral provided that the hospital discharge summary, diagnostic reference number, and official clinical verification form are uploaded to the student affairs portal within forty-eight hours of recovery. "
        "Note that inquiries sent to Prof. Dr. Tariq Mahmood after the grading window closes cannot modify locked portal marks. "
        "Group project milestones require every team member to confirm their individual contribution statement online before grades are released. "
        "Students must keep personal backup copies of all source code, raw experiment logs, and laboratory reports until final semester transcripts are officially published by the university registrar."
    ),
    "it_security": (
        "University network accounts provide access to campus Wi-Fi, cloud storage, and virtual computing labs for all currently enrolled students. "
        "Users must choose strong passphrases and never share one-time recovery codes with anyone claiming to be technical support staff. "
        "Expired or locked accounts are deactivated automatically after three failed login attempts, unless the user completes self-service password recovery using a verified backup email link. "
        "If an undergraduate or faculty workstation exhibits suspicious outbound network traffic or unauthorized token requests on port 8443, the automated campus firewall immediately quarantines the device hardware address, revokes all active session tokens, and requires an in-person identity check at the Main IT Help Desk in Block C. "
        "Multi-factor authentication tokens must be refreshed every thirty days on untrusted personal laptops and mobile devices. "
        "System maintenance follows policy v2.1. "
        "Dr. Amina Khan in the cybersecurity unit reviews flagged audit logs weekly. "
        "Technical assistance is available Monday through Friday from 8:00 AM to 6:00 PM via help@example.com or by visiting room C-104 with a valid university student card."
    ),
    "fee_refund": (
        "Semester tuition fees and laboratory charges must be cleared through the designated bank portal. "
        "Students paying after the fifth day face an administrative surcharge. "
        "Tuition fee refunds are strictly unavailable after week two of the semester, except when a student withdraws completely due to certified medical incapacity or mandatory national service deployment. "
        "Whenever an approved refund application is processed by the central finance office, the reimbursement is credited exclusively to the original bank account used during fee deposit after deducting non-refundable admission processing charges, hostel security adjustments, and any outstanding library overdue fines recorded by the chief librarian. "
        "Merit scholarship recipients must maintain a minimum cumulative grade point average of 3.00 to retain their full tuition waiver for subsequent academic terms at the university. "
        "Questions regarding monthly installment plans, fee challan corrections, or corporate sponsorship letters should be directed to the student accounts section in the main administration building before the midterm examination week officially begins."
    ),
}

EVIDENCE_RULES = {
    "handbook_late": (
        "Late submission is normally penalized at ten percent per day, except students with documented illness who submit signed medical evidence before the deadline."
    ),
    "it_security": (
        "Expired or locked accounts are deactivated automatically after three failed login attempts, unless the user completes self-service password recovery using a verified backup email link."
    ),
    "fee_refund": (
        "Tuition fee refunds are strictly unavailable after week two of the semester, except when a student withdraws completely due to certified medical incapacity or mandatory national service deployment."
    ),
}

PARAPHRASED_QUERIES = [
    (
        "I was sick and missed the assignment due date; how do I avoid the daily grade penalty with a doctor note?",
        "handbook_late",
    ),
    (
        "My login got disabled after entering the wrong passphrase three times; how can I restore my account via email?",
        "it_security",
    ),
    (
        "Can I get my semester fee money back in week three if I withdraw for certified medical reasons?",
        "fee_refund",
    ),
]


def run_boundary_tests():
    print("=" * 72)
    print("TASK 2A: BOUNDARY & EDGE-CASE TESTS")
    print("=" * 72)
    # 1. Empty text
    assert windows("") == []
    assert sentence_chunks("") == []
    print("[PASS] Empty text returns [] for both windows() and sentence_chunks().")

    # 2. Document shorter than the 40-word budget
    assert windows("short text") == [(0, 10)]
    assert sentence_chunks("short text") == [(0, 10)]
    print("[PASS] Short document ('short text', 2 words) produces single span [(0, 10)].")

    # 3. Invalid overlap (overlap >= size or negative overlap)
    for bad_size, bad_overlap in [(2, 2), (2, 3), (5, -1), (0, 0)]:
        try:
            windows("a b c", bad_size, bad_overlap)
        except ValueError:
            pass
        else:
            raise AssertionError(
                f"Invalid overlap ({bad_size}, {bad_overlap}) was accepted"
            )
    print("[PASS] Invalid overlap/size parameters correctly raise ValueError.")

    # 4. Sentence longer than the 40-word budget (95-word sentence)
    long_sent = " ".join(["word"] * 95) + "."
    long_spans = sentence_chunks(long_sent, size=40)
    long_lengths = [len(long_sent[a:b].split()) for a, b in long_spans]
    assert all(w <= 40 for w in long_lengths)
    assert long_lengths == [40, 40, 15]
    print(
        f"[PASS] 95-word single sentence falls back to 3 windows with word lengths {long_lengths}."
    )

    # 5. Reference smoke test
    ref_docs = {"example": "Reset your password. Keep recovery codes private."}
    for strategy in ["0", "10", "sentence"]:
        for c in make_chunks(ref_docs, strategy):
            assert c["text"] == ref_docs[c["doc"]][c["start"] : c["end"]]


def run_corpus_chunking_comparison():
    print("\n" + "=" * 72)
    print("TASK 2B: CHUNKING COMPARISON ACROSS 3 SYNTHETIC DOCUMENTS (150-250 WORDS)")
    print("=" * 72)
    for doc_id, text in DOCS.items():
        n_words = len(text.split())
        assert 150 <= n_words <= 250, f"{doc_id} has {n_words} words"
        assert EVIDENCE_RULES[doc_id] in text
        print(f"Document '{doc_id}': {n_words} words, {len(text)} chars")

    print(
        "\nStrategy Summary Table (per document and total across corpus):"
    )
    header = f"{'Strategy':<10} | {'Doc ID':<14} | {'Chunks':>6} | {'Orig W':>6} | {'Emit W':>6} | {'Dup W':>5} | {'Min/Avg/Max W':<15} | {'Rule+Exc Survives?'}"
    print(header)
    print("-" * len(header))

    for strategy in ["0", "10", "sentence"]:
        all_chunks = make_chunks(DOCS, strategy)
        tot_orig, tot_emit, tot_dup, tot_surv = 0, 0, 0, 0
        for doc_id, text in DOCS.items():
            doc_chunks = [c for c in all_chunks if c["doc"] == doc_id]
            for c in doc_chunks:
                assert c["text"] == text[c["start"] : c["end"]]
                assert 0 <= c["start"] < c["end"] <= len(text)
                assert len(c["text"].split()) <= 40
            w_counts = [len(c["text"].split()) for c in doc_chunks]
            orig_w = len(text.split())
            emit_w = sum(w_counts)
            dup_w = emit_w - orig_w
            survives = any(
                EVIDENCE_RULES[doc_id] in c["text"] for c in doc_chunks
            )
            tot_orig += orig_w
            tot_emit += emit_w
            tot_dup += dup_w
            tot_surv += int(survives)
            stats_str = f"{min(w_counts):2d}/{emit_w/len(w_counts):4.1f}/{max(w_counts):2d}"
            print(
                f"{strategy:<10} | {doc_id:<14} | {len(doc_chunks):>6} | {orig_w:>6} | {emit_w:>6} | {dup_w:>5} | {stats_str:<15} | {str(survives)}"
            )
        print(
            f"{strategy:<10} | {'TOTAL':<14} | {len(all_chunks):>6} | {tot_orig:>6} | {tot_emit:>6} | {tot_dup:>5} | {'-':<15} | {tot_surv}/3 docs preserved"
        )
        print("-" * len(header))


def explain_sentence_splitting_failures():
    print("\n" + "=" * 72)
    print("TASK 2C: WHERE REGEX SENTENCE SPLITTING (r'[.!?]\\s+') FAILS")
    print("=" * 72)
    sample = (
        "Contact Prof. Dr. Tariq Mahmood or Dr. Amina Khan (e.g. via help@example.com) "
        "before 5 p.m. on Friday for policy v2.1. Late appeals are rejected."
    )
    cuts = (
        [0]
        + [m.end() for m in re.finditer(r"[.!?]\s+", sample)]
        + [len(sample)]
    )
    raw_segments = [sample[a:b] for a, b in zip(cuts, cuts[1:]) if sample[a:b]]
    print("Sample text with abbreviations:")
    print(" ", sample)
    print(f"Raw segments produced by r'[.!?]\\s+' ({len(raw_segments)} segments):")
    for idx, seg in enumerate(raw_segments, 1):
        print(f"  {idx}. {repr(seg)}")
    print(
        "\nExplanation: The regex r'[.!?]\\s+' treats any period followed by whitespace as a "
        "sentence boundary. As shown above, honorifics ('Prof.', 'Dr.'), Latin abbreviations "
        "('e.g.'), and time abbreviations ('p.m.') cause premature splits mid-sentence. "
        "If the 40-word packing budget fills up right at 'Prof.' or 'Dr.', the title is placed "
        "at the end of one chunk while the person's name and rule land in the next chunk."
    )


def run_paraphrase_retrieval_comparison():
    print("\n" + "=" * 72)
    print("TASK 2D: PARAPHRASED QUERY RETRIEVAL ACROSS CHUNKS (TF-IDF & EMBEDDING)")
    print("=" * 72)
    backends = ["tfidf"]
    try:
        import sentence_transformers  # noqa: F401
        backends.append("embedding")
    except ImportError:
        pass

    for backend in backends:
        print(f"\n>>> Backend: {backend.upper()} <<<")
        for strategy in ["0", "10", "sentence"]:
            chunks = make_chunks(DOCS, strategy)
            try:
                engine = Retriever(chunks, backend=backend)
            except Exception as exc:
                print(f"[Note] {backend} backend is unavailable: {exc}")
                print("Skipping this backend; the TF-IDF results above remain available.")
                break
            print(f"\n--- Strategy: {strategy} ({len(chunks)} total chunks) ---")
            for q_text, target_doc in PARAPHRASED_QUERIES:
                hits = engine.search(q_text, k=2)
                print(f"Query: {q_text}")
                for rank, (rec, score) in enumerate(hits, 1):
                    has_full_rule = EVIDENCE_RULES[target_doc] in rec["text"]
                    print(
                        f"  Rank {rank}: {rec['id']} [{rec['start']}:{rec['end']}] "
                        f"score={score:.3f} | full_rule_in_chunk={has_full_rule}"
                    )
                    print(f"    Evidence: {repr(rec['text'])}")

    if "embedding" not in backends:
        print(
            "\n[Note] sentence-transformers is not installed; install the requirements and "
            "download the model to run the optional embedding comparison."
        )


if __name__ == "__main__":
    run_boundary_tests()
    run_corpus_chunking_comparison()
    explain_sentence_splitting_failures()
    run_paraphrase_retrieval_comparison()
