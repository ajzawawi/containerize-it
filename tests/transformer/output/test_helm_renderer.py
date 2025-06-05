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

def test_helm_output_renderer_creates_subcharts_per_role():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "mychart"
        output_dir.mkdir()

        renderer = HelmOutputRenderer(output_dir, mode="subcharts")
        
        k8s_objects = [
            {
                "apiVersion": "v1",
                "kind": "ConfigMap",
                "metadata": {"name": "one", "labels": {"role": "role-a"}},
                "data": {"key1": "value1"}
            },
            {
                "apiVersion": "v1",
                "kind": "ConfigMap",
                "metadata": {"name": "two", "labels": {"role": "role-a"}},
                "data": {"key2": "value2"}
            },
            {
                "apiVersion": "v1",
                "kind": "ConfigMap",
                "metadata": {"name": "three", "labels": {"role": "role-b"}},
                "data": {"key3": "value3"}
            }
        ]

        renderer.render(k8s_objects)

        role_a_chart = output_dir / "charts" / "role-a" / "Chart.yaml"
        role_b_chart = output_dir / "charts"/ "role-b" / "Chart.yaml"
        
        assert role_a_chart.exists(), "role-a Chart.yaml not created"
        assert role_b_chart.exists(), "role-b Chart.yaml not created"

        role_a_templates = list((output_dir / "charts" / "role-a" / "templates").glob("*.yaml"))
        role_b_templates = list((output_dir / "charts" / "role-b" / "templates").glob("*.yaml"))

        assert len(role_a_templates) == 2, "Expected 2 templates for role-a"
        assert len(role_b_templates) == 1, "Expected 1 template for role-b"

        role_a_content = yaml.safe_load(role_a_chart.read_text())
        assert role_a_content["name"] == "role-a"