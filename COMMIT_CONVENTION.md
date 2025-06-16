
---

### `COMMIT_CONVENTION.md`

```markdown
# Commit Message Convention — pycleancode

We follow the Conventional Commits v1.0.0 standard.

## Format

<type>(scope): short description

## Types

- feat — new feature
- fix — bug fix
- refactor — code refactor (no behavior change)
- docs — documentation
- test — unit or integration tests
- build — build system or dependency updates
- chore — non-functional cleanup
- perf — performance improvements
- ci — CI/CD pipeline updates

## Scopes

- parser
- vbtree
- rules
- cli
- config
- core
- filesystem
- reporter
- engine
- deps

## Examples

feat(parser): add libcst metadata parsing

fix(vbtree): handle nested function definitions properly

refactor(core): decouple rule engine interface

---

✅ Following these conventions allows us to automatically generate changelogs and release notes.
