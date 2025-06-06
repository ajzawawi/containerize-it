# Overview

The containerize-it cli transforms Ansible playbooks into Kubernetes/OpenShift-native manifests, enabling seamless migration to modern container platforms.

The general flow:

```
Ansible Playbook
   │
   ├──▶ RequirementsResolver   ──┐
   │                            ▼
   ├──▶ PlayLoader         → Rendered Tasks
   │                            ▼
   ├──▶ PlaybookTransformer → K8s Objects
   │                            ▼
   └──▶ OutputRenderer      → YAML / Helm Chart
```

Below is the step-by-step breakdown of how the CLI works under the hood:

🧭 1. Parse the Input Playbook

📦 2. Resolve Role Dependencies

📂 3. Load and Expand Tasks

🔁 4. Transform Tasks to Kubernetes Resources

🖨️ 5. Render the Output
