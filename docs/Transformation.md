# Transformation

The PlaybookTransformer is responsible for the core transformation step in containerize-it. After Ansible tasks have been loaded and rendered, this class walks through each task and generates the corresponding Kubernetes/OpenShift resource definitions.

It handles:

* Task-to-resource conversion

* Mount tracking and ConfigMap creation

* Deployment generation

The result is a complete list of Kubernetes-compatible objects that can be rendered into raw YAML or Helm charts.

In a nutshell, it:

* Bridges the gap between task-level logic and resource-level infrastructure

* Converts task semantics into declarative Kubernetes objects

* Abstracts resource generation behind a consistent transformation API

* Works in tandem with context objects like ConfigMountContext to track file relationships