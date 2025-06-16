# Contributing to pycleancode

Thank you for considering contributing to `pycleancode`!  
This project follows strict OSS engineering and clean code principles to ensure long-term scalability, maintainability, and correctness.

---

## 🚀 Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
    ```bash
    git clone git@github.com:your-username/pycleancode.git
    ```
3. **Create a feature branch**:
    ```bash
    git checkout -b feature/your-feature-name
    ```
4. **Set up the environment**:
    ```bash
    poetry install
    pre-commit install
    ```
5. **Write your code following the standards below.**
6. **Run full tests and linters locally**.
7. **Push your branch** and open a Pull Request (PR).

---

## 📦 Code Standards

- Python version: **3.11+** (locked via Poetry & pyenv)
- Type annotations: **mandatory** everywhere.
- Code formatters:
    - `black`
    - `ruff`
    - `mypy`
- Run full pre-commit checks before submitting:
    ```bash
    poetry run pre-commit run --all-files
    ```
- Follow **Clean Code** principles:
  - SOLID
  - SRP (Single Responsibility Principle)
  - OOP where applicable
  - Fully documented functions & classes
- Public API must not introduce breaking changes without prior discussion via issue or RFC.

---

## 🧪 Testing

- Run full tests locally before submitting a PR:

```bash
poetry run pytest --cov=pycleancode --cov-report=term-missing
