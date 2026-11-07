"""
Lab 1 - Task 1.4, 1.5 & 1.6: Symbolic vs. Probability-Based Decision Comparison
Course: CA1601400 / CS4944 Artificial Intelligence Lab
Note: All scores and probability values are synthetic demonstration inputs.
Review is a routing flag for human inspection, not a final scholarship award.
"""


def symbolic(score, complete):
    return "Review" if complete and score >= 70 else "Hold"


def threshold(probability):
    return "Review" if probability >= 0.70 else "Hold"


def run_comparison():
    cases = [
        ("complete_high", 82, True, 0.81),
        ("complete_low", 68, True, 0.74),
        ("incomplete_high", 91, False, 0.88),
        ("boundary", 70, True, 0.70),
    ]

    print("=== SECTION 1.5: GUIDED SCHOLARSHIP SCREENING COMPARISON ===")
    print("case | score | complete | probability | symbolic | threshold | disagreement")
    print("-" * 78)
    for name, score, complete, probability in cases:
        a = symbolic(score, complete)
        b = threshold(probability)
        disagree = a != b
        print(f"{name:15s} | {score:5d} | {str(complete):8s} | {probability:11.2f} | {a:8s} | {b:9s} | {disagree}")

    print("\n=== SECTION 1.6: BOUNDARY ISOLATION TESTS (69 vs 0.69) ===")
    boundary_tests = [
        ("boundary_exact", 70, True, 0.70, "Both rules meet exact inclusive threshold"),
        ("score_drop_69", 69, True, 0.70, "Score drops below 70; probability stays 0.70"),
        ("prob_drop_0.69", 70, True, 0.69, "Score stays 70; probability drops below 0.70"),
        ("both_drop", 69, True, 0.69, "Both score and probability drop below threshold"),
    ]
    print("test_name | score | complete | probability | symbolic | threshold | disagreement | note")
    print("-" * 105)
    for name, score, complete, prob, note in boundary_tests:
        a = symbolic(score, complete)
        b = threshold(prob)
        print(f"{name:15s} | {score:5d} | {str(complete):8s} | {prob:11.2f} | {a:8s} | {b:9s} | {str(a != b):12s} | {note}")


if __name__ == "__main__":
    run_comparison()
