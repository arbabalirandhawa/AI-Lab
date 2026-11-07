import subprocess
import sys
from pathlib import Path


SCRIPTS = [
    "task1_tokens.py",
    "task1_chatbot_check.py",
    "task2_chunks.py",
    "task2_semantic_check.py",
    "guided_tokens.py",
    "guided_chunks.py",
    "guided_metrics.py",
    "guided_suggestions.py",
    "scenario1_handbook.py",
    "scenario2_support.py",
    "scenario3_docs.py",
    "scenario4_workplace.py",
    "scenario5_equipment.py",
]


def main():
    folder = Path(__file__).resolve().parent

    for script in SCRIPTS:
        print(f"\nRunning {script}...", flush=True)
        subprocess.run([sys.executable, script], cwd=folder, check=True)

    print("\nAll available checks completed successfully.")


if __name__ == "__main__":
    main()
