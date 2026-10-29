# kadet-hub generator template

Start a [Kapitan](https://kapitan.dev/) generator that can be listed on
[kadet-hub](https://kadet-hub.org): **Use this template** on GitHub, then:

1. Rename `example/` to your generator's name and replace `example` in its
   files. The name becomes `ghcr.io/kadet-hub/<name>`.
2. Set `owners` in `kapitan-generator.yaml` to your GitHub user ID
   (`gh api users/<login> --jq .id`), and `tags` from the
   [tag list](https://kadet-hub.org/tags/). Turn on private vulnerability
   reporting with `gh api -X PUT repos/<owner>/<repo>/private-vulnerability-reporting`:
   [SECURITY.md](SECURITY.md) sends reports there, and a repository made
   from a template does not inherit the setting.
3. Write the generator in `__init__.py`, an inventory example in its
   `README.md`, and fixture targets under `tests/fixtures`. Put the JSON
   Schemas of the resources it emits under `schemas/` with their source in
   `schemas/sources.yaml`.
4. Run `./check <name>` on Linux x86-64 with docker, uv and yq. It runs the
   gate's static scan (tree and import checks, gitleaks, semgrep, ruff,
   GuardDog, ClamAV) with the scanner versions the gate pins, compiles the
   fixtures in the sandbox image without network, and checks tags and
   schemas, as the gate does. Only the gate judges the gVisor syscall trace
   and applies exceptions. ClamAV runs as in the gate, because the gate's
   scan script runs it unconditionally: the first run pulls the clamav image
   (about 390 MB), and each run updates its signatures or warns and scans
   with the shipped ones.
5. Add the version to `CHANGELOG.md`, tag the commit `<name>-v0.1.0`, push,
   and open the entry pull request described in
   [Adding a generator](https://github.com/kadet-hub/registry/blob/main/docs/authors.md).

For a generator of an operator's custom resources, `./scaffold <name>
<crd-url>...` does step 1 and starts step 3. Each URL is a CRD file at a
release tag: a GitHub blob or raw URL, or any https URL with the tag in its
path, such as a release asset. It creates `<name>/` like `example/`: the
JSON Schemas and CRD files under `schemas/`, written as `tools/upstream.py`
in kadet-hub/generators writes them, a generator that renders one resource
per inventory entry with its `spec` passed through, and a `minimal` fixture
whose required fields take the CRD's defaults or first enum values, or
placeholders that it lists. It asks for each API group's software and
licence, the generator's licence and tags, and the kinds to take from a file
with several CRDs. It needs uv and network, and reads
`example/kapitan-generator.yaml`, so keep `example/` until you have run it.

Working with a coding agent: point it at [AGENTS.md](AGENTS.md).

Before you start, read [when a generator is worth
writing](https://github.com/kadet-hub/registry/blob/main/docs/authors.md#when-a-generator-is-worth-writing).

The template is Apache-2.0; your generator can use any license on the
[marketplace list](https://github.com/kadet-hub/registry/blob/main/policy/licenses.txt).
`example/schemas/core/configmap_v1.json` comes from
[kubernetes-json-schema](https://github.com/yannh/kubernetes-json-schema)
(Apache-2.0).
