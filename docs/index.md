# pycleancode

`pycleancode` is a Python toolkit for clean-code-focused static analysis.

The current package includes `brace_linter`, a structural analyzer for Python
code depth and nested functions. Use the repository README for installation,
configuration, contribution, and release details.

## Quick Start

```bash
pip install pycleancode
pycleancode-brace-linter path/to/code.py --config pybrace.yml --report
```

## Configuration

```yaml
rules:
  max_depth:
    enabled: true
    max_depth: 3
  nested_function:
    enabled: true
    max_nested: 1
```

## Project Links

- Repository: https://github.com/pycleancode/pycleancode
- PyPI: https://pypi.org/project/pycleancode/
