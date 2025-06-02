from pathlib import Path
from containerize.transformer.play_loader import PlayLoader
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
            "Final step"    # from main.yml
        ]