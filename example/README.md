# example

Renders one ConfigMap per entry under `parameters.generators.example`.
Replace this text with what your generator renders and why someone would
use it; the kadet-hub catalog shows this README on the generator's page.

## Usage

```yaml
parameters:
  kapitan:
    dependencies:
      - type: oci
        source: ghcr.io/kadet-hub/example@sha256:<digest>
        output_path: lib/example
    compile:
      - input_type: kadet
        input_paths:
          - lib/example
        output_path: manifests/
  generators:
    example:
      namespace: demo            # default: parameters.namespace, then "default"
      configmaps:
        settings:
          labels:
            team: platform
          data:
            LOG_LEVEL: info
```

## Output

| Input | Kind | File |
|---|---|---|
| `configmaps.<name>` | ConfigMap | `<namespace>/<name>-cm.yaml` |

Every resource carries `app.kubernetes.io/name` and
`app.kubernetes.io/managed-by: kapitan`; `labels` adds to them.
