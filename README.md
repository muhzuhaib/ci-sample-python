# wordtally

A small command line tool that counts the words in text files and lists the
most common ones. It is a working example of a complete GitHub Actions setup
for a Python project: lint, tests on three Python versions on Linux, Windows and macOS, a built package with
smoke tests and checksums, signed releases with an SBOM and build
provenance, and a signed container image on GitHub Container Registry.

```
pip install wordtally-0.4.0-py3-none-any.whl
wordtally notes.txt --top 3
```

## What runs on GitHub Actions

| Workflow | When | What it does |
| --- | --- | --- |
| `ci.yml` | Every push to `main` and every pull request | Lint and format check (ruff), unit tests on Python 3.12, 3.13 and 3.14, each on Linux, Windows and macOS, build the wheel and source archive, 5 smoke tests on the built wheel in a clean environment, SHA-256 checksums, files kept as a run artifact for 14 days |
| `release.yml` | A version tag such as `v0.4.0`, or by hand with a tag | Runs every check above first. Only when all pass: checks the checksums, makes an SPDX SBOM, signs build provenance and the SBOM, and publishes a GitHub release with the files. Then builds a container image from the checked package, pushes it to `ghcr.io/muhzuhaib/ci-sample-python`, and signs its build provenance and SBOM next to the image |

How to release, check a release and restore one: [RUNBOOK.md](RUNBOOK.md).

## Check a release yourself

```
gh release download v0.4.0 --repo muhzuhaib/ci-sample-python
sha256sum -c SHA256SUMS
gh attestation verify wordtally-0.4.0-py3-none-any.whl --repo muhzuhaib/ci-sample-python
```

Check the container image (signed in to the gh CLI):

```
gh attestation verify oci://ghcr.io/muhzuhaib/ci-sample-python:0.4.0 --repo muhzuhaib/ci-sample-python
docker run --rm ghcr.io/muhzuhaib/ci-sample-python:0.4.0 --version
```

## License

MIT
