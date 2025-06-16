# Changelog — pycleancode

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
