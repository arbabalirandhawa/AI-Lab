"""
Lab 2 - Section 2.7 & Verification: Reflex vs. Stateful Comparison and Hysteresis Check
Course: CA1601400 / CS4944 Artificial Intelligence Lab
Compares command counts between the simple reflex agent and the stateful agent,
and tests a noisy sequence oscillating around the 26C boundary.
"""

from lab2_percepts import ClassroomAgent
from lab2_model import StatefulClassroomAgent


def run_verification():
    reflex_agent = ClassroomAgent()
    stateful_agent = StatefulClassroomAgent()

    sequence = [
        (29, True),
        (29, True),
        (20, True),
        (26, True),
        (19, True),
        (29, False),
    ]

    print("=== 1. REFLEX VS. STATEFUL AGENT COMPARISON ON STANDARD SEQUENCE ===")
    print("step | percept      | reflex_cmd | stateful_prev | stateful_target | stateful_outcome")
    print("-" * 86)
    reflex_commands = 0
    stateful_commands = 0

    for step, percept in enumerate(sequence, 1):
        r_mode = reflex_agent.act(*percept)
        reflex_commands += 1
        prev, s_target, send_cmd, outcome = stateful_agent.act(*percept)
        if send_cmd:
            stateful_commands += 1
        print(f"{step:4d} | {str(percept):12s} | {r_mode:10s} | {str(prev):13s} | {s_target:15s} | {outcome}")

    print(f"\nTotal actuator commands sent -> Reflex: {reflex_commands}, Stateful: {stateful_commands}")

    print("\n=== 2. SECTION 2.7 EDGE CASE: NOISY SENSOR SEQUENCE AROUND 26C BOUNDARY ===")
    print("Demonstrates that remembering previous_mode does not provide hysteresis against sensor noise.")
    noisy_agent = StatefulClassroomAgent()
    noisy_percepts = [
        (26.1, True),
        (25.9, True),
        (26.2, True),
        (25.8, True),
        (26.1, True),
    ]
    print("step | previous_mode | percept        | target_mode | outcome")
    print("-" * 65)
    noisy_cmds = 0
    for step, percept in enumerate(noisy_percepts, 1):
        prev, target, send_cmd, outcome = noisy_agent.act(*percept)
        if send_cmd:
            noisy_cmds += 1
        print(f"{step:4d} | {str(prev):13s} | {str(percept):14s} | {target:11s} | {outcome}")
    print(f"Commands triggered during 5 noisy steps: {noisy_cmds}/5 (oscillates COOL <-> IDLE every step).")


if __name__ == "__main__":
    run_verification()
