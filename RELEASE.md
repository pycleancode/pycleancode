# 🚀 Release Process — pycleancode

We follow **Semantic Versioning (semver.org)** to ensure safe, predictable OSS releases.

---

## 📦 Version Format

```
MAJOR.MINOR.PATCH
```

| Segment   | Meaning                                       |
| --------- | --------------------------------------------- |
| **MAJOR** | Incompatible API changes (breaking changes)   |
| **MINOR** | New features (backward-compatible)            |
| **PATCH** | Bug fixes, maintenance, or small improvements |

---

## ✅ Release Checklist

Before publishing a release:

* [ ] All tests pass locally:

  ```bash
  poetry run pytest --cov=pycleancode --cov-report=term-missing
  ```
* [ ] All pre-commit checks pass:

  ```bash
  poetry run pre-commit run --all-files
  ```
* [ ] Security checks pass:

  ```bash
  poetry run pip-audit
  poetry run bandit -r pycleancode
  ```
* [ ] All CI pipelines (GitHub Actions) pass.
* [ ] Dependencies fully frozen via `poetry.lock`:

  ```bash
  poetry lock --no-update
  ```
* [ ] Update version in `pyproject.toml`:

  ```toml
  [tool.poetry]
  version = "X.Y.Z"
  ```
* [ ] Update `CHANGELOG.md`:

  * Document changes clearly under appropriate version section.
  * Use `Conventional Commits` messages to auto-generate changelog where possible.
* [ ] Verify documentation is up to date (`README.md`, `docs/`).
* [ ] Push final code to `main` branch.
* [ ] Create GitHub Release with full release notes.
* [ ] Publish to PyPI:

  ```bash
  poetry build
  poetry publish
  ```

---

## ✅ Release Automation

The `Release` GitHub Actions workflow runs on version tags matching `v*.*.*`.
It validates that the tag matches the version in `pyproject.toml`, builds the
package, publishes to PyPI through trusted publishing, and creates or updates
the matching GitHub Release with built `dist/*` assets.

To publish a new release:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

To backfill a GitHub Release for an existing tag without republishing to PyPI,
run the `Release` workflow manually with:

* `tag`: existing tag, for example `v1.0.4`
* `publish_to_pypi`: `false`

Version bumps, changelog generation, and release-note copy are still maintained
manually.

---

## 🔒 Release Stability Commitment

* Releases only ship when 100% test coverage is preserved.
* No breaking changes allowed in PATCH or MINOR releases.
* Every MAJOR release will have full migration documentation.

---

✅ OSS Quality. ✅ Predictable Releases. ✅ Professional Engineering.
