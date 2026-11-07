"""
Lab 3 - Section 3.6 & Task 2: Depth-Limited Search (DLS) and IDDFS
Course: CA1601400 / CS4944 Artificial Intelligence Lab
Uses the original unweighted A-G graph. Root A is at depth 0.
Uses path-local cycle checking (node not in current path) and distinguishes
FOUND, CUTOFF, and FAILURE.
"""

ORIGINAL_GRAPH = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": [],
}


def dls(graph, start, goal, limit):
    """
    Depth-Limited Search with path-local cycle checking.
    Returns (status, path, visit_order) where status is 'FOUND', 'CUTOFF', or 'FAILURE'.
    """
    visit_order = []

    def recursive_dls(node, path, depth):
        visit_order.append(node)
        if node == goal:
            return "FOUND", path
        if depth == limit:
            has_unexplored_child = any(nxt not in path for nxt in graph.get(node, []))
            return ("CUTOFF" if has_unexplored_child else "FAILURE"), None

        cutoff_occurred = False
        for nxt in graph.get(node, []):
            if nxt in path:
                continue
            status, result_path = recursive_dls(nxt, path + [nxt], depth + 1)
            if status == "FOUND":
                return "FOUND", result_path
            if status == "CUTOFF":
                cutoff_occurred = True

        return ("CUTOFF" if cutoff_occurred else "FAILURE"), None

    status, found_path = recursive_dls(start, [start], 0)
    return status, found_path, visit_order


def iddfs(graph, start, goal, max_depth):
    """
    Iterative Deepening Depth-First Search starting from depth 0 up to max_depth.
    Uses a fresh path-local cycle check at every depth limit.
    """
    limits_attempted = []
    all_visits_by_limit = {}
    last_status = "FAILURE"

    for limit in range(0, max_depth + 1):
        limits_attempted.append(limit)
        status, path, visit_order = dls(graph, start, goal, limit)
        all_visits_by_limit[limit] = visit_order
        last_status = status
        if status == "FOUND":
            return "FOUND", path, limits_attempted, all_visits_by_limit
        if status == "FAILURE":
            return "FAILURE", None, limits_attempted, all_visits_by_limit

    return last_status, None, limits_attempted, all_visits_by_limit


def run_depth_experiments():
    print("=== TASK 2A: DEPTH-LIMITED SEARCH (DLS) AT LIMITS 1, 2, 3, AND 4 ===")
    print("limit | status  | returned_path        | visit_order (including goal if reached)")
    print("-" * 88)
    for limit in [1, 2, 3, 4]:
        status, path, visited = dls(ORIGINAL_GRAPH, "A", "G", limit)
        print(f"{limit:5d} | {status:7s} | {str(path):20s} | {visited}")

    print("\n=== TASK 2B: IDDFS WITH MAXIMUM DEPTHS 1, 2, 3, AND 4 (ROOT DEPTH = 0) ===")
    print("max_depth | status  | returned_path        | limits_attempted | total_nodes_processed_across_iterations")
    print("-" * 102)
    for max_d in [1, 2, 3, 4]:
        status, path, limits, visits_map = iddfs(ORIGINAL_GRAPH, "A", "G", max_d)
        total_processed = sum(len(v) for v in visits_map.values())
        print(f"{max_d:9d} | {status:7s} | {str(path):20s} | {str(limits):16s} | {total_processed:3d} -> {visits_map}")

    print("\n=== SECTION 3.8: EDGE CASES FOR DLS AND IDDFS (FOUND vs CUTOFF vs FAILURE) ===")
    s1, p1, v1 = dls(ORIGINAL_GRAPH, "A", "A", limit=1)
    print(f"1. Start == Goal (A -> A, limit=1)        : status={s1}, path={p1}, visited={v1}")

    s2_cut, p2_cut, v2_cut = dls(ORIGINAL_GRAPH, "A", "Z", limit=2)
    s2_fail, p2_fail, v2_fail = dls(ORIGINAL_GRAPH, "A", "Z", limit=4)
    print(f"2a. Unreachable Goal (A -> Z, limit=2)    : status={s2_cut}, path={p2_cut}, visited={v2_cut} (E has child G at depth 3)")
    print(f"2b. Unreachable Goal (A -> Z, limit=4)    : status={s2_fail}, path={p2_fail}, visited={v2_fail} (All branches exhausted)")

    cyclic_graph = {"A": ["B", "C"], "B": ["A", "E"], "C": ["A"], "E": ["G"], "G": []}
    s3, p3, limits3, visits3 = iddfs(cyclic_graph, "A", "G", max_depth=3)
    print(f"3. Cyclic Graph IDDFS (A<->B->E->G, max=3): status={s3}, path={p3}, limits={limits3}")


if __name__ == "__main__":
    run_depth_experiments()
