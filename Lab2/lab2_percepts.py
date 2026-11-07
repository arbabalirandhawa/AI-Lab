"""
Lab 2 - Section 2.4 & 2.5: Guided Simple Reflex Classroom Agent
Course: CA1601400 / CS4944 Artificial Intelligence Lab
Note: ECO, COOL, WARM, and IDLE are simulated operating-mode labels.
Temperature is in degrees Celsius; occupied is a Boolean.
"""


class ClassroomAgent:
    def act(self, temp, occupied):
        # Empty room has priority over temperature
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"


def run_percept_trace():
    agent = ClassroomAgent()
    percepts = [
        (29, True),
        (29, True),
        (20, True),
        (26, True),
        (19, True),
        (29, False),
    ]
    print("=== SECTION 2.5: REFLEX AGENT PERCEPT AND ACTION TRACE ===")
    print("step | percept      | target_mode")
    print("-" * 38)
    for step, percept in enumerate(percepts, 1):
        mode = agent.act(*percept)
        print(f"{step:4d} | {str(percept):12s} | {mode}")


if __name__ == "__main__":
    run_percept_trace()
