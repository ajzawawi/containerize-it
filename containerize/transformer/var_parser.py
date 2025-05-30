import logging
from pathlib import Path
from typing import Dict
import yaml

logger = logging.getLogger(__name__)

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
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.vars: Dict[str, str] = {}

    def load(self):
        self._load_group_and_host_vars()
        self._load_role_vars()
        return self.vars

    def _parse_yaml_file(self, path: Path) -> Dict:
       try:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else {}
       except Exception as e:
           logger.warning(f"Failed to parse {path}: {e}")
           return {}

    def _load_group_and_host_vars(self):
        for folder in ["group_vars", "host_vars"]:
            for file in (self.project_root / folder).rglob("*.yml"):
                self.vars.update(self._parse_yaml_file(file))

    def _load_role_vars(self):
        roles_path = self.project_root / "roles"
        if not roles_path.exists():
            return

        for file in roles_path.rglob("*/defaults/*.yml"):
            self.vars.update(self._parse_yaml_file(file))

        for file in roles_path.rglob("*/vars/*.yml"):
            self.vars.update(self._parse_yaml_file(file))