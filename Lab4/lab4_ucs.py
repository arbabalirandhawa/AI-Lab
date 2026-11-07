"""
Lab 4 - Section 4.2 & 4.6: Priority-Queue Search Engine and Zero-Heuristic UCS Control
Course: CA1601400 / CS4944 Artificial Intelligence Lab
Counting Convention (Section 4.6):
- A node is logged in processed_nodes when popped (if not a stale queue entry).
- The goal node is logged as processed, but returns immediately before successor examination.
- A node is counted in expanded_nodes ONLY when its successors are examined (goal excluded).
- Stale queue entries (where popped g != best[node]) are ignored and neither processed nor expanded.
"""

import heapq

CAMPUS_GRAPH = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("G", 5)],
    "C": [("G", 3)],
    "G": [],
}

ZERO_HEURISTIC = {"S": 0, "A": 0, "B": 0, "C": 0, "G": 0}


def sum_path_cost(graph, path):
    """Independently calculates total edge weight along a returned path."""
    if not path or len(path) < 2:
        return 0
    total = 0
    for u, v in zip(path[:-1], path[1:]):
        edges = dict(graph.get(u, []))
        total += edges[v]
    return total


def priority_search(graph, h, start, goal):
    """
    Shared priority-queue implementation for A* and UCS (when h(n)=0 for all n).
    Follows the exact guided A* logic from Section 4.2 with trace instrumentation.
    """
    pq = [(h[start], 0, start, [start])]
    best = {start: 0}
    processed_nodes = []
    expanded_nodes = []
    stale_skipped = []
    expansion_trace = []

    while pq:
        f, g, node, path = heapq.heappop(pq)
        if g != best[node]:
            stale_skipped.append((f, g, node, path))
            continue

        processed_nodes.append(node)
        if node == goal:
            return {
                "cost": g,
                "independent_cost": sum_path_cost(graph, path),
                "path": path,
                "processed_nodes": processed_nodes,
                "expanded_nodes": expanded_nodes,
                "expansion_count": len(expanded_nodes),
                "stale_skipped": stale_skipped,
                "expansion_trace": expansion_trace,
            }

        expanded_nodes.append(node)
        for nxt, w in graph.get(node, []):
            ng = g + w
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                heapq.heappush(pq, (ng + h[nxt], ng, nxt, path + [nxt]))

        frontier_snapshot = sorted([(item[0], item[1], item[2], item[3]) for item in pq])
        expansion_trace.append({
            "step": len(expanded_nodes),
            "node": node,
            "g": g,
            "h": h[node],
            "f": f,
            "path": path,
            "frontier": frontier_snapshot,
        })

    return {
        "cost": None,
        "independent_cost": None,
        "path": None,
        "processed_nodes": processed_nodes,
        "expanded_nodes": expanded_nodes,
        "expansion_count": len(expanded_nodes),
        "stale_skipped": stale_skipped,
        "expansion_trace": expansion_trace,
    }


def ucs_control(graph, start, goal):
    """Runs UCS as the zero-heuristic control using the identical priority_search function."""
    zero_h = {node: 0 for node in graph}
    return priority_search(graph, zero_h, start, goal)


def run_ucs_demo():
    print("=== LAB 4: ZERO-HEURISTIC UCS CONTROL RUN ON CAMPUS GRAPH (S -> G) ===")
    res = ucs_control(CAMPUS_GRAPH, "S", "G")
    print(f"Returned Path           : {res['path']}")
    print(f"Reported Cost g(G)      : {res['cost']}")
    print(f"Independent Cost Sum    : {res['independent_cost']}")
    print(f"Processed Nodes (w/ G)  : {res['processed_nodes']} (count={len(res['processed_nodes'])})")
    print(f"Expanded Nodes (no G)   : {res['expanded_nodes']} (expansion_count={res['expansion_count']})")
    print(f"Stale Entries Skipped   : {res['stale_skipped']}\n")

    print("step | expanded | g(n) | h(n) | f(n) | remaining_frontier (f, g, node, path)")
    print("-" * 88)
    for entry in res["expansion_trace"]:
        print(f"{entry['step']:4d} | {entry['node']:8s} | {entry['g']:4d} | {entry['h']:4d} | {entry['f']:4d} | {entry['frontier']}")

    print("\n=== EDGE-CASE TEST: STALE QUEUE ENTRY FILTERING IN UCS ===")
    stale_graph = {
        "S": [("A", 1), ("B", 10)],
        "A": [("B", 2)],
        "B": [("G", 10)],
        "G": [],
    }
    stale_res = ucs_control(stale_graph, "S", "G")
    print(f"Graph: {stale_graph}")
    print(f"Returned Path           : {stale_res['path']} (cost={stale_res['cost']}, verified={stale_res['independent_cost']})")
    print(f"Processed Nodes (w/ G)  : {stale_res['processed_nodes']}")
    print(f"Expanded Nodes (no G)   : {stale_res['expanded_nodes']} (expansion_count={stale_res['expansion_count']})")
    print(f"Stale Entries Ignored   : {stale_res['stale_skipped']}")


if __name__ == "__main__":
    run_ucs_demo()
