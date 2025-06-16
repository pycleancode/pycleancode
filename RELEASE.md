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

## ✅ Release Automation (Planned)

In future versions:

* Full **semantic-release** automation pipelines will handle:

  * Automated version bumping.
  * Automated changelog generation.
  * Automated PyPI publishing.
  * Automated GitHub Releases.
* Auto-triggered on `main` protected branch merges.
* Safe for external OSS contributor PRs.

---

## 🔒 Release Stability Commitment

* Releases only ship when 100% test coverage is preserved.
* No breaking changes allowed in PATCH or MINOR releases.
* Every MAJOR release will have full migration documentation.

---

✅ OSS Quality. ✅ Predictable Releases. ✅ Professional Engineering.
