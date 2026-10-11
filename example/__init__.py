"""Example generator: one ConfigMap per entry under parameters.generators.example.

Replace the body of main() with your generator. Keep to the import
allowlist of the kadet-hub gate (policy/imports.txt in kadet-hub/registry).
"""

from kapitan.inputs.kadet import BaseObj, inventory


def main(input_params=None):
    params = inventory().parameters
    config = params.get("generators", {}).get("example", {})
    namespace = config.get("namespace", params.get("namespace", "default"))
    out = BaseObj()
    for name in sorted(config.get("configmaps", {})):
        spec = config["configmaps"][name]
        labels = {"app.kubernetes.io/name": name, "app.kubernetes.io/managed-by": "kapitan"}
        labels.update({str(k): str(v) for k, v in spec.get("labels", {}).items()})
        out.root[f"{namespace}/{name}-cm"] = {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {"name": name, "namespace": namespace, "labels": labels},
            "data": {str(k): str(v) for k, v in spec.get("data", {}).items()},
        }
    return out
