# kadet-hub generator template

Start a [Kapitan](https://kapitan.dev/) generator that can be listed on
[kadet-hub](https://kadet-hub.org): **Use this template** on GitHub, then:

1. Rename `example/` to your generator's name and replace `example` in its
   files. The name becomes `ghcr.io/kadet-hub/<name>`.
2. Set `owners` in `kapitan-generator.yaml` to your GitHub user ID
   (`gh api users/<login> --jq .id`), and `tags` from the
   [tag list](https://kadet-hub.org/tags/).
3. Write the generator in `__init__.py`, an inventory example in its
   `README.md`, and fixture targets under `tests/fixtures`. Put the JSON
   Schemas of the resources it emits under `schemas/` with their source in
   `schemas/sources.yaml`.
4. Run `./check <name>`. It runs the marketplace's ruff rules, compiles the
   fixtures in the sandbox image without network, and checks tags and
   schemas, as the gate does (without gVisor and the secret, malware and
   code scans, which the gate adds).
5. Add the version to `CHANGELOG.md`, tag the commit `<name>-v0.1.0`, push,
   and open the entry pull request described in
   [Adding a generator](https://github.com/kadet-hub/registry/blob/main/docs/authors.md).

Working with a coding agent: point it at [AGENTS.md](AGENTS.md).

Before you start, read [when a generator is worth
writing](https://github.com/kadet-hub/registry/blob/main/docs/authors.md#when-a-generator-is-worth-writing).

The template is Apache-2.0; your generator can use any license on the
[marketplace list](https://github.com/kadet-hub/registry/blob/main/policy/licenses.txt).
`example/schemas/core/configmap_v1.json` comes from
[kubernetes-json-schema](https://github.com/yannh/kubernetes-json-schema)
(Apache-2.0).
