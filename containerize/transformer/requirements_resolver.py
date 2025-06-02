import yaml
import logging
import os
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

class RequirementsResolver:
    def __init__(self, requirements_path: str, role_dir: str = "roles"):
        self.requirements_path = requirements_path
        self.role_dir = role_dir
        self.roles = []
        
    def load(self):
        with open(self.requirements_path, 'r') as f:
            raw = yaml.safe_load(f)
            
        # There are two valid formats for a requirements.yml file
        if isinstance(raw, dict) and "roles" in raw:
            self.roles = raw["roles"]
        elif isinstance(raw, list):
            self.roles = raw
        else:
            logger.error("Invalid requirements.yml format")
            raise ValueError("Expected a list or dict with 'roles'")
        
    def clone_roles(self):
        os.makedirs(self.role_dir, exist_ok=True)
        for role in self.roles:
            name = role["name"]
            src = role["src"]
            version = role.get("version")
            
            dest = os.path.join(self.role_dir, name.replace('.', '/'))
            if os.path.exists(dest):
                logger.info(f"Role '{name}' already exists, skipping.")
                continue
            logger.info(f"Cloning role '{name}' from {src} into {dest}")
            try:
                subprocess.run(["git", "clone", src, dest], check=True)
                if version:
                    subprocess.run(["git", "checkout", version], cwd=dest, check=True)
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to clone role '{name}': {e}")


