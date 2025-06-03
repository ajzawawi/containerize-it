from containerize.transformer.config.config_mount_context import ConfigMountContext
from containerize.transformer.config.deployment_generator import generate_deploymentconfig

def test_generate_deploymentconfig_with_config_mounts():
    ctx = ConfigMountContext()

    # Register multiple copy tasks that go into different mount paths
    ctx.register_copy_task({
        "name": "Copy app.conf",
        "copy": {
            "src": "roles/my_role/files/app.conf",
            "dest": "/etc/myapp/app.conf"
        }
    }, configmap_name_hint="my-role")

    ctx.register_copy_task({
        "name": "Copy input.txt",
        "copy": {
            "src": "roles/my_role/files/input.txt",
            "dest": "/opt/data/input.txt"
        }
    }, configmap_name_hint="my-role")

    dc = generate_deploymentconfig(config_ctx=ctx)

    assert dc["kind"] == "DeploymentConfig"
    assert dc["metadata"]["name"] == "my-app"
    assert dc["spec"]["replicas"] == 1

    # Validate container config
    containers = dc["spec"]["template"]["spec"]["containers"]
    assert len(containers) == 1
    assert containers[0]["name"] == "my-container"
    assert containers[0]["image"] == "REPLACE_ME"

    volume_mounts = containers[0]["volumeMounts"]
    assert {"name": "my-role-etc-myapp", "mountPath": "/etc/myapp"} in volume_mounts
    assert {"name": "my-role-opt-data", "mountPath": "/opt/data"} in volume_mounts

    volumes = dc["spec"]["template"]["spec"]["volumes"]
    assert {"name": "my-role-etc-myapp", "configMap": {"name": "my-role-etc-myapp"}} in volumes
    assert {"name": "my-role-opt-data", "configMap": {"name": "my-role-opt-data"}} in volumes
