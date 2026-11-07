"""
Lab 2 - Task 3: Stateful Classroom Agent with Previous-Mode Memory
Course: CA1601400 / CS4944 Artificial Intelligence Lab
Extends ClassroomAgent to remember its previous target mode and suppress
repeated identical actuator commands while preserving thresholds and priority.
"""


class StatefulClassroomAgent:
    def __init__(self):
        self.previous_mode = None

    def compute_target_mode(self, temp, occupied):
        # Occupancy priority and exact temperature thresholds (< 20, > 26)
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"

    def act(self, temp, occupied):
        prev = self.previous_mode
        target = self.compute_target_mode(temp, occupied)
        # Send command only when the target mode differs from the previous mode
        send_command = target != prev
        command_outcome = "SEND_COMMAND" if send_command else "NO_COMMAND"
        self.previous_mode = target
        return prev, target, send_command, command_outcome


def run_stateful_trace():
    agent = StatefulClassroomAgent()
    # Includes: repeated percepts, exact boundaries (20C, 26C), mode transitions, and empty-room cases
    test_percepts = [
        ((29, True), "Initial high temp (occupied)"),
        ((29, True), "Repeated high temp percept"),
        ((20, True), "Exact lower boundary (20C) -> transition to IDLE"),
        ((26, True), "Exact upper boundary (26C) -> remains IDLE"),
        ((19, True), "Below 20C threshold -> transition to WARM"),
        ((19, True), "Repeated low temp percept"),
        ((29, False), "Empty room priority overrides high temp -> ECO"),
        ((22, False), "Repeated empty room at normal temp -> remains ECO"),
    ]

    print("=== TASK 3: STATEFUL CLASSROOM AGENT MODE-TRANSITION TRACE ===")
    print("step | previous_mode | percept      | target_mode | outcome      | test_case")
    print("-" * 92)
    for step, (percept, desc) in enumerate(test_percepts, 1):
        prev, target, send_cmd, outcome = agent.act(*percept)
        prev_str = str(prev) if prev is not None else "None"
        print(f"{step:4d} | {prev_str:13s} | {str(percept):12s} | {target:11s} | {outcome:12s} | {desc}")


if __name__ == "__main__":
    run_stateful_trace()
