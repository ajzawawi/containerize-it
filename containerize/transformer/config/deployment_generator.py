from containerize.transformer.config.config_mount_context import ConfigMountContext

from containerize.transformer.context.transform_context import TransformContext

def generate_deploymentconfig(config_ctx: ConfigMountContext, ctx: TransformContext):
    name = "{{ .Values.name }}" if ctx.helm_mode else ctx.name
    image = "{{ .Values.image }}" if ctx.helm_mode else ctx.image
    replicas = "{{ .Values.replicas }}" if ctx.helm_mode else ctx.replicas
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
            "name": name
        },
        "spec": {
            "replicas": replicas,
            "selector": {"app": name},
            "template": {
                "metadata": {
                    "labels": {"app": name }
                },
                "spec": {
                    "containers": [{
                        "name": f"{name}-container",
                        "image": image,
                        "volumeMounts": volume_mounts
                    }],
                    "volumes": volumes
                }
            }
        }
    }
