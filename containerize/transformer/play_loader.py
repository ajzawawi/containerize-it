import yaml
from pathlib import Path

class PlayLoader:
    def __init__(self, playbook: list, roles_dir: Path):
        self.playbook = playbook
        self.roles_dir = roles_dir

    def load_tasks(self):
        all_tasks = []

        for play in self.playbook:
            if "roles" in play:
                for role_entry in play["roles"]:
                    role_name = role_entry if isinstance(role_entry, str) else role_entry.get("role") or role_entry.get("name")
                    role_path = self.roles_dir / role_name
                    main_task_file = role_path / "tasks" / "main.yml"

                    if not main_task_file.exists():
                        raise FileNotFoundError(f"{main_task_file} not found for role {role_name}")

                    all_tasks.extend(self._expand_tasks(main_task_file, role_path / "tasks"))
            else:
                all_tasks.extend(play.get("tasks", []))

        return all_tasks

    def _expand_tasks(self, file: Path, base_dir: Path) -> list:
        with open(file) as f:
            tasks = yaml.safe_load(f) or []

        expanded = []
        for task in tasks:
            if "import_tasks" in task or "include" in task:
                task_file = task.get("import_tasks") or task.get("include")
                include_path = base_dir / task_file
                if not include_path.exists():
                    raise FileNotFoundError(f"Included file {include_path} not found")

                included_tasks = self._expand_tasks(include_path, base_dir)
                expanded.extend(included_tasks)
            else:
                expanded.append(task)

        return expanded

    