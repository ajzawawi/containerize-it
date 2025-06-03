from containerize.transformer.config.config_mount_context import ConfigMountContext

def test_config_mount_context_accumulates_copy_tasks():
    ctx = ConfigMountContext()

    ctx.register_copy_task("roles/my_role/files/app.conf", "/etc/myapp/app.conf", "my-role")
    ctx.register_copy_task("roles/my_role/files/log.conf", "/etc/myapp/log.conf", "my-role")
    ctx.register_copy_task("roles/my_role/files/input.txt", "/opt/data/input.txt", "my-role")

    mounts = ctx.mounts

    assert "/etc/myapp" in mounts
    assert "/opt/data" in mounts
    
    print(mounts)

    etc_mount = mounts["/etc/myapp"]
    assert etc_mount["configmap_name"] == "my-role-etc-myapp"
    assert etc_mount["files"]["app.conf"] == "# from roles/my_role/files/app.conf"
    assert etc_mount["files"]["log.conf"] == "# from roles/my_role/files/log.conf"

    opt_mount = mounts["/opt/data"]
    assert opt_mount["configmap_name"] == "my-role-opt-data"
    assert opt_mount["files"]["input.txt"] == "# from roles/my_role/files/input.txt"