# Requirements


In Ansible-based projects, a requirements.yml file is used to declare external roles that your playbook depends on. These roles are typically sourced from remote Git repositories or Ansible Galaxy and help modularize and reuse automation logic across different projects.

When converting an Ansible playbook to an OpenShift deployment using containerize-it, it’s important to fetch and include these roles so that all referenced tasks and variables are available during transformation.

## What Is a requirements.yml?
A requirements.yml file lists the roles your playbook relies on. For example:

```yaml
# requirements.yml
- name: my-role
  src: https://github.com/ajzawawi/ansible-sample-role.git
  version: 3.0.0
```

Each entry typically includes:

`name`: The role name (used for directory structure)

`src`: The Git or Galaxy source

`version (optional)`: A specific tag or branch to check out


## RequirementsResolver

To handle this automatically, containerize-it uses a utility class called RequirementsResolver, the class:

1. Parses the requirements.yml file

2. Clones each required role from its source into the local roles/ directory

3. Ensures those roles are available before transforming the playbook

This makes your transformation self-contained, even if the original playbook depends on external code.