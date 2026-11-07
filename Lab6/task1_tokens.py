import re
from guided_chatbot import FAQ, build_bot, reply


def run_token_comparison():
    print("=" * 72)
    print("TASK 1A: TOKENIZATION & CONSERVATIVE NORMALIZATION COMPARISON")
    print("=" * 72)
    samples = [
        ("Punctuation", "AI, search!"),
        ("Contraction", "I can't log in."),
        ("Email", "help@example.com"),
        ("Identifier", "CS4944 version 2.1"),
        ("Empty string", ""),
        ("Urdu text", "یہ ایک مثال ہے"),
        ("Urdu + Code + Punct", "کیا میں CS4944 کی اسائنمنٹ جمع کروا سکتا ہوں؟"),
    ]

    for label, text in samples:
        ws = text.split()
        words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
        print(f"\n[{label}]")
        print("  Original  :", repr(text))
        print(f"  Whitespace ({len(ws):2d}):", ws)
        print(f"  Word-like  ({len(words):2d}):", words)

    assert re.findall(r"\b\w+\b", "") == []

    print("\n" + "-" * 72)
    print("Model Subword Tokenizer (sentence-transformers/all-MiniLM-L6-v2)")
    print("-" * 72)
    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2", device="cpu"
        )
        for label, text in samples:
            subwords = model.tokenizer.tokenize(text)
            token_ids = model.tokenizer(text, truncation=False)["input_ids"]
            print(
                f"  {label:12s} | {repr(text):22s} -> subwords ({len(subwords)}): {subwords} | ids w/ specials ({len(token_ids)})"
            )
    except Exception as exc:
        print("  [Note] Model tokenizer was not run:", exc)
        print(
            "  Install the requirements and allow all-MiniLM-L6-v2 to download "
            "once to print subword tokens for all seven inputs."
        )

    print("\n" + "-" * 72)
    print("Analysis: Two Key Differences & One Normalization Risk")
    print("-" * 72)
    print(
        "1. Attached vs. Stripped vs. Isolated Punctuation: Whitespace splitting keeps "
        "trailing punctuation glued to tokens ('AI,', 'search!', 'in.'), so 'late' and 'late!' "
        "fail to match. The regex r'\\b\\w+\\b' strips punctuation completely, whereas "
        "the model WordPiece tokenizer isolates punctuation (',', '!', '.') as standalone tokens."
    )
    print(
        "2. Contractions, Emails, and Identifiers: Whitespace keeps \"can't\", "
        "'help@example.com', and '2.1' intact as single units. The word-like regex splits "
        "on every non-alphanumeric character, fracturing \"can't\" -> ['can', 't'], "
        "'help@example.com' -> ['help', 'example', 'com'], and '2.1' -> ['2', '1']. "
        "Meanwhile, WordPiece splits unseen course codes like 'CS4944' into subwords ['cs', '##49', '##44']."
    )
    print(
        "3. Normalization Risk & Multilingual Caveat: Aggressive regex stripping or blind "
        "lowercasing destroys version decimals ('2.1'), email structure ('@'), API paths, and "
        "negation in contractions (\"can't\" -> 'can' + 't', where stopword filtering can drop 't' "
        "and invert meaning). Furthermore, r'\\b\\w+\\b' is NOT a complete multilingual "
        "tokenizer: while it matches space-separated Urdu words, it breaks on combining "
        "diacritics/marks and scripts without whitespace boundaries."
    )


def run_faq_chatbot_demo():
    print("\n" + "=" * 72)
    print("TASK 1B: COMMAND-LINE FAQ CHATBOT (TF-IDF BACKEND)")
    print("=" * 72)
    engine = build_bot(backend="tfidf")
    print(f"Loaded {len(FAQ)} FAQs (including 2 newly added FAQs with sources):")
    for item in FAQ:
        print(f"  - [{item['id']}] {item['question']} (source: {item['source']})")

    test_queries = [
        ("Exact canonical match (base FAQ)", "How do I reset my password?"),
        ("Exact canonical match (new FAQ 1)", "Can I get a tuition fee refund after week two?"),
        ("Exact canonical match (new FAQ 2)", "How do I connect to campus Wi-Fi?"),
        ("Non-exact paraphrase -> Suggestion", "forgot password recovery link"),
        ("Non-exact paraphrase (new FAQ) -> Suggestion", "tuition refund medical withdrawal"),
        ("Empty input -> Prompt user", "   "),
        ("Unsupported input -> Help-desk fallback", "volcano geology"),
    ]

    print("\nChatbot Transcript:")
    for label, q in test_queries:
        response = reply(engine, q)
        print(f"\n[{label}]")
        print(f"You: {q}")
        print(f"Bot: {response}")

    # Verification assertions
    assert "it_help.txt" in reply(engine, "How do I reset my password?")
    assert "fee_policy.txt" in reply(
        engine, "Can I get a tuition fee refund after week two?"
    )
    assert "network_guide.txt" in reply(
        engine, "How do I connect to campus Wi-Fi?"
    )
    assert reply(engine, "") == "Please enter a question."
    assert "No matching FAQ" in reply(engine, "volcano geology")
    assert "Possible matches" in reply(engine, "password recovery")

    print("\n" + "-" * 72)
    print("Why the Chatbot Requires Confirmation on Non-Exact Questions:")
    print("-" * 72)
    print(
        "A nonzero lexical or semantic similarity score only reflects surface word overlap "
        "or distributional relatedness—not guaranteed equivalence of intent, conditions, or "
        "policy scope. Automatically asserting an answer on a partial or paraphrased match "
        "could mislead a student with an inapplicable rule (e.g., returning general remote-work "
        "rules to a contractor or missing an exception). Presenting top-ranked canonical "
        "questions for user confirmation keeps a human in the loop before displaying policy answers."
    )


if __name__ == "__main__":
    run_token_comparison()
    run_faq_chatbot_demo()
