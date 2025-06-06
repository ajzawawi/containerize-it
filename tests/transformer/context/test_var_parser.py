import pytest
from pathlib import Path
from containerize.transformer.context.var_parser import VarContext

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

        assert vars["users"] == [{"name": "Luke"}, {"name": "Leia"}]
        assert vars["usernames"] == ["Luke", "Leia"]

    def it_should_resolve_inline_jinja_loop_with_filters():
        project = Path("tests/test_projects/interpolation")
        ctx = VarContext(project_root=project)
        vars = ctx.load()

        assert vars["users"] == [{"name": "Luke"}, {"name": "Leia"}]
        assert vars["usernames"] == ["Luke", "Leia"]
        
    def it_should_apply_ansible_combine_filter():
        project = Path("tests/test_projects/interpolation")
        ctx = VarContext(project_root=project)
        vars = ctx.load()
        
        assert vars["combined"] == {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }

    def it_should_apply_ansible_dict2items_filter():
        project = Path("tests/test_projects/interpolation")
        ctx = VarContext(project_root=project)
        vars = ctx.load()
        
        assert vars["dict_items"] == [
            {"key": "key1", "value": "value1"},
            {"key": "key2", "value": "value2"}
        ]


    def it_should_apply_ansible_flatten_filter():
        project = Path("tests/test_projects/interpolation")
        ctx = VarContext(project_root=project)
        vars = ctx.load()
        
        assert vars["flat_users"] == [{"name": "Luke"}, {"name": "Leia"}]
        
        
    def it_should_apply_unique_filter_case_insensitive():
        project = Path("tests/test_projects/interpolation")
        ctx = VarContext(project_root=project)
        vars = ctx.load()
        
        insensitive = vars["unique_users_case_insensitive"]
        assert isinstance(insensitive, list)
        assert len(insensitive) == 2  # "Luke" and "Leia"
        names = {u["name"].lower() for u in insensitive}
        assert names == {"luke", "leia"}

    def it_should_apply_difference_filter():
        project = Path("tests/test_projects/filter_tests")
        ctx = VarContext(project_root=project)
        vars = ctx.load()

        result = vars["difference_result"]
        assert isinstance(result, list)
        assert result == [1, 2]

    def it_should_apply_intersect_filter():
        project = Path("tests/test_projects/filter_tests")
        ctx = VarContext(project_root=project)
        vars = ctx.load()

        result = vars["intersect_result"]
        assert isinstance(result, list)
        assert result == [3, 4, 5]
        
    def it_should_apply_union_filter():
        project = Path("tests/test_projects/filter_tests")
        ctx = VarContext(project_root=project)
        vars = ctx.load()

        result = vars["union_result"]
        assert isinstance(result, list)
        assert result == [1, 2, 3, 4, 5, 6]
        
    def it_should_apply_map_filter():
        project = Path("tests/test_projects/filter_tests")
        ctx = VarContext(project_root=project)
        vars = ctx.load()

        usernames = vars["usernames"]
        assert isinstance(usernames, list)
        assert usernames == ["Luke", "Leia", "Han"]
        
    def it_should_apply_select_filter():
        project = Path("tests/test_projects/filter_tests")
        ctx = VarContext(project_root=project)
        vars = ctx.load()

        selected = vars["selected"]
        assert isinstance(selected, list)
        assert selected == [1, 3, 5]
        
    def it_should_apply_reject_filter():
        project = Path("tests/test_projects/filter_tests")
        ctx = VarContext(project_root=project)
        vars = ctx.load()

        rejected = vars["rejected"]
        assert isinstance(rejected, list)
        assert rejected == [1, 3, 5]
        
    def it_should_apply_selectattr_filter():
        project = Path("tests/test_projects/filter_tests")
        ctx = VarContext(project_root=project)
        vars = ctx.load()

        result = vars["active_users"]
        assert isinstance(result, list)
        assert len(result) == 2
        names = {user["name"] for user in result}
        assert names == {"Luke", "Han"}
        
    def it_should_apply_rejectattr_filter():
        project = Path("tests/test_projects/filter_tests")
        ctx = VarContext(project_root=project)
        vars = ctx.load()

        result = vars["inactive_users"]
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["name"] == "Leia"
        
    def it_should_apply_items2dict_filter():
        project = Path("tests/test_projects/filter_tests")
        ctx = VarContext(project_root=project)
        vars = ctx.load()

        result = vars["user_dict"]
        assert isinstance(result, dict)
        assert result == {"name": "Luke", "planet": "Tatooine"}