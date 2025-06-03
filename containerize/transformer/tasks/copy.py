
def transform_copy(task):
    copy_args = task.get("copy", {})
    src = copy_args.get("src")
    dest = copy_args.get("dest")
    
    # Create a ConfigMap YAML dict
    return {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {"name": "generated-config"},
        "data": {
            dest.split('/')[-1]: f"# from {src} (content placeholder)"
        }
    }