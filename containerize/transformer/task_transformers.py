
from containerize.transformer.task_transformers.copy import transform_copy

class TaskTransformer:
    @staticmethod
    def transform_task(task: dict) -> dict | None:
        module_name = TaskTransformer._detect_module(task)

        match module_name:
            case "copy":
                return transform_copy(task)
            case "systemd":
                return {}
            case "shell" | "command":
                return {}
            case _:
                print(f"Unsupported module: {module_name}")
                return None

    @staticmethod
    def _detect_module(task: dict) -> str:
        # First key in task besides 'name' is usually the module
        return next((k for k in task.keys() if k != "name"), None)
