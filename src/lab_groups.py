from collections import Counter
from typing import Any

from src.content.lab import LAB_TASKS


def propose_groups(students: list[dict[str, Any]], group_size: int = 3) -> list[dict[str, Any]]:
    """Transparent demo grouping: sort by readiness then distribute round-robin."""
    ordered = sorted(students, key=lambda s: s.get("readiness", 0), reverse=True)
    n_groups = max(1, (len(ordered) + group_size - 1) // group_size)
    groups = [[] for _ in range(n_groups)]
    for i, student in enumerate(ordered):
        group_index = i % n_groups if (i // n_groups) % 2 == 0 else (n_groups - 1 - i % n_groups)
        groups[group_index].append(student)

    task_names = [t["task"] for t in LAB_TASKS]
    output = []
    for i, members in enumerate(groups, start=1):
        roles = []
        used = Counter()
        for j, student in enumerate(members):
            limited = student.get("limited_opportunities", [])
            selected = next((name for name in limited if name in task_names and not used[name]), None)
            if selected is None:
                selected = task_names[(i + j - 2) % len(task_names)]
            used[selected] += 1
            roles.append({"student": student["name"], "task": selected})
        output.append({"group": f"Group {i}", "members": roles})
    return output
