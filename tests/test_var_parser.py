import pytest
from pathlib import Path
from containerize.transformer.var_parser import VarContext

def describe_var_context():
    def it_should_load_vars_from_all_sources():
        repo_path = Path("tests/test_projects/simple")
        
        context = VarContext(project_root=repo_path)
        vars = context.load()
        
        assert "global_var" in vars
        assert vars["global_var"] == "global-value"

        assert "default_var" in vars
        assert vars["default_var"] == "default-value"

        assert "role_var" in vars
        assert vars["role_var"] == "role-value"
        
    def it_should_handle_deeply_nested_vars():
        repo_path = Path("tests/test_projects/deeply_nested")
        
        context = VarContext(project_root=repo_path)
        vars = context.load()
        
        assert len(vars) == 5