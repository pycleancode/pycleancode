![pycleancode logo](assets/readme/pycleancode-logo.png)
# Pycleancode: Professional Python Clean Code Toolkit

> **A Python toolkit to help developers write professional-grade, maintainable, and clean code following clean code principles.**

[![PyPI version](https://img.shields.io/pypi/v/pycleancode)](https://pypi.org/project/pycleancode/)
[![Python versions](https://img.shields.io/pypi/pyversions/pycleancode)](https://pypi.org/project/pycleancode/)
[![Wheel](https://img.shields.io/pypi/wheel/pycleancode)](https://pypi.org/project/pycleancode/)
[![License](https://img.shields.io/github/license/pycleancode/pycleancode)](LICENSE)

[![CI](https://github.com/pycleancode/pycleancode/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/pycleancode/pycleancode/actions/workflows/ci.yml)
[![Build Docs](https://github.com/pycleancode/pycleancode/actions/workflows/docs.yml/badge.svg?branch=main)](https://github.com/pycleancode/pycleancode/actions/workflows/docs.yml)
[![Security Scan](https://github.com/pycleancode/pycleancode/actions/workflows/security-scan.yml/badge.svg)](https://github.com/pycleancode/pycleancode/actions/workflows/security-scan.yml)
[![Release](https://github.com/pycleancode/pycleancode/actions/workflows/workflow.yml/badge.svg)](https://github.com/pycleancode/pycleancode/actions/workflows/workflow.yml)

[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: Ruff](https://img.shields.io/badge/linting-ruff-46A4A4.svg)](https://docs.astral.sh/ruff/)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)

---

**pycleancode** is a professional-grade Python toolkit that helps developers write clean, maintainable, and scalable code following clean code principles.

## 🌍 Project Goal

> Build multiple code quality tools under a single unified package architecture.

Unlike traditional linters that only focus on style violations, `pycleancode` implements advanced rule engines that target deeper structural and maintainability aspects of your code.

---

## 🔄 Why pycleancode?

While tools like `flake8`, `pylint`, `ruff`, and `black` are excellent, most focus heavily on surface-level syntax or style violations.

**pycleancode** is different:

* 🔄 Designed for professional teams writing critical Python codebases.
* 🤝 Rule-based pluggable architecture to extend new structural checks.
* 🔄 AST-powered deep nesting detection.
* 🎡 Focused on long-term maintainability.
* 🦖 OSS-grade code architecture.

---

## 🔄 Current Release - v1.1.0

**pycleancode 1.1.0** — "Output teams can use" — adds a unified `pycleancode check` CLI, JSON and Markdown reports, severity-aware exit codes for CI, and `pyproject.toml` configuration on top of the `brace_linter` module.

### New in 1.1.0

* **Unified CLI** — `pycleancode check <path>` replaces `pycleancode-brace-linter` (the old command still works and prints a deprecation notice; removal planned for 2.0).
* **Report formats** — `--format text|json|markdown` with optional `--output <file>`. JSON carries a stable `schemaVersion: 1` for CI integrations; Markdown is ready to paste into a pull request.
* **Exit codes for CI** — `0` clean or warnings-only, `1` error violations, `2` usage/config/parse failure. Builds can finally fail on maintainability regressions.
* **Per-rule severity** — set `severity: warning` on a rule to report without failing the build, then tighten to `error` when the team is ready.
* **Layered configuration** — `--config <path>` → `./pybrace.yml` → `[tool.pycleancode]` in `pyproject.toml` → built-in defaults. Fresh installs run with zero setup.

### Brace Linter

The `brace_linter` module focuses on structural code depth and complexity. It analyzes Python code for excessive nesting and deeply nested functions that often make code harder to read, maintain, and extend.

### Key Features

* **Max Depth Rule**

  * Enforces maximum logical nesting depth.
  * Helps prevent pyramid-of-doom structures.

* **Nested Function Rule**

  * Enforces maximum levels of nested function definitions.
  * Prevents excessive local function scoping that can reduce readability.

* **Structural Reporting**

  * Full structural report of nesting tree.
  * Emoji + ASCII visualization of code structure.
  * Summary chart output for quick depth evaluation.

### Sample output:

```bash
sandbox/test_sample.py:2: Nested functions depth 2 exceeds allowed 1
sandbox/test_sample.py:3: Depth 4 exceeds max 3

📈 Structural Report:

 🔾 ROOT (Line 0, Depth 1)
│ 🔹 FunctionDef (Line 1, Depth 2)
│ │ 🔹 FunctionDef (Line 2, Depth 3)
│ │ │ 🔹 FunctionDef (Line 3, Depth 4)
```

---

## 🛡 Python Compatibility

- ✅ Supported Python versions: 3.9, 3.10, 3.11, 3.12
- ⚠ Python 3.13+ is not yet supported (due to upstream Rust dependencies)

## 🌐 Installation

Install via PyPI:

```bash
pip install pycleancode
```

Or using Poetry:

```bash
poetry add pycleancode
```

---

## 🔧 Basic Usage

Run directly via CLI:

```bash
pycleancode check path/to/your/code.py --report
```

Generate machine-readable or review-friendly reports:

```bash
pycleancode check src --format json --output report.json
pycleancode check src --format markdown --output report.md
```

Exit codes: `0` = clean or warnings-only · `1` = error-severity violations · `2` = usage/config/parse failure.

> The legacy `pycleancode-brace-linter` command still works with its original arguments and prints a deprecation notice. Migrate scripts to `pycleancode check`.

---

## 🏓 Configuration

Configuration is discovered in this order: `--config <path>` → `./pybrace.yml` → `[tool.pycleancode]` in `pyproject.toml` → built-in defaults.

Via `pybrace.yml`:

```yaml
rules:
  max_depth:
    enabled: true
    max_depth: 3
  nested_function:
    enabled: true
    max_nested: 1
    severity: warning   # report, but do not fail the build
```

Or via `pyproject.toml`:

```toml
[tool.pycleancode.rules.max_depth]
enabled = true
max_depth = 3

[tool.pycleancode.rules.nested_function]
enabled = true
max_nested = 1
severity = "warning"
```

Each rule accepts `enabled`, its thresholds, and an optional `severity` (`error` by default, `warning` to report without failing CI).

---

## 🔧 Development Setup

```bash
git clone git@github.com:YOUR_USERNAME/pycleancode.git
cd pycleancode
poetry install
pre-commit install
```

Run full tests:

```bash
poetry run pytest --cov=pycleancode --cov-report=term-missing
```

Run pre-commit:

```bash
poetry run pre-commit run --all-files
```

---

## 📖 Roadmap

| Module / Feature         | Description                                        | Status      |
| ------------------------ | -------------------------------------------------- | ----------- |
| `brace_linter`           | Structural depth analysis (nesting, functions)     | ✅ Completed |
| Team-usable output       | JSON/Markdown reports, exit codes, pyproject config | ✅ v1.1.0   |
| Regression diff mode     | `diff --base main`: fail CI only on regressions     | ⏳ Planned (v1.2) |
| Baseline & ratchet       | Adopt on legacy codebases without fixing old debt   | ⏳ Planned (v1.3) |
| GitHub Action            | PR comments, status checks, annotations             | ⏳ Planned (v1.4) |
| Full documentation site  | OSS-grade docs & API reference                      | ✅ Live      |

---

## 🔒 License

Released under the MIT License. See [LICENSE](LICENSE).

---

## 🛡️ Code of Conduct

Please see our [CODE\_OF\_CONDUCT.md](CODE_OF_CONDUCT.md)

---

## 🔗 Contributing

We welcome OSS contributions. Please read our full [CONTRIBUTING.md](CONTRIBUTING.md) to get started!

* Clean Code Principles
* 100% Test Coverage Required
* Pre-commit Hooks Required
* Conventional Commits Required

---

## 🔔 Community

* GitHub Discussions (coming soon)
* Issues and PRs welcomed
* PyPI release v1.1.0 adds team-usable output: reports, exit codes, and pyproject configuration

---

🚀 **Pycleancode: Clean Code. Professional Quality. OSS-Grade Python. Unified Modular Clean Code Toolkit.**
