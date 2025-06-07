from containerize.transformer.playbook_transformer import PlaybookTransformer

from containerize.transformer.context.transform_context import TransformContext

def describe_playbook_transformer():
    def it_should_transform_copy_tasks_and_generate_configmaps_and_deployment():
        playbook = [
            {
                "name": "Apply my_role",
                "hosts": "all",
                "tasks": [
                    {
                        "name": "Copy app.conf",
                        "copy": {
                            "src": "roles/my_role/files/app.conf",
                            "dest": "/etc/myapp/app.conf"
                        }
                    },
                    {
                        "name": "Copy log.conf",
                        "copy": {
                            "src": "roles/my_role/files/log.conf",
                            "dest": "/etc/myapp/log.conf"
                        }
                    },
                    {
                        "name": "Copy input.txt",
                        "copy": {
                            "src": "roles/my_role/files/input.txt",
                            "dest": "/opt/data/input.txt"
                        }
                    }
                ]
            }
        ]

        transform_ctx = TransformContext(
            name="my-app",
            image="my-app-image:latest",
            replicas=1,
            helm_mode=False
        )

        transformer = PlaybookTransformer(playbook, ctx=transform_ctx, role_name_hint="my-role")
        output = transformer.transform()

        configmaps = [res for res in output if res["kind"] == "ConfigMap"]
        deployment = next(res for res in output if res["kind"] == "DeploymentConfig")

        assert len(configmaps) == 2

        etc_map = next(cm for cm in configmaps if cm["metadata"]["name"] == "my-role-etc-myapp")
        assert etc_map["data"]["app.conf"] == "# from roles/my_role/files/app.conf"
        assert etc_map["data"]["log.conf"] == "# from roles/my_role/files/log.conf"

        opt_map = next(cm for cm in configmaps if cm["metadata"]["name"] == "my-role-opt-data")
        assert opt_map["data"]["input.txt"] == "# from roles/my_role/files/input.txt"

        volume_mounts = deployment["spec"]["template"]["spec"]["containers"][0]["volumeMounts"]
        assert {"name": "my-role-etc-myapp", "mountPath": "/etc/myapp"} in volume_mounts
        assert {"name": "my-role-opt-data", "mountPath": "/opt/data"} in volume_mounts

        volumes = deployment["spec"]["template"]["spec"]["volumes"]
        assert {"name": "my-role-etc-myapp", "configMap": {"name": "my-role-etc-myapp"}} in volumes
        assert {"name": "my-role-opt-data", "configMap": {"name": "my-role-opt-data"}} in volumes

        assert deployment["metadata"]["name"] == "my-app"
        assert deployment["spec"]["replicas"] == 1
        assert deployment["spec"]["template"]["spec"]["containers"][0]["image"] == "my-app-image:latest"
        assert deployment["spec"]["template"]["spec"]["containers"][0]["name"] == "my-app-container"