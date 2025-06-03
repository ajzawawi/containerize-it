import os

class ConfigMountContext:
    def __init__(self):
        self.mounts = {}
    
    def register_copy_task(self, task, configmap_name_hint: str):
        copy_args = task["copy"]
        src = copy_args.get("src")
        dest = copy_args.get("dest")
        
        mount_path = os.path.dirname(dest)
        filename = os.path.basename(dest)
        
        if mount_path not in self.mounts:
            self.mounts[mount_path] = {
                "configmap_name": self._generate_name(configmap_name_hint, mount_path),
                "files": {}
            }
            
        self.mounts[mount_path]["files"][filename] = f"# from {src}"
            
    def _generate_name(self, base, path):
        slug = path.strip("/").replace("/", "-")
        return f"{base}-{slug or 'root'}"