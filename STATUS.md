## Supported Features

[x] Load variables from `group_vars/`, `host_vars/`, `roles/*/defaults/`, and `roles/*/vars/`

[x] Apply basic variable precedence: `defaults < group_vars/host_vars < role vars`

[x] Recursively interpolate variables with `{{ ... }}`

[x] Support block-level Jinja syntax (e.g., `{% for user in users %} ... {% endfor %}`)

[x] Support inline Jinja expressions with filters (e.g., `{{ users | map(attribute='name') | list }}`)

[x] Parse rendered output using YAML to support lists and dictionaries

[x] Allow skipping specific files (used in tests to isolate behavior)

[x] Test framework with realistic test projects and reusable test patterns

[x] Multi-pass interpolation with max depth limit

[x] Jinja2 environment with built-in filters

## TODO

### Enhancements

[ ] Enforce strict precedence application across file types even when keys overlap

[ ] Detect and warn on circular references

[ ] Track unresolved variables after interpolation

[ ] Preserve original values along with resolved ones (for debug and traceability)

### Ansible Compatibility

[x] Add support for Ansible-specific filters:

    [x] dict2items	- Converts a dict to a list of key-value pairs

    [x] items2dict	- Converts a list of key-value pairs to a dict

    [x] combine	 - Merges dictionaries

    [x] flatten	- Flattens nested lists

    [x] unique	- Removes duplicate list items

    [x] difference	- Returns list items not in another list

    [x] intersect	- Returns common items

    [x] union	- Merges two lists

    [x] selectattr, rejectattr - Filter a list of dicts based on attributes
    
    [x] map, select, reject - Jinja standard filters extended in Ansible

[x] Import and register Ansible’s full Jinja filter set

[x] Import external roles using both formats for requirements.yml file

[ ] Support `.j2` variable files or templated var files

[ ] Support `vars/main.yml` in other relevant Ansible folders (e.g., `tasks/`, `handlers/`)

### Output Compatability

[ ] Helm
    [x] Render 1 chart 
    [] Render 1 parent chart with subcharts
[x] Raw k8s


### Test Coverage

[ ] Add test for precedence enforcement across all scopes

[ ] Add test for circular reference resolution edge case

[ ] Add test for deeply nested list/dict interpolation

[ ] Add test for unsupported or malformed Jinja expressions

### Dev Quality

[ ] Set up `black`, `isort`, and `ruff` for linting and formatting

[ ] Add `pytest-cov` for code coverage reporting

[ ] Auto-generate documentation of supported filters, resolution rules, and file precedence
