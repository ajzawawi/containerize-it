from containerize.transformer.tasks.task_transformer import TaskTransformer
from containerize.transformer.config.config_mount_context import ConfigMountContext
from containerize.transformer.config.deployment_generator import generate_deploymentconfig

class PlaybookTransformer:
    def __init__(self, playbook: dict, role_name_hint: str = "generated"):
        self.playbook = playbook
        self.output = []
        self.config_ctx = ConfigMountContext()
        self.role_name_hint = role_name_hint
    
    def transform(self):
        for play in self.playbook:
            tasks = play.get("tasks", [])
            for task in tasks:
                self.config_ctx.register_copy_task(task, configmap_name_hint=self.role_name_hint)
                result = TaskTransformer.transform_task(task)
                if result:
                    self.output.append(result)
        self._generate_grouped_config_maps()
        self._generate_deployment_config()
        return self.output
    
    def _generate_grouped_config_maps(self):
        for mount_path, info in self.config_ctx.mounts.items():
            configmap = {
                "apiVersion": "v1",
                "kind": "ConfigMap",
                "metadata": {"name": info["configmap_name"]},
                "data": info["files"]
            }
            self.output.append(configmap)
    
    def _generate_deployment_config(self):
        deployment = generate_deploymentconfig(self.config_ctx)
        self.output.append(deployment)