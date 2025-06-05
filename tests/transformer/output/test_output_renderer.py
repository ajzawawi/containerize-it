import tempfile
from pathlib import Path
import yaml
import pytest

from containerize.transformer.output.output_renderer import OutputRenderer

@pytest.mark.parametrize("output_type", ["helm", "raw"])
def test_output_renderer_end_to_end(output_type):
    k8s_objects = [
        {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {"name": "test-config"},
            "data": {"key": "value"}
        },
        {
            "apiVersion": "apps.openshift.io/v1",
            "kind": "DeploymentConfig",
            "metadata": {"name": "test-app"},
            "spec": {"replicas": 1}
        }
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "out"
        renderer = OutputRenderer(output_type=output_type, output_dir=output_dir)
        renderer.render(k8s_objects)

        if output_type == "raw":
            files = list(output_dir.glob("*.yaml"))
            assert len(files) == 2
            for f in files:
                doc = yaml.safe_load(f.read_text())
                assert "apiVersion" in doc and "kind" in doc

        elif output_type == "helm":
            chart = output_dir / "Chart.yaml"
            values = output_dir / "values.yaml"
            templates = list((output_dir / "templates").glob("*.yaml"))

            assert chart.exists()
            assert values.exists()
            assert len(templates) == 2

            # Sanity check on one of the templates
            doc = yaml.safe_load(templates[0].read_text())
            assert "apiVersion" in doc and "kind" in doc