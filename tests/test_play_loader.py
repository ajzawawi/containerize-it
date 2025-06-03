from pathlib import Path
from containerize.transformer.play_loader import PlayLoader
from containerize.transformer.context.var_parser import VarContext
import yaml

def describe_play_loader():
    def it_should_flatten_all_tasks_including_imported():
        repo_path = Path("tests/test_projects/playloader_basic")
        site_file = repo_path / "site.yml"
        roles_dir = repo_path / "roles"

        playbook_data = site_file.read_text()
        parsed_playbook = yaml.safe_load(playbook_data)
        
        loader = PlayLoader(playbook=parsed_playbook, roles_dir=roles_dir)
        tasks = loader.load_tasks()
        
        # Assert all tasks are present in the correct order
        task_names = [t["name"] for t in tasks]
        assert task_names == [
            "Log message",  # from setup.yml
            "Greeting",      # from main.yml
            "Final step"    # from main.yml
        ]
                
    def it_should_apply_vars_including_deeply_nested():
        repo_path = Path("tests/test_projects/playloader_basic")
        site_file = repo_path / "site.yml"
        roles_dir = repo_path / "roles"

        playbook_data = site_file.read_text()
        parsed_playbook = yaml.safe_load(playbook_data)
        
        context = VarContext(project_root=repo_path)
        vars = context.load()
                    
        loader = PlayLoader(playbook=parsed_playbook, roles_dir=roles_dir, var_context=vars)
        tasks = loader.load_tasks()

        assert tasks[1]["debug"]["msg"] == "Hi Luke Skywalker from Tatooine"
