# Changelog — pycleancode

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-07-13

### Output Teams Can Use

- Added the unified `pycleancode` CLI with a `check` subcommand: `pycleancode check src --format json --output report.json`.
- Deprecated `pycleancode-brace-linter`. It keeps working with its existing arguments, prints a one-line notice on stderr, and is planned for removal in 2.0.
- Added JSON output (`--format json`, stable `schemaVersion: 1` with per-file summaries) and Markdown output (`--format markdown`) suitable for pull-request summaries; both support `--output <file>`.
- Added severity-aware exit codes: `0` clean or warnings-only, `1` at least one error-severity violation, `2` usage/config/parse/write failure.
- Added per-rule `severity: error | warning` configuration so teams can adopt rules without failing builds, then tighten over time.
- Added layered configuration discovery: `--config <path>`, then `./pybrace.yml`, then `[tool.pycleancode]` in `./pyproject.toml`, then built-in defaults. Running without any config file now works instead of crashing.
- Added configuration validation with clear errors for invalid severity values, non-integer thresholds, non-boolean `enabled`, and malformed TOML.
- Restructured the analyzer to return structured results (`AnalysisRun`) with rendering moved to a dedicated formatter layer; unparseable files are reported and no longer abort the run.
- Removed the unused `ParserEngine` and legacy `reporter` package; rule-registry tests no longer write into the production package.
- Added `tomli` as a dependency for Python 3.9/3.10 (`tomllib` is used on 3.11+).

---

## [1.0.4] - 2026-06-08

### Security Hardening

- Raised vulnerable runtime and development dependency constraints.
- Replaced the scheduled Safety export flow with `pip-audit` and Bandit checks.
- Pinned GitHub Actions to immutable commit SHAs.
- Added PyPI release tag validation and an environment gate for trusted publishing.
- Escaped control characters before writing untrusted paths to the console.
- Added a minimal MkDocs configuration so the documentation workflow has a real site to build.
- Committed a Poetry lockfile for reproducible CI and release installs.

---

## [1.0.3] - 2026-06-08

### Trust-Repair Release

- Fixed rule loading so YAML thresholds are passed to enabled rule constructors.
- Preserved strict config loading behavior with passing regression coverage.
- Aligned README release metadata with package behavior and Python version support.
- Added regression coverage proving `max_depth` configuration changes rule output.

---

## [1.0.0] - 2025-06-16

### 🚀 First Official OSS Release — pycleancode

- ✅ Project fully migrated to unified `pycleancode` multi-module OSS architecture.
- ✅ Initial module: `brace_linter` — Structural Depth Analyzer.
- ✅ Supports deep AST parsing using `libcst` with full metadata extraction.
- ✅ Implements Virtual Brace Tree (VBT) model for structural analysis.
- ✅ Added Max Depth Rule (logical nesting depth check).
- ✅ Added Nested Function Rule (function-in-function depth control).
- ✅ Full configuration via `pybrace.yml` for rule thresholds.
- ✅ Fully functional CLI powered by Typer with entry point: `pycleancode-brace-linter`.
- ✅ Advanced visual reporting:
  - Emoji-based tree rendering
  - ASCII structure output
  - Summary charts for quick glance depth reports.
- ✅ Fully frozen reproducible `pyproject.toml`.
- ✅ 100% test coverage (unit + integration).
- ✅ Pre-commit hooks: Black, Ruff, MyPy, Isort.
- ✅ GitHub Actions CI/CD fully integrated.
- ✅ Full security policy, contributing guidelines, commit conventions, and release workflows.
- ✅ PyPI-publishable build pipeline added (`release.yml`).

---

## [0.1.0] - 2024-06-11

### Initial private scaffold (pre-OSS)

- Initial Phase 1 scaffold
- Implemented libcst-based parser with metadata extraction
- Built Virtual Brace Tree (VBT) model
- Implemented max depth rule
- Integrated configuration via YAML
- Created CLI interface via Typer
- Fully pinned dependencies for reproducibility
- Established OSS-grade project structure and contribution guidelines

---
