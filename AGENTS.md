# Instructions for coding agents

You are writing a Kapitan generator that will be submitted to the kadet-hub
marketplace. The marketplace gate runs automatically on the submission and
rejects anything that breaks the rules below, so follow them exactly.
Background for humans: [docs/authors.md](https://github.com/kadet-hub/registry/blob/main/docs/authors.md);
machine-readable entry point: <https://kadet-hub.org/llms.txt>.

## Decide first

Write a generator only if it adds knowledge: one inventory block that fans
out into several consistent resources, defaults or conventions, derived
values, or output in several formats. If the inventory would mirror the
output field by field, if an upstream Helm chart already does the job, or if
it is a single resource without defaults, stop and tell the user; a
`jinja2`/`copy`/`helm` input is the right tool then. See
[when not](https://github.com/kadet-hub/registry/blob/main/docs/authors.md#when-not).

## What a generator is

A directory with `__init__.py` defining `main(input_params=None)` that
returns a `kapitan.inputs.kadet.BaseObj`. Kapitan writes every key of
`obj.root` as one output file; a `/` in the key creates a directory. The
generator reads its settings from `inventory().parameters.generators.<name>`.

## Layout (rename `example` everywhere)

```
<name>/
  __init__.py              generator code
  kapitan-generator.yaml   manifest; name must equal <name>
  README.md                must contain a fenced yaml block with "parameters:"
  CHANGELOG.md             must have a "## <version>" heading for every tag
  tests/fixtures/          a Kapitan project; target "minimal" is required
    inventory/targets/*.yml
    inventory/classes/
  schemas/                 JSON Schemas of emitted kinds + sources.yaml
LICENSE                    at the repository root, must match `license`
```

## Hard rules (the gate fails otherwise)

- **Imports**: only the allowlist in
  [policy/imports.txt](https://github.com/kadet-hub/registry/blob/main/policy/imports.txt):
  stdlib modules such as `json`, `re`, `typing`, `copy`, `hashlib`,
  `base64`; `yaml` safe functions; `omegaconf`; `jsonschema`;
  `kapitan.inputs.kadet` (`BaseObj`, `inventory`, ...). No `subprocess`,
  no `os.system`, no network libraries, no `eval`/`exec`/`compile`,
  no dynamic imports.
- **No network, no secrets**: the gate compiles without network and with
  decoy credentials; reading `~/.aws`, `~/.kube`, `~/.ssh` or environment
  tokens fails it. Use Kapitan refs (`?{...}`) for secrets.
- **Programs**: if the generator must start a program (rare), list it in
  `binaries` as `"<program> <subcommand>"`; anything else that runs fails.
- **Output capabilities**: privileged pods, added Linux capabilities, host
  paths or namespaces, cluster-admin RBAC, admission webhooks, Terraform
  provisioners or external data, remote Dockerfile sources must be declared
  in `output_capabilities`, or the gate fails.
- **Determinism**: the same inventory must give the same output, also with
  `CI=true` set. No timestamps, random values or environment lookups.
- **Tags** from [the tag list](https://kadet-hub.org/tags/); `kubernetes`
  needs documents with `apiVersion` and `kind` in the output, `helm` a chart
  or `helm template`, `terraform` `*.tf.json` output.
- **Schemas**: for every apiVersion/kind you emit, put its JSON Schema at
  `schemas/<group>/<kind lowercase>_<version>.json` (`core` for `v1`) and add
  the group to `schemas/sources.yaml` with `software`, `version`, `source`
  (a pinned upstream URL) and `license`. Take core schemas from
  [kubernetes-json-schema](https://github.com/yannh/kubernetes-json-schema)
  `vX.Y.Z-standalone-strict`, CRD schemas from the operator's CRDs at a
  release tag. Never invent a schema.
- **Code quality**: `ruff check` with the marketplace's rules (syntax
  errors and pyflakes); `# noqa` is ignored. No symlinks, no executable
  files, no file above 1 MiB, no `.gitattributes`.
- **Fixtures**: each target sets `parameters.kapitan.vars.target` to its file
  name and compiles `input_paths: [lib/<name>]`, where the gate places the
  generator. Every target must produce at least one file. Cover the main
  options in a second target (`complete.yml`).

## Workflow

1. Implement, then run `./check <name>` until it passes. Fix the cause of a
   finding; do not suppress it.
2. Update `README.md` with a realistic inventory example and a table of
   inputs and output files.
3. Bump the version in `CHANGELOG.md`, commit, tag `<name>-v<semver>`.
4. The entry pull request in kadet-hub/registry is opened by a human owner
   (`generators/<name>.yaml` with repo, path, tag, sha and owners). Prepare
   its content, but leave opening it to the owner, who accepts the
   [terms of listing](https://github.com/kadet-hub/registry/blob/main/TERMS.md).
