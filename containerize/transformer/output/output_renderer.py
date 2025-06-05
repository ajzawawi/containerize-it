
from pathlib import Path
import yaml

from containerize.transformer.output.helm_output_renderer import HelmOutputRenderer

class OutputRenderer:
    def __init__(self, output_type: str, output_dir: Path):
        self.output_type = output_type
        self.output_directory = output_dir
        
    def render(self, k8s_objects: list[dict]):
        # Create the output directory
        self.output_directory.mkdir(parents=True, exist_ok=True)

        if self.output_type == "raw":
            self._render_raw(k8s_objects)
        elif self.output_type == "helm":
            self._render_helm(k8s_objects)
        elif self.output_type == "helm-subcharts":
            self._render_helm_subcharts(k8s_objects)
        else:
            raise ValueError(f"Unsupported output type: {self.output_type}")
            
    def _render_raw(self, k8s_objects):
        for idx, obj in enumerate(k8s_objects):
            kind = obj.get("kind", "UnknownKind").lower()
            name = obj.get("metadata", {}).get("name", f"unnamed-{idx}")
            filename = f"{idx:02d}-{kind}-{name}.yaml"

            with open(self.output_directory / filename, "w") as f:
                yaml.dump(obj, f, sort_keys=False)
    
    def _render_helm(self, k8s_objects):
        HelmOutputRenderer(self.output_directory, mode="flat").render(k8s_objects)

    def _render_helm_subcharts(self, k8s_objects):
        HelmOutputRenderer(self.output_directory, mode="subcharts").render(k8s_objects)