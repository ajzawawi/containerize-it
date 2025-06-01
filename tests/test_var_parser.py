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
        
    def it_should_handle_deeply_nested_group_vars():
        repo_path = Path("tests/test_projects/deeply_nested")
        
        context = VarContext(project_root=repo_path)
        vars = context.load()
        
        assert len(vars) == 6
        assert "top_level_env" in vars
        assert "deeply_nested_role_var" in vars
        
    def it_should_resolve_using_ansible_precedence_rules():
        project = Path("tests/test_projects/precedence")
        ctx = VarContext(project)
        vars = ctx.load()

        assert vars["fruit"] == "kiwi"
        assert vars["color"] == "green"
        assert len(vars) == 2
    
    def it_should_respect_precedence_without_role_vars():
        project = Path("tests/test_projects/precedence")

        # Simulate missing role vars
        exclude = [
            project / "roles/my-role/vars/main.yml" 
        ]

        ctx = VarContext(project_root=project, exclude_files=exclude)
        vars = ctx.load()
        
        assert vars["fruit"] == "apples"
        assert vars["color"] == "green"
        assert len(vars) == 2
        
    def it_should_respect_precedence_without_group_vars():
        project = Path("tests/test_projects/precedence")

        # Simulate missing role vars
        exclude = [
            project / "roles/my-role/vars/main.yml",
            project / "group_vars/all.yml" 
        ]

        ctx = VarContext(project_root=project, exclude_files=exclude)
        vars = ctx.load()
        
        assert vars["fruit"] == "apples"
        assert vars["color"] == "red"
        assert len(vars) == 2
        
    def it_should_resolve_variable_references():
        project = Path("tests/test_projects/interpolation")
        ctx = VarContext(project_root=project)
        
        vars = ctx.load()
        assert vars["full_name"] == "Luke Skywalker"

    def it_should_fail_to_resolve_nested_templates():
        project = Path("tests/test_projects/interpolation")
        ctx = VarContext(project_root=project)
        vars = ctx.load()

        assert vars["name_address"] == "Luke Skywalker - Tatooine"
        
    def it_should_resolve_block_jinja_into_list():
        project = Path("tests/test_projects/interpolation")
        ctx = VarContext(project_root=project)
        vars = ctx.load()

        print(vars)
        assert vars["users"] == [{"name": "Luke"}, {"name": "Leia"}]
        assert vars["usernames"] == ["Luke", "Leia"]

    def it_should_resolve_inline_jinja_loop_with_filters():
        project = Path("tests/test_projects/interpolation")
        ctx = VarContext(project_root=project)
        vars = ctx.load()

        assert vars["users"] == [{"name": "Luke"}, {"name": "Leia"}]
        assert vars["usernames"] == ["Luke", "Leia"]