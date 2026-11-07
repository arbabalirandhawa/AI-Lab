# Lab 3: Uninformed Search — BFS, DFS, DLS, IDDFS & UCS (CS4944 / CA1601400)

## Description
Applies uninformed search strategies to an emergency-exit building graph. Verifies manual frontier traces for BFS and DFS on the original unweighted `A–G` topology, implements Depth-Limited Search (DLS) and Iterative Deepening DFS (IDDFS) with path-local cycle checking across depth limits 1–4, and compares BFS against Uniform Cost Search (UCS) on the documented weighted extension with the added `C -> G` corridor.

## Included Files
- `lab3_bfs_dfs.py` — BFS and DFS implementations on the original unweighted `A–G` graph with step-by-step frontier traces and edge-case tests (`start == goal`, unreachable goal, cyclic graph).
- `lab3_depth_search.py` — DLS and IDDFS implementations distinguishing `FOUND`, `CUTOFF`, and `FAILURE` using path-local cycle checking at limits 1, 2, 3, and 4.
- `lab3_ucs.py` — UCS and unweighted BFS comparison on the extended weighted topology (including the documented `C -> G` corridor of weight 10) with independent path-cost verification.
- `Lab3_Report.docx` — Lab 3 academic report containing manual traces, DLS/IDDFS depth experiments, weighted graph documentation, and UCS vs. BFS comparison.
- `output.txt` — Captured console output from executing `lab3_bfs_dfs.py`, `lab3_depth_search.py`, and `lab3_ucs.py`.

## Requirements
- Python 3.8+ (standard library `collections` and `heapq`).

## Execution Commands
```bash
python lab3_bfs_dfs.py
python lab3_depth_search.py
python lab3_ucs.py
```
