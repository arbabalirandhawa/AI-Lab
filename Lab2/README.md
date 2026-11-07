# Lab 2: Intelligent Agents & the PEAS Framework (CS4944 / CA1601400)

## Description
Implements a smart classroom energy-management agent, compares a stateless simple reflex controller with a stateful model-based controller that remembers its previous operating mode to suppress duplicate actuator commands, and evaluates sensor boundary noise around 26°C.

## Included Files
- `lab2_percepts.py` — Guided simple reflex `ClassroomAgent` implementation and 6-step percept trace.
- `lab2_model.py` — Extended `StatefulClassroomAgent` that tracks `previous_mode` and suppresses repeated identical commands across repeated percepts, exact boundaries (`20°C`, `26°C`), mode transitions, and empty-room priority cases.
- `lab2_check.py` — Verification script comparing command counts between the reflex and stateful agents and testing a noisy sequence around `26°C`.
- `Lab2_Report.docx` — Lab 2 academic report containing PEAS specifications, environment classifications, and stateful agent traces.
- `output.txt` — Captured console output from executing `lab2_percepts.py`, `lab2_model.py`, and `lab2_check.py`.

## Requirements
- Python 3.8+ (standard library only).

## Execution Commands
```bash
python lab2_percepts.py
python lab2_model.py
python lab2_check.py
```
