"""
Lab 1 - Task 2: Extended Rule-Based Scholarship Screening System
Course: CA1601400 / CS4944 Artificial Intelligence Lab
Assumptions: All thresholds (score >= 70, gpa >= 3.0, attendance_rate >= 80)
and probability values are synthetic lab assumptions for behavioral comparison.
"""


def extended_rule_based(score, documents_complete, gpa, attendance_rate):
    """
    Evaluates scholarship eligibility for human review using four explicit conditions:
    1. documents_complete == True (original condition)
    2. score >= 70 (original condition)
    3. gpa >= 3.0 (added named condition 1: minimum cumulative GPA)
    4. attendance_rate >= 80 (added named condition 2: minimum attendance percentage)
    Returns (decision, reason).
    """
    failed_reasons = []
    if not documents_complete:
        failed_reasons.append("incomplete documents (documents_complete=False)")
    if score < 70:
        failed_reasons.append(f"score below threshold ({score} < 70)")
    if gpa < 3.0:
        failed_reasons.append(f"GPA below minimum ({gpa:.1f} < 3.0)")
    if attendance_rate < 80:
        failed_reasons.append(f"attendance below minimum ({attendance_rate}% < 80%)")

    if not failed_reasons:
        return "Review", "Passed all 4 explicit rules (complete, score>=70, gpa>=3.0, attendance>=80%)"
    return "Hold", "Failed: " + "; ".join(failed_reasons)


def probability_based(probability):
    return "Review" if probability >= 0.70 else "Hold"


def run_rule_tests():
    # Exactly four required core test cases:
    # 1. Successful pass of all conditions
    # 2. Failure of new condition 1 (gpa < 3.0)
    # 3. Failure of new condition 2 (attendance_rate < 80)
    # 4. Exact threshold boundary case
    core_cases = [
        {
            "name": "Case 1: Full Pass",
            "input": {"score": 84, "documents_complete": True, "gpa": 3.6, "attendance_rate": 92},
            "prob": 0.85,
            "expected": "Review",
        },
        {
            "name": "Case 2: Fail New Condition 1 (Low GPA)",
            "input": {"score": 80, "documents_complete": True, "gpa": 2.7, "attendance_rate": 88},
            "prob": 0.79,
            "expected": "Hold",
        },
        {
            "name": "Case 3: Fail New Condition 2 (Low Attendance)",
            "input": {"score": 78, "documents_complete": True, "gpa": 3.4, "attendance_rate": 74},
            "prob": 0.76,
            "expected": "Hold",
        },
        {
            "name": "Case 4: Exact Threshold Boundary",
            "input": {"score": 70, "documents_complete": True, "gpa": 3.0, "attendance_rate": 80},
            "prob": 0.70,
            "expected": "Review",
        },
    ]

    print("=== TASK 2: EXTENDED RULE-BASED SYSTEM (4 CORE TEST CASES) ===")
    print("Note: Thresholds (score>=70, gpa>=3.0, attendance>=80%) are synthetic lab assumptions.\n")

    for idx, case in enumerate(core_cases, 1):
        inp = case["input"]
        actual, reason = extended_rule_based(
            inp["score"], inp["documents_complete"], inp["gpa"], inp["attendance_rate"]
        )
        prob_decision = probability_based(case["prob"])
        match = actual == case["expected"]
        print(f"[{idx}] {case['name']}")
        print(f"    Input           : score={inp['score']}, documents_complete={inp['documents_complete']}, gpa={inp['gpa']}, attendance_rate={inp['attendance_rate']}%")
        print(f"    Expected Result : {case['expected']}")
        print(f"    Actual Result   : {actual} (Verified: {match})")
        print(f"    Reason          : {reason}")
        print(f"    Prob. Comparison: prob={case['prob']:.2f} -> {prob_decision} (Disagreement: {actual != prob_decision})\n")

    print("=== ADDITIONAL EDGE-CASE CHECK (MISSING DOCUMENTS WITH HIGH SCORE) ===")
    edge_inp = {"score": 95, "documents_complete": False, "gpa": 3.9, "attendance_rate": 96}
    edge_actual, edge_reason = extended_rule_based(**edge_inp)
    edge_prob = probability_based(0.91)
    print(f"    Input           : {edge_inp}, prob=0.91")
    print(f"    Symbolic Result : {edge_actual} ({edge_reason})")
    print(f"    Prob. Result    : {edge_prob} (Disagreement: {edge_actual != edge_prob})")


if __name__ == "__main__":
    run_rule_tests()
