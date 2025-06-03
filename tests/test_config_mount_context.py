from containerize.transformer.config.config_mount_context import ConfigMountContext

def describe_config_mount_context():
    def it_should_group_files_by_mount_path():
        ctx = ConfigMountContext()

        ctx.register_copy_task({
            "name": "Copy app.conf",
            "copy": {
                "src": "roles/my_role/files/app.conf",
                "dest": "/etc/myapp/app.conf"
            }
        }, "my-role")

        ctx.register_copy_task({
            "name": "Copy log.conf",
            "copy": {
                "src": "roles/my_role/files/log.conf",
                "dest": "/etc/myapp/log.conf"
            }
        }, "my-role")

        ctx.register_copy_task({
            "name": "Copy input.txt",
            "copy": {
                "src": "roles/my_role/files/input.txt",
                "dest": "/opt/data/input.txt"
            }
        }, "my-role")

        mounts = ctx.mounts

        assert "/etc/myapp" in mounts
        assert "/opt/data" in mounts

        etc_mount = mounts["/etc/myapp"]
        assert etc_mount["configmap_name"] == "my-role-etc-myapp"
        assert etc_mount["files"]["app.conf"] == "# from roles/my_role/files/app.conf"
        assert etc_mount["files"]["log.conf"] == "# from roles/my_role/files/log.conf"

        opt_mount = mounts["/opt/data"]
        assert opt_mount["configmap_name"] == "my-role-opt-data"
        assert opt_mount["files"]["input.txt"] == "# from roles/my_role/files/input.txt"