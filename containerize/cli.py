import typer
from pathlib import Path

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
def transform(playbook: Path, output: Path = Path("./k8s-output")):
    """
    🔄 Convert an Ansible playbook to OpenShift manifests.
    """
    typer.echo(f"⚙️ Transforming {playbook} ...")
    # Placeholder for conversion logic
    typer.echo(f"📁 Generated OpenShift manifests in {out}")

if __name__ == "__main__":
    app()