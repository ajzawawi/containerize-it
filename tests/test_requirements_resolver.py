import shutil
from pathlib import Path
from containerize.transformer.requirements_resolver import RequirementsResolver
from containerize.transformer.var_parser import VarContext

def describe_requirements_resolver():
    def it_should_successfully_process_external_role_requirements(mocker):
        base_project = Path("tests/test_projects/external_requirements")
        requirements_file = base_project / "roles" / "requirements.yml"
        external_repo = base_project / "external" / "external_role_example"
        target_dir = base_project / "roles"

        output_role_path = target_dir / "external_role_example"
        if output_role_path.exists():
            shutil.rmtree(output_role_path)

        # Patch subprocess.run to simulate git clone by copying external/external_role_example
        def fake_git_clone(cmd, check, cwd=None):
            if "clone" in cmd:
                shutil.copytree(external_repo, output_role_path)
            elif "checkout" in cmd:
                pass  # no-op

        mocker.patch("containerize.transformer.requirements_resolver.subprocess.run", side_effect=fake_git_clone)

        resolver = RequirementsResolver(str(requirements_file), str(target_dir))
        resolver.load()
        resolver.clone_roles()
        
        context = VarContext(project_root=base_project)
        vars = context.load()
        
        assert "external_var" in vars
        assert vars["external_var"] == "I'm a variable imported from an external playbook!"
        
        # Assert the cloned role exists and has expected structure
        # Then assert vars loaded
        assert output_role_path.exists()
        assert (output_role_path / "tasks" / "main.yml").exists()
        
        # TODO: better clean up
        if output_role_path.exists():
            shutil.rmtree(output_role_path)
            
    def it_should_account_for_alternative_requirements_format(mocker):
        base_project = Path("tests/test_projects/external_requirements")
        requirements_file = base_project / "roles" / "requirements_alt.yml"
        external_repo = base_project / "external" / "external_role_example"
        target_dir = base_project / "roles"

        output_role_path = target_dir / "external_role_example"
        if output_role_path.exists():
            shutil.rmtree(output_role_path)

        # Patch subprocess.run to simulate git clone by copying external/external_role_example
        def fake_git_clone(cmd, check, cwd=None):
            if "clone" in cmd:
                shutil.copytree(external_repo, output_role_path)
            elif "checkout" in cmd:
                pass  # no-op

        mocker.patch("containerize.transformer.requirements_resolver.subprocess.run", side_effect=fake_git_clone)

        resolver = RequirementsResolver(str(requirements_file), str(target_dir))
        resolver.load()
        resolver.clone_roles()
        
        context = VarContext(project_root=base_project)
        vars = context.load()
        
        assert "external_var" in vars
        assert vars["external_var"] == "I'm a variable imported from an external playbook!"
        
        # Assert the cloned role exists and has expected structure
        # Then assert vars loaded
        assert output_role_path.exists()
        assert (output_role_path / "tasks" / "main.yml").exists()
        
        # TODO: better clean up
        if output_role_path.exists():
            shutil.rmtree(output_role_path)