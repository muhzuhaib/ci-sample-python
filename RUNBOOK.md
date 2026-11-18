# Runbook: wordtally on GitHub Actions

This is how the checks and releases of this repository work, what to do when
something goes red, and how to restore a release. Everything runs on GitHub
Actions with free actions; nothing here needs a paid plan for a public
repository.

## 1. What runs, and when

| Workflow | Starts on | Jobs |
| --- | --- | --- |
| `.github/workflows/ci.yml` | every push to `main`, every pull request | `lint` (ruff check and ruff format --check), `test` (pytest on Python 3.12, 3.13 and 3.14, each on Linux, Windows and macOS), `build` (python -m build, 5 smoke tests on the wheel in a clean environment, SHA256SUMS, run artifact kept 14 days) |
| `.github/workflows/release.yml` | a tag starting with `v`, or by hand with a tag | `checks` (all of `ci.yml`), then `release` and `image`, then `sign-image` on public repositories |

The `release` job has `needs: checks`. If any lint, test or smoke test fails,
GitHub skips `build`, `release` and `image`, and nothing is published.

The `image` job builds a container image from the checked package (see `Dockerfile`), runs it once,
and pushes it to GitHub Container Registry as `ghcr.io/muhzuhaib/ci-sample-python:<version>` with the built-in
token. On public repositories `sign-image` then signs its build provenance and its SBOM, stores both
next to the image, pulls the image by digest and checks both signatures.

Security settings in both files:

- `permissions: contents: read` at the top. Only the `release` job gets write
  access to the code and releases (`contents`, `id-token`, `attestations`, `artifact-metadata`).
  The `image` job may write packages only. `sign-image` may write packages, `id-token` and
  `attestations`, and installs and builds nothing.
- Every action is pinned to a full commit SHA, with the version in a comment.
- `actions/checkout` runs with `persist-credentials: false`.
- No secrets are used. The release job uses the built-in `GITHUB_TOKEN`.
- Every job has a `timeout-minutes` limit.
- The release job installs nothing. The SBOM is made in the read-only
  `build` job, and the token that writes the release is set only on the
  publish step.

Caching: `actions/setup-python` caches pip downloads, keyed on `requirements-ci.txt` and `pyproject.toml`. The run log shows `Cache restored from key: ...` when it is used.

## 2. Make a release

1. Set the new version in `pyproject.toml` and merge it to `main`.
2. Wait for CI on `main` to be green.
3. Tag and push:

```
git tag -a v0.4.0 -m "wordtally 0.4.0"
git push origin v0.4.0
```

The release page then holds the wheel, the source archive, `SHA256SUMS` and `sbom.spdx.json`, and
`ghcr.io/muhzuhaib/ci-sample-python:0.4.0` holds the container image.

## 3. When a check goes red

1. Open the run: `gh run list --limit 5`, then `gh run view <id> --log-failed`.
2. Fix the cause on a branch and open a pull request; CI runs on it.
3. If a version tag was already pushed, nothing was published. Push a new
   tag (for example `v0.4.1`) once the fix is on `main`.

Proof this repository blocks a release on a failing test: tag `v0.4.0-rc.1`
on branch `drill/red-test-4`. Its release run failed in `test` and skipped
`build` and `release`, and no release exists for that tag.

## 4. Check a release

```
gh release download v0.4.0 --repo muhzuhaib/ci-sample-python
sha256sum -c SHA256SUMS
gh attestation verify wordtally-0.4.0-py3-none-any.whl --repo muhzuhaib/ci-sample-python
gh attestation verify wordtally-0.4.0-py3-none-any.whl --repo muhzuhaib/ci-sample-python --predicate-type https://spdx.dev/Document/v2.3
```

`sha256sum -c` shows `OK` for each file. Each `gh attestation verify` ends
with `Verification succeeded!`: the first checks the build provenance, the
second checks that the SBOM was signed for that exact file.

The container image:

```
gh attestation verify oci://ghcr.io/muhzuhaib/ci-sample-python:0.4.0 --repo muhzuhaib/ci-sample-python
gh attestation verify oci://ghcr.io/muhzuhaib/ci-sample-python:0.4.0 --repo muhzuhaib/ci-sample-python --predicate-type https://spdx.dev/Document/v2.3
```

## 5. Recovery drill: restore a release

Use this when a release file is lost, damaged or replaced by mistake.

1. Confirm the damage: `sha256sum -c SHA256SUMS` shows `FAILED`, or
   `gh attestation verify` finds no attestation for the file.
2. Rebuild that release from its tag:

```
gh workflow run release.yml -f tag=v0.4.0
gh run watch
```

3. The run checks out the tag, runs every check again, builds, signs and
   replaces the files on the existing release (`Release v0.4.0 exists:
   replacing its files (recovery)` in the log).
4. Check it again with section 4. The rebuilt files have new checksums and
   new signatures, made by the release workflow on `main`.

## 6. Upkeep

- Pinned actions: once a month, check each action's latest release and
  replace the SHA and the version comment together. Change one action at a
  time and let CI run.
- Runtime versions: when a new Python version becomes current, add it to
  the `matrix` in `ci.yml` and drop the oldest one.
- Private repositories: the checks, SBOM, checksums and releases work the
  same, and the two signing steps are skipped there (they run only on public
  repositories). The kit signs releases on public repositories only. Run time in
  private repositories counts against the monthly minutes of your GitHub plan, and Windows and
  macOS runs use those minutes faster than Linux runs.
- To stop a pull request from being merged while CI is red, turn on a branch
  rule for `main` in Settings and pick the `lint`, `build` and each `test` check
  (for example `test (3.12, ubuntu-latest)`) as required. Branch rules are free on public repositories; on a private
  repository they need GitHub Pro, Team or Enterprise.
