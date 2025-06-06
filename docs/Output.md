# Output

The OutputRenderer is the final step in the containerization pipeline—a bridge between Ansible’s imperative style and Kubernetes’ declarative world. 

It gives teams flexibility in how they adopt the output, whether they’re experimenting locally or deploying at scale in production. 

Once a playbook has been transformed into Kubernetes/OpenShift objects, the final step is rendering those objects to disk. 

## Why OutputRenderer?

Different users and deployment environments have different needs:

* Some want raw YAML to inspect or apply manually.

* Others want a Helm chart to integrate into CI/CD pipelines.

* More advanced teams may want modular Helm subcharts to reflect the original structure of their Ansible roles.

The OutputRenderer is designed to support all these modes from the same transformation output, without requiring the user to re-run or reconfigure the pipeline.

## Architecture

**Separation of Concerns**

OutputRenderer is strictly concerned with formatting and writing files. It doesn’t transform logic or interpret Ansible.

**Pluggable & Extensible**

Each output mode (raw, helm, helm-subcharts) is encapsulated, allowing for future formats without touching transformation logic.

**Consistent Naming & Structure**

Whether generating simple YAML or structured Helm charts, the renderer ensures clear filenames, predictable directory structures, and reproducible output.

**Declarative by Default**

Every output mode is designed to be immediately usable with tools like kubectl, helm install, or oc apply—favoring Kubernetes-native best practices.

