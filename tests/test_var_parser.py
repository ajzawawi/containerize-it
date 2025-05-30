from pathlib import Path
from containerize.transformer.var_parser import VarContext

def test_var_resolution():
    repo_path = Path("tests/test_projects/sample_ansible_project")
    
    context = VarContext(project_root=repo_path)
    vars = context.load()
    
    assert "global_var" in vars
    assert vars["global_var"] == "global-value"

    assert "default_var" in vars
    assert vars["default_var"] == "default-value"

    assert "role_var" in vars
    assert vars["role_var"] == "role-value"