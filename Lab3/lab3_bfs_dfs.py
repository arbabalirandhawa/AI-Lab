"""
Lab 3 - Section 3.2, 3.5 & Task 1: BFS and DFS Implementation and Trace Verification
Course: CA1601400 / CS4944 Artificial Intelligence Lab
Uses the original unweighted A-G emergency-exit graph from Section 3.2.
Convention: Log each node removed from queue/stack and processed, including the goal.
"""

from collections import deque

ORIGINAL_GRAPH = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": [],
}


def bfs(graph, start, goal):
    q = deque([(start, [start])])
    seen = {start}
    visit_order = []
    trace = []

    while q:
        node, path = q.popleft()
        visit_order.append(node)
        if node == goal:
            trace.append((node, path, [item[0] for item in q]))
            return path, visit_order, trace
        for n in graph.get(node, []):
            if n not in seen:
                seen.add(n)
                q.append((n, path + [n]))
        trace.append((node, path, [item[0] for item in q]))
    return None, visit_order, trace


def dfs(graph, start, goal):
    stack = [(start, [start])]
    seen = set()
    visit_order = []
    trace = []

    while stack:
        node, path = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        visit_order.append(node)
        if node == goal:
            trace.append((node, path, [item[0] for item in stack]))
            return path, visit_order, trace
        # Reversed insertion ensures the first listed neighbour is popped first (LIFO)
        for n in reversed(graph.get(node, [])):
            if n not in seen:
                stack.append((n, path + [n]))
        trace.append((node, path, [item[0] for item in stack]))
    return None, visit_order, trace


def print_trace(title, path, visit_order, trace, frontier_label):
    print(f"=== {title} ===")
    print(f"step | processed | path_to_node         | {frontier_label} (after step)")
    print("-" * 74)
    for step, (node, p, frontier) in enumerate(trace, 1):
        print(f"{step:4d} | {node:9s} | {str(p):20s} | {frontier}")
    print(f"Returned Path : {path} (hops: {len(path) - 1 if path else 'N/A'})")
    print(f"Visit Order   : {visit_order} (total processed including goal: {len(visit_order)})\n")


def run_all():
    bfs_path, bfs_order, bfs_trace = bfs(ORIGINAL_GRAPH, "A", "G")
    print_trace("TASK 1A: BFS TRACE ON ORIGINAL A-G GRAPH", bfs_path, bfs_order, bfs_trace, "queue_frontier_front_to_back")

    dfs_path, dfs_order, dfs_trace = dfs(ORIGINAL_GRAPH, "A", "G")
    print_trace("TASK 1B: DFS TRACE ON ORIGINAL A-G GRAPH", dfs_path, dfs_order, dfs_trace, "stack_frontier_bottom_to_top")

    print("=== SECTION 3.8: EDGE-CASE TESTS (BFS & DFS) ===")
    p_bfs_same, v_bfs_same, _ = bfs(ORIGINAL_GRAPH, "A", "A")
    p_dfs_same, v_dfs_same, _ = dfs(ORIGINAL_GRAPH, "A", "A")
    print(f"1. Start == Goal (A -> A)      | BFS path: {p_bfs_same}, visited: {v_bfs_same} | DFS path: {p_dfs_same}, visited: {v_dfs_same}")

    p_bfs_unr, v_bfs_unr, _ = bfs(ORIGINAL_GRAPH, "A", "Z")
    p_dfs_unr, v_dfs_unr, _ = dfs(ORIGINAL_GRAPH, "A", "Z")
    print(f"2. Unreachable Goal (A -> Z)   | BFS path: {p_bfs_unr}, visited: {v_bfs_unr} | DFS path: {p_dfs_unr}, visited: {v_dfs_unr}")

    cyclic_graph = {"A": ["B", "C"], "B": ["A", "D"], "C": ["B"], "D": ["G"], "G": []}
    p_bfs_cyc, v_bfs_cyc, _ = bfs(cyclic_graph, "A", "G")
    p_dfs_cyc, v_dfs_cyc, _ = dfs(cyclic_graph, "A", "G")
    print(f"3. Cyclic Graph (A<->B->D->G)  | BFS path: {p_bfs_cyc}, visited: {v_bfs_cyc} | DFS path: {p_dfs_cyc}, visited: {v_dfs_cyc}")


if __name__ == "__main__":
    run_all()
