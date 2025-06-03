from containerize.transformer.config.config_mount_context import ConfigMountContext

def generate_deploymentconfig(config_ctx: ConfigMountContext):
    volume_mounts = []
    volumes = []

    for path, info in config_ctx.mounts.items():
        mount_name = info["configmap_name"]
        volume_mounts.append({
            "name": mount_name,
            "mountPath": path
        })
        volumes.append({
            "name": mount_name,
            "configMap": {
                "name": mount_name
            }
        })

    return {
        "apiVersion": "apps.openshift.io/v1",
        "kind": "DeploymentConfig",
        "metadata": {
            "name": "my-app"
        },
        "spec": {
            "replicas": 1,
            "selector": {"app": "my-app"},
            "template": {
                "metadata": {
                    "labels": {"app": "my-app"}
                },
                "spec": {
                    "containers": [{
                        "name": "my-container",
                        "image": "REPLACE_ME",
                        "volumeMounts": volume_mounts
                    }],
                    "volumes": volumes
                }
            }
        }
    }
