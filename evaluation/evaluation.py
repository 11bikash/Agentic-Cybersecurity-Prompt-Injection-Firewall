import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from agents.red_team import run_red_team

if __name__ == "__main__":
    rows = run_red_team()
    passed = sum(r["passed"] for r in rows)
    print(f"Passed {passed}/{len(rows)} cases")
    for row in rows:
        print(row)
