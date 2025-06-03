from containerize.transformer.config.config_mount_context import ConfigMountContext

def transform_copy(task: dict, config_ctx: ConfigMountContext, role_name_hint: str) -> None:
    config_ctx.register_copy_task(task, configmap_name_hint=role_name_hint)
