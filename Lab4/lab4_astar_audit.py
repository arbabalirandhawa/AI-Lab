"""
Lab 4 - Tasks 1, 2 & 3: Heuristic Audit, A* vs. UCS Comparison, and Overestimate Experiment
Course: CA1601400 / CS4944 Artificial Intelligence Lab
Implements A* search, verifies heuristic admissibility and consistency,
compares A* against the zero-heuristic UCS control, and evaluates the h(C)=10 overestimate.
"""

from lab4_ucs import CAMPUS_GRAPH, ZERO_HEURISTIC, priority_search

SUPPLIED_HEURISTIC = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}
TRUE_REMAINING_COST = {"S": 6, "A": 5, "B": 5, "C": 3, "G": 0}


def audit_heuristic(graph, h, true_h, label):
    print(f"=== HEURISTIC AUDIT: {label} ===")
    print("1. Admissibility Check: h(n) <= h*(n) for every node")
    print("node | h(n) | true_remaining h*(n) | admissible?")
    print("-" * 50)
    all_admissible = True
    for node in ["S", "A", "B", "C", "G"]:
        adm = h[node] <= true_h[node]
        all_admissible = all_admissible and adm
        print(f"{node:4s} | {h[node]:4d} | {true_h[node]:20d} | {adm}")

    print("\n2. Consistency Check: h(u) <= cost(u,v) + h(v) for every directed edge u -> v")
    print("edge   | h(u) | cost(u,v) | h(v) | rhs = c+h(v) | consistent?")
    print("-" * 62)
    all_consistent = True
    for u, edges in graph.items():
        for v, w in edges:
            rhs = w + h[v]
            cons = h[u] <= rhs
            all_consistent = all_consistent and cons
            print(f"{u} -> {v} | {h[u]:4d} | {w:9d} | {h[v]:4d} | {rhs:12d} | {cons}")

    print(f"Audit Summary -> Admissible: {all_admissible} | Consistent: {all_consistent}\n")


def print_expansion_trace(title, res):
    print(f"=== {title} ===")
    print("step | expanded | g(n) | h(n) | f(n) | path_to_node       | remaining_frontier (f, g, node, path)")
    print("-" * 105)
    for entry in res["expansion_trace"]:
        print(
            f"{entry['step']:4d} | {entry['node']:8s} | {entry['g']:4d} | {entry['h']:4d} | "
            f"{entry['f']:4d} | {str(entry['path']):18s} | {entry['frontier']}"
        )
    print(f"Returned Path          : {res['path']}")
    print(f"Reported Cost / Summed : {res['cost']} / {res['independent_cost']}")
    print(f"Processed Nodes (w/ G) : {res['processed_nodes']} (total={len(res['processed_nodes'])})")
    print(f"Expanded Nodes (no G)  : {res['expanded_nodes']} (expansion_count={res['expansion_count']})\n")


def run_all_tasks():
    audit_heuristic(CAMPUS_GRAPH, SUPPLIED_HEURISTIC, TRUE_REMAINING_COST, "Supplied Heuristic (S:5, A:4, B:4, C:2, G:0)")

    astar_res = priority_search(CAMPUS_GRAPH, SUPPLIED_HEURISTIC, "S", "G")
    print_expansion_trace("TASK 1 & 2: A* EXPANSION TRACE WITH SUPPLIED HEURISTIC", astar_res)

    ucs_res = priority_search(CAMPUS_GRAPH, ZERO_HEURISTIC, "S", "G")
    print_expansion_trace("TASK 2: UCS CONTROL EXPANSION TRACE (ZERO HEURISTIC)", ucs_res)

    over_h = dict(SUPPLIED_HEURISTIC)
    over_h["C"] = 10
    audit_heuristic(CAMPUS_GRAPH, over_h, TRUE_REMAINING_COST, "Modified Overestimating Heuristic (h(C)=10)")

    over_res = priority_search(CAMPUS_GRAPH, over_h, "S", "G")
    print_expansion_trace("TASK 3: A* EXPANSION TRACE WITH OVERESTIMATE h(C)=10", over_res)

    print("=== SUMMARY COMPARISON TABLE (A* SUPPLIED vs. UCS CONTROL vs. A* OVERESTIMATE) ===")
    print("run_name                 | returned_path        | cost | indep_sum | processed_nodes (w/ G)    | expanded_nodes (no G) | exp_count")
    print("-" * 132)
    rows = [
        ("A* (Supplied h)", astar_res),
        ("UCS Control (h=0)", ucs_res),
        ("A* Overestimate h(C)=10", over_res),
    ]
    for label, r in rows:
        print(
            f"{label:24s} | {str(r['path']):20s} | {r['cost']:4d} | {r['independent_cost']:9d} | "
            f"{str(r['processed_nodes']):25s} | {str(r['expanded_nodes']):21s} | {r['expansion_count']:9d}"
        )

    print("\n=== ADDITIONAL EDGE-CASE CHECKS (START==GOAL & UNREACHABLE GOAL) ===")
    same_res = priority_search(CAMPUS_GRAPH, SUPPLIED_HEURISTIC, "S", "S")
    print(f"1. Start == Goal (S -> S)    : path={same_res['path']}, cost={same_res['cost']}, processed={same_res['processed_nodes']}, expanded={same_res['expanded_nodes']} (count={same_res['expansion_count']})")
    unr_graph = dict(CAMPUS_GRAPH)
    unr_graph["Z"] = []
    unr_h = dict(SUPPLIED_HEURISTIC, Z=0)
    unr_res = priority_search(unr_graph, unr_h, "S", "Z")
    print(f"2. Unreachable Goal (S -> Z) : path={unr_res['path']}, cost={unr_res['cost']}, processed={unr_res['processed_nodes']}, expanded={unr_res['expanded_nodes']} (count={unr_res['expansion_count']})")


if __name__ == "__main__":
    run_all_tasks()
