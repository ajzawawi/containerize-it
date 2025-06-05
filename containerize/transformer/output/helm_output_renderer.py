from pathlib import Path
import yaml

class HelmOutputRenderer:
    """
        Render Kubernetes objects into a Helm chart structure.

        This method generates a directory structure like the following:

        mychart/
        ├── Chart.yaml              # Chart metadata (name, version, etc.)
        ├── values.yaml             # Default configuration values
        ├── charts/                 # Subcharts (dependencies, if any)
        ├── templates/              # Kubernetes manifests and templates
        │   ├── _helpers.tpl        # Template functions/macros
        │   ├── deployment.yaml     # Deployment spec
        │   ├── service.yaml        # Service spec
        │   ├── ingress.yaml        # Ingress spec (optional)
        │   ├── configmap.yaml      # ConfigMap (optional)
        │   ├── secret.yaml         # Secret (optional)
        │   ├── serviceaccount.yaml # ServiceAccount for RBAC (optional)
        │   ├── hpa.yaml            # HorizontalPodAutoscaler (optional)
        │   ├── pvc.yaml            # PersistentVolumeClaim (optional)
        │   └── NOTES.txt           # Post-install CLI notes (optional)
        └── .helmignore             # Patterns to exclude from packaging

        The generated chart will use `values.yaml` for dynamic configuration,
        and templates will reference these values using Helm's templating syntax.

        Args:
            k8s_objects (list[dict]): A list of Kubernetes manifest dictionaries to be converted into Helm templates.
        """
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def render(self, k8s_objects: list[dict]):
        chart_dir = self.output_dir
        templates_dir = chart_dir / "templates"
        chart_dir.mkdir(parents = True, exist_ok = True)
        templates_dir.mkdir(parents = True, exist_ok = True)
        
        chart_yaml = {
            "apiVersion": "v2",
            "name": chart_dir.name,
            "version": "0.1.0",
            "description": "Auto-generated from Ansible playbook"
        }
        
        # Chart
        with open(chart_dir / "Chart.yaml", "w") as f:
            yaml.dump(chart_yaml, sort_keys=False)
           
        # Values.yaml 
        with open(chart_dir / "values.yaml", "w") as f:
            f.write("# Your helm values get added here!\n")
            
        # Templates
        for idx, obj in enumerate(k8s_objects, start=1):
            kind = obj.get("kind", "object").lower()
            filename = f"{kind}-{idx:02d}.yaml"
            with open(templates_dir / filename, "w") as f:
                yaml.dump(obj, f, sort_keys=False)