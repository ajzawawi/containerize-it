import yaml
import tempfile
from pathlib import Path
from containerize.transformer.output.helm_output_renderer import HelmOutputRenderer

def test_helm_output_renderer_creates_valid_chart_yaml():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "mychart"
        renderer = HelmOutputRenderer(output_dir)
        
        k8s_objects = [
            {
                "apiVersion": "v1",
                "kind": "ConfigMap",
                "metadata": {"name": "my-config"},
                "data": {"key": "value"}
            }
        ]
        
        renderer.render(k8s_objects)

        chart_file = output_dir / "Chart.yaml"
        templates_dir = output_dir / "templates"

        # Assert Chart.yaml exists
        assert chart_file.exists(), "Chart.yaml was not created"
        
        # Assert it's not empty
        content = chart_file.read_text().strip()
        assert content, "Chart.yaml is empty"
        
        # Parse YAML and validate structure
        parsed = yaml.safe_load(content)
        assert parsed.get("apiVersion") == "v2"
        assert parsed.get("name") == "mychart"
        assert parsed.get("version") == "0.1.0"
        assert "description" in parsed

        # Assert at least one template was rendered
        template_files = list(templates_dir.glob("*.yaml"))
        assert template_files, "No templates were rendered"
