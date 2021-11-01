# OpenWasteMap

## Development Setup

1. Install [poetry](https://github.com/python-poetry/poetry)
   ```bash
   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
   ```
1. Install the dependencies
   ```bash
   poetry install
   ```
1. Install the [pre-commit](https://github.com/pre-commit/pre-commit) and pre-push hooks
   ```bash
   pre-commit install
   pre-commit install -t push
   ```