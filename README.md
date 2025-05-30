# 🧪 Containerize It

A single CLI to help you:

1. 🩺 **Doctor** your local setup and project for containerization readiness
2. 🔁 **Transform** existing Ansible playbooks into OpenShift/Kubernetes manifests

---

## ✨ Features

- ✅ Run diagnostics on your local system (Docker, OpenShift CLI, Python, etc.)
- 🔍 Analyze your repo for anti-patterns (e.g., hardcoded `/efs/`, missing Dockerfiles)
- 🔄 Convert Ansible playbooks to Kubernetes/OpenShift YAML
- ⚙️ Configurable rules via YAML
- 🧩 Modular and extensible: add your own checks or transformers

---

## 🛠 Installation

```bash
git clone https://github.com/ajzawawi/containerize-it.git
cd containerize-it
pip install -e .
```
---
## 🚀 Usage

🩺 Doctor Mode — Check your environment and repo

```
containerize doctor

```

Examples of common checks:

🐳 Docker or podman installed and running

🔧 oc (OpenShift CLI) is installed

🛡️ Access to your OpenShift project (via oc whoami, etc.)

⚙️ Helm CLI is installed (helm version)

📦 Artifactory access is provisioned and API key is present

📈 Access to Splunk (e.g., ping or test query)

🧪 Python version compatibility

---

## 🔁 Transform Mode — Convert Ansible to K8s/OpenShift


```
containerize transform playbook.yml --out k8s-output/
```

What it does:

Parses your Ansible tasks

Applies rules to generate corresponding OpenShift manifests

Outputs clean YAMLs to the specified folder

---

📂 Example Config
config.yaml:

```yaml
rules:
  - env_check
  - efs_check
  - dockerfile_exists
```