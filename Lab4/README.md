# Lab 4: Informed Search — Heuristics & A* (CS4944 / CA1601400)

## Description
Applies heuristic evaluation (`f(n) = g(n) + h(n)`) and A* search to a weighted campus navigation graph (`S, A, B, C, G`). Performs programmatic admissibility and consistency audits, compares A* expansion efficiency against a zero-heuristic UCS control under a strict expansion-counting convention, and demonstrates how overestimating `h(C) = 10` causes A* to return a suboptimal route.

## Included Files
- `lab4_astar_audit.py` — Heuristic admissibility/consistency audit, A* search trace, comparison against the zero-heuristic UCS control, and the single-value overestimate experiment (`h(C) = 10`).
- `lab4_ucs.py` — Shared priority-queue search engine and zero-heuristic UCS control implementation, including stale queue-entry filtering verification.
- `Lab4_Report.docx` — Lab 4 academic report containing manual `g/h/f` calculations, heuristic audit tables, A* vs. UCS comparison, and overestimation analysis.
- `output.txt` — Captured console output from executing `lab4_astar_audit.py` and `lab4_ucs.py`.

## Requirements
- Python 3.8+ (standard library `heapq`).

## Execution Commands
```bash
python lab4_astar_audit.py
python lab4_ucs.py
```
