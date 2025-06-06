
# Contexts
Context objects are used to carry shared state, configuration and metadata across different transformation stages. They help decouple logic between parsing, transformation and rendering phases while ensuring consistency and flexibility.

Each context serves a distinct purpose and is designed to evolve independently as new use cases (e.g., Helm templating, multi-role parsing) are added.

## Context Types
| Context Class        | Purpose                                                                                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `VarContext`         | Gathers and resolves variables from all Ansible-like scopes (`vars`, `defaults`, `role vars`, etc.). Provides variable interpolation and Jinja2 evaluation.           |
| `ConfigMountContext` | Collects all `copy`/`template`-like tasks that result in mounted files/configs, and tracks configMap names and mount paths. Used when generating `volumes` and `volumeMounts`. |
| `TransformContext` | Encapsulates transformation-level parameters like app name, image, replica count, and target output format (e.g. raw YAML vs Helm). Enables conditional template logic and value injection. |

## Context Use Cases

| Use Case                                            | `VarContext` | `ConfigMountContext` | `TransformContext` |
| --------------------------------------------------- | ------------ | -------------------- | ------------------ |
| Resolving `{{ my_var }}` in a template              | ✅            | ❌                    | ❌                  |
| Tracking `copy` targets and generating `ConfigMaps` | ❌            | ✅                    | ❌                  |
| Injecting `.Values.image` in Helm mode              | ❌            | ❌                    | ✅                  |
| Deciding whether to write K8s or Helm YAML          | ❌            | ❌                    | ✅                  |
| Tracking files to mount and where                   | ❌            | ✅                    | ❌                  |

