import logging
from pathlib import Path
from typing import Dict, List
from containerize.transformer.filters.registry import FilterRegistry
from jinja2 import Environment, StrictUndefined, UndefinedError
import yaml
import re

logger = logging.getLogger(__name__)
INTERPOLATION_PATTERN = re.compile(r"{{.*?}}")
BLOCK_PATTERN = re.compile(r"{%.*?%}", re.DOTALL)


class VarContext:
    """
    VarContext is responsible for collecting and managing Ansible-style variables
    from a project directory.

    It looks for variables in standard Ansible locations:
      - group_vars/
      - host_vars/
      - roles/*/defaults/
      - roles/*/vars/

    The variables are flattened into a single dictionary, following a basic
    Ansible-style precedence (defaults < group_vars/host_vars < role vars).

    Example:
        vc = VarContext(Path("my-ansible-project"))
        variables = vc.load()
        print(variables["my_var"])
    """

    def __init__(self, project_root: Path, exclude_files: List[Path] = None):
        self.project_root = project_root
        self.vars: Dict[str, str] = {}
        self.exclude_files = set(exclude_files or [])
        self.jinja_env = FilterRegistry().get_env() 


    def load(self) -> Dict[str, str]:
        self._load_role_defaults()
        self._load_group_and_host_vars()
        self._load_role_vars()
        self._interpolate_vars()
        return self.vars

    def _should_ignore_file(self, file: Path) -> bool:
        """Check if a file should be excluded based on the test context."""
        return file.resolve() in {f.resolve() for f in self.exclude_files}

    def _parse_yaml_file(self, path: Path) -> Dict:
        try:
            if self._should_ignore_file(path):
                logger.debug(f"Skipping excluded file: {path}")
                return {}
            with open(path, "r") as f:
                data = yaml.safe_load(f)
                return data if isinstance(data, dict) else {}
        except Exception as e:
            logger.warning(f"Failed to parse {path}: {e}")
            return {}

    def _load_role_defaults(self):
        roles_path = self.project_root / "roles"
        if not roles_path.exists():
            return

        for file in roles_path.rglob("defaults/**/*.yml"):
            self.vars.update(self._parse_yaml_file(file))

    def _load_group_and_host_vars(self):
        for folder in ["group_vars", "host_vars"]:
            path = self.project_root / folder
            if not path.exists():
                continue

            for ext in ["*.yml", "*.yaml"]:
                for file in path.rglob(ext):
                    self.vars.update(self._parse_yaml_file(file))

    def _load_role_vars(self):
        roles_path = self.project_root / "roles"
        if not roles_path.exists():
            return

        for file in roles_path.rglob("vars/**/*.yml"):
            self.vars.update(self._parse_yaml_file(file))

    def _interpolate_vars(self, max_depth=30):
        """
        Recursively interpolates Jinja-style variables.
        If the output is a YAML-parseable string (e.g. list or dict), it is parsed into native types.
        """
        def render_string(s: str, context: dict) -> str:
            try:
                return self.jinja_env.from_string(s).render(**context)
            except UndefinedError as e:
                logger.warning(f"Failed to resolve: {s} → {e}")
                return s

        for i in range(max_depth):
            logger.debug(f"Interpolation pass {i + 1}")
            changed = False
            new_vars = {}

            for key, value in self.vars.items():
                if isinstance(value, str) and (
                    INTERPOLATION_PATTERN.search(value) or BLOCK_PATTERN.search(value)
                ):
                    rendered = render_string(value, self.vars)
                    try:
                        parsed = yaml.safe_load(rendered)
                        new_value = parsed if parsed is not None else rendered
                    except Exception as e:
                        logger.warning(f"Failed to parse rendered value for {key}: {e}")
                        new_value = rendered

                    if new_value != value:
                        changed = True
                        logger.debug(f"{key}: '{value}' → '{new_value}'")
                    new_vars[key] = new_value
                else:
                    new_vars[key] = value

            self.vars = new_vars

            if not changed:
                logger.debug("All variables fully resolved.")
                break
        else:
            logger.warning("Reached max interpolation depth without resolving all variables.")