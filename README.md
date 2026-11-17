# wordtally

A small command line tool that counts the words in text files and lists the
most common ones. It is a working example of a complete GitHub Actions setup
for a Python project: lint, tests on two Python versions, a built package with
smoke tests and checksums, and signed releases with an SBOM and build
provenance.

```
pip install wordtally-0.1.0-py3-none-any.whl
wordtally notes.txt --top 3
```

## What runs on GitHub Actions

| Workflow | When | What it does |
| --- | --- | --- |
| `ci.yml` | Every push to `main` and every pull request | Lint and format check (ruff), unit tests on Python 3.12 and 3.13, build the wheel and source archive, 5 smoke tests on the built wheel in a clean environment, SHA-256 checksums, files kept as a run artifact for 14 days |
| `release.yml` | A version tag such as `v0.1.0`, or by hand with a tag | Runs every check above first. Only when all pass: checks the checksums, makes an SPDX SBOM, signs build provenance and the SBOM, and publishes a GitHub release with the files |

How to release, check a release and restore one: [RUNBOOK.md](RUNBOOK.md).

## Check a release yourself

```
gh release download v0.1.0 --repo muhzuhaib/ci-sample-python
sha256sum -c SHA256SUMS
gh attestation verify wordtally-0.1.0-py3-none-any.whl --repo muhzuhaib/ci-sample-python
```

## License

MIT
