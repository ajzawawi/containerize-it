# Plays
An Ansible play is a unit of execution in an Ansible playbook. Each play maps a group of hosts to a set of roles or tasks, which are executed in order. Plays are defined in YAML and are typically structured like this:

```yaml
- name: Configure Web Server
  hosts: web
  roles:
    - nginx
```

Within each play:

- hosts defines the target machines.

- roles or tasks define the logic to run.

- Roles include reusable components like tasks, templates, handlers, and variables.

Plays can include other files using import_tasks or include, and rely heavily on variables rendered with Jinja2 ({{ var_name }}) to stay flexible and dynamic.

## What PlayLoader Does
The PlayLoader class is responsible for loading, expanding, and rendering all tasks defined in a list of Ansible plays — including:

- Role-based tasks (roles:)

- Inline tasks (tasks:)

- Nested task imports (import_tasks, include)

- Jinja2-based variable resolution

The end result is a flat, fully-resolved list of tasks ready to be transformed into Kubernetes/OpenShift manifests.


So in a nutshell, it:

- Handles Ansible’s flexible, multi-file structure and variable resolution

- Prepares all task logic in a consistent format before transformation

- Acts as the bridge between Ansible semantics and Kubernetes semantics