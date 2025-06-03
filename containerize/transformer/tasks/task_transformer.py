import logging
from containerize.transformer.tasks.copy import transform_copy
from containerize.transformer.config.config_mount_context import ConfigMountContext

logger = logging.getLogger(__name__)

class TaskTransformer:
    @staticmethod
    def transform_task(task: dict, config_ctx: ConfigMountContext, role_name_hint: str) -> dict | None:
        module_name = TaskTransformer._detect_module(task)

        if not module_name:
            logger.warning(f"⚠️ Could not detect module in task: {task}")
            return None

        match module_name:
            case "copy":
                return transform_copy(task, config_ctx, role_name_hint)
            case "systemd":
                # TODO: Generate Deployment or postStart lifecycle hook
                return {
                    "kind": "Note",
                    "metadata": {"reason": "systemd tasks should be containerized differently"}
                }
            case "shell" | "command":
                return {
                    "kind": "Note",
                    "metadata": {"reason": "Manual review needed for shell/command tasks"}
                }
            case _:
                logger.warning(f"❌ Unsupported module: {module_name}")
                return None

    @staticmethod
    def _detect_module(task: dict) -> str | None:
        # Detects first key that's not 'name' (since it's usually metadata)
        return next((k for k in task if k != "name"), None)
