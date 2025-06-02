
from pathlib import Path


class OutputRenderer:
    def __init__(self, output_type: str, output_dir: Path):
        self.output_type = output_type
        self.output_directory = output_dir
        
    def render(self, k8s_objects: list[dict]):
        if self.output_type == "raw":
            self._render_raw(k8s_objects)
        elif self.output_type == "helm":
            self._render_helm(k8s_objects)
        elif self.output_type == "helm-subcharts":
            self._render_helm_subcharts(k8s_objects)
        else:
            raise ValueError(f"Unsupported output type: {self.output_type}")
            
    def _render_raw(self, k8s_objects):
        pass
    
    def _render_helm(self, k8s_objects):
        pass
    
    def _render_helm_subcharts(self, k8s_objects):
        pass