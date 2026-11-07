"""
Lab 3 - Section 3.7, 3.8 & Task 3: Uniform Cost Search (UCS) on Extended Weighted Graph
Course: CA1601400 / CS4944 Artificial Intelligence Lab
Documented Extension (Section 3.7):
Retains original vertices (A-G) and corridors, assigns nonnegative edge weights,
and explicitly adds the C -> G corridor (weight 10) so that:
- BFS prefers A -> C -> G (2 hops, total cost = 2 + 10 = 12)
- UCS finds A -> B -> E -> G (3 hops, total cost = 1 + 1 + 1 = 3)
"""

from collections import deque
import heapq

WEIGHTED_GRAPH = {
    "A": [("B", 1), ("C", 2)],
    "B": [("D", 2), ("E", 1)],
    "C": [("F", 3), ("G", 10)],  # Added corridor C -> G with weight 10
    "D": [],
    "E": [("G", 1)],
    "F": [],
    "G": [],
}


def sum_path_cost(graph, path):
    """Independently sums edge weights along a returned path."""
    if not path or len(path) < 2:
        return 0
    total = 0
    for u, v in zip(path[:-1], path[1:]):
        edge_weights = dict(graph.get(u, []))
        total += edge_weights[v]
    return total


def bfs_on_weighted_topology(graph, start, goal):
    """Runs standard unweighted BFS on the weighted graph topology."""
    q = deque([(start, [start])])
    seen = {start}
    processing_order = []

    while q:
        node, path = q.popleft()
        processing_order.append(node)
        if node == goal:
            return path, processing_order
        for nxt, _weight in graph.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                q.append((nxt, path + [nxt]))
    return None, processing_order


def ucs(graph, start, goal):
    """
    Uniform Cost Search using a min-heap priority queue ordered by accumulated path cost g(n).
    Logs processed nodes (including goal when popped) and skips stale queue entries.
    """
    pq = [(0, start, [start])]
    best_cost = {start: 0}
    processing_order = []
    trace = []

    while pq:
        cost, node, path = heapq.heappop(pq)
        if cost > best_cost.get(node, float("inf")):
            continue
        processing_order.append(node)
        if node == goal:
            trace.append((node, cost, path, [(c, n) for c, n, _ in pq]))
            return cost, path, processing_order, trace

        for nxt, weight in graph.get(node, []):
            new_cost = cost + weight
            if new_cost < best_cost.get(nxt, float("inf")):
                best_cost[nxt] = new_cost
                heapq.heappush(pq, (new_cost, nxt, path + [nxt]))
        trace.append((node, cost, path, [(c, n) for c, n, _ in pq]))

    return None, None, processing_order, trace


def run_ucs_experiment():
    print("=== TASK 3: DOCUMENTED EXTENDED WEIGHTED GRAPH TOPOLOGY ===")
    for u, edges in WEIGHTED_GRAPH.items():
        edge_str = ", ".join(f"{u}->{v} (w={w})" for v, w in edges) if edges else "No outgoing edges"
        print(f"  {u}: {edge_str}")
    print("  * Explicitly documented extension: Added corridor C->G (w=10) per Section 3.7.\n")

    ucs_cost, ucs_path, ucs_order, ucs_trace = ucs(WEIGHTED_GRAPH, "A", "G")
    indep_ucs_cost = sum_path_cost(WEIGHTED_GRAPH, ucs_path)

    print("=== UCS STEP-BY-STEP PROCESSING TRACE (A -> G) ===")
    print("step | processed | g(n) | path_to_node         | pq_after_step (cost, node)")
    print("-" * 82)
    for step, (node, cost, p, pq_state) in enumerate(ucs_trace, 1):
        print(f"{step:4d} | {node:9s} | {cost:4d} | {str(p):20s} | {pq_state}")

    bfs_path, bfs_order = bfs_on_weighted_topology(WEIGHTED_GRAPH, "A", "G")
    indep_bfs_cost = sum_path_cost(WEIGHTED_GRAPH, bfs_path)

    print("\n=== COMPARISON: BFS VS. UCS ON EXTENDED WEIGHTED GRAPH ===")
    print("algorithm | returned_path        | hop_count | reported_cost | independent_cost_sum | processing_order (incl. goal)")
    print("-" * 116)
    print(f"BFS       | {str(bfs_path):20s} | {len(bfs_path)-1:9d} | {'N/A (unw.)':13s} | {indep_bfs_cost:20d} | {bfs_order}")
    print(f"UCS       | {str(ucs_path):20s} | {len(ucs_path)-1:9d} | {ucs_cost:13d} | {indep_ucs_cost:20d} | {ucs_order}")

    print("\n=== SECTION 3.8: UCS EDGE-CASE TESTS ===")
    c_same, p_same, o_same, _ = ucs(WEIGHTED_GRAPH, "A", "A")
    print(f"1. Start == Goal (A -> A)      : cost={c_same}, path={p_same}, processed={o_same}")

    c_unr, p_unr, o_unr, _ = ucs(WEIGHTED_GRAPH, "A", "Z")
    print(f"2. Unreachable Goal (A -> Z)   : cost={c_unr}, path={p_unr}, processed={o_unr}")

    cyclic_weighted = {
        "A": [("B", 2), ("C", 5)],
        "B": [("A", 1), ("C", 1)],
        "C": [("A", 2), ("G", 2)],
        "G": [],
    }
    c_cyc, p_cyc, o_cyc, _ = ucs(cyclic_weighted, "A", "G")
    print(f"3. Cyclic Weighted (A<->B->C->G): cost={c_cyc} (verified={sum_path_cost(cyclic_weighted, p_cyc)}), path={p_cyc}, processed={o_cyc}")


if __name__ == "__main__":
    run_ucs_experiment()
