import logging
import yaml
from pathlib import Path
from containerize.transformer.filters.registry import FilterRegistry

logger = logging.getLogger(__name__)

class PlayLoader:
    def __init__(self, playbook: list, roles_dir: Path, var_context=None):
        self.playbook = playbook
        self.roles_dir = roles_dir
        self.var_context = var_context or {}
        self.jinja_env = FilterRegistry().get_env() 


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
    
    def _render_with_vars(self, value):
        if isinstance(value, str):
            try:
                template = self.jinja_env.from_string(value)
                rendered = template.render(**self.var_context)
                # Try to parse rendered string into structured type (list/dict/bool/etc.)
                
                try:
                    parsed = yaml.safe_load(rendered)
                    return parsed if parsed is not None else rendered
                except Exception as e:
                    logger.warning(f"Failed to parse rendered value: '{rendered}' → {e}")
                    return rendered
            except Exception as e:
                logger.warning(f"Failed to render template: '{value}' → {e}")
                return value
        return value
    
    def _render_deep(self, value):
        if isinstance(value, str):
            return self._render_with_vars(value)

        elif isinstance(value, list):
            return [self._render_deep(item) for item in value]

        elif isinstance(value, dict):
            return {
                self._render_with_vars(k) if isinstance(k, str) else k:
                self._render_deep(v)
                for k, v in value.items()
            }

        # Return primitives (int, float, bool, None) as-is
        return value  

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
                rendered_task = self._render_deep(task)
                expanded.append(rendered_task)

        return expanded

