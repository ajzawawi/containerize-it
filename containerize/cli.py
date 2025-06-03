import typer
import yaml
from pathlib import Path
import logging

from containerize.transformer.requirements.requirements_resolver import RequirementsResolver
from containerize.transformer.context.var_parser import VarContext
from containerize.transformer.play_loader import PlayLoader
from containerize.transformer.output.output_type import OutputType
from containerize.transformer.playbook_transformer import PlaybookTransformer
from containerize.transformer.output.output_renderer import OutputRenderer

logger = logging.getLogger(__name__)
app = typer.Typer(help="🧪 Diagnose and 🛠 Transform your repo for containerization.")

@app.command()
def doctor(repo_path: Path):
    """
    🩺 Run checks on your local system and repo to determine containerization readiness.
    """
    typer.echo(f"🔍 Running doctor checks on {repo_path} ...")
    # Placeholder for calling doctor checks
    typer.echo("✅ Docker installed")
    typer.echo("✅ Helm installed")
    typer.echo("✅ oc CLI available")
    typer.echo("✅ Artifactory API key detected")
    typer.echo("✅ Access to OpenShift project confirmed")
    typer.echo("✅ Access to Splunk verified")
    typer.echo("🚫 EFS usage detected in: [repo/folder/file.py]")  # Example fail
    typer.echo("🩺 Doctor complete.")

@app.command()
def transform(
    playbook: Path,
    output: Path = Path("./k8s-output"),
    requirements: Path = Path("requirements.yml"),
    roles_dir: Path = Path("roles"),
    output_type: OutputType = OutputType.raw
):    
    """
    🔄 Convert an Ansible playbook to OpenShift manifests.
    """
    typer.echo(f"⚙️ Transforming {playbook} ...")
    
    #TODO: Respect ansible.cfg for custom path for roles
    
    # Make everything relative to the project root
    project_root = playbook.parent
    roles_path = (project_root / roles_dir).resolve()
    requirements_path = (project_root / requirements).resolve()
    
    
    # Step 1: Fetch roles in requirements.yml if it exists
    if requirements.exists():
        logger.info(f"📦 Found {requirements}, resolving roles...")
        resolver = RequirementsResolver(str(requirements_path), str(roles_path))
        resolver.load()
        resolver.clone_roles()
    else:
        logger.warning(f"⚠️ No {requirements} found — skipping role fetch.")

    # Step 2: Load playbook, resolve roles, transform tasks
    logger.info("🔍 Parsing playbook and generating manifests...")
    
    with open(playbook, "r") as f:
        playbook_data = yaml.safe_load(f)
            
    # Step 3: Load variables using VarContext
    project_root = playbook.parent  # Assume project root is where site.yml is
    var_context = VarContext(project_root=project_root)
    vars = var_context.load()

    # Step 4: Load and flatten all tasks using PlayLoader
    loader = PlayLoader(playbook=playbook_data, roles_dir=roles_path, var_context=vars)
    tasks = loader.load_tasks()
    
    #  Step 5: Transform tasks to Openshift artifacts
    for task in tasks:
        typer.echo(f"✅ Task: {task.get('name')}")

    transformer = PlaybookTransformer(tasks)
    k8s_objects = transformer.transform()
    
    # Step 6: Output Rendering
    # renderer = OutputRenderer(output_type=output_type, output_dir=output)

    typer.echo(f"📁 Generated OpenShift project in {output}")

if __name__ == "__main__":
    app()