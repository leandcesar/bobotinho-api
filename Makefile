
NAME = app
VENV = venv
BIN = $(VENV)/bin
PYTHON = $(BIN)/python3.9
PIP = $(BIN)/pip

.PHONY = help install version format lint run test clean uninstall
.DEFAULT_GOAL = help

$(BIN)/activate: requirements.txt requirements-dev.txt
	@python3.9 -m venv $(VENV)
	@$(PIP) install -U pip
	@$(PIP) install -r requirements-dev.txt

.PHONY: help
help:  ## ❓ Show the help.
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make \033[36m<command>\033[36m\033[0m\nCommands:\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: install
install: $(BIN)/activate  ## ⬇️  Install the virtual env project in dev mode.

.PHONY: version
version: $(BIN)/activate  ## 🔢 Show the current environment.
	@$(PYTHON) --version
	@$(PIP) --version
	@$(PIP) freeze

.PHONY: format
format: $(BIN)/activate  ## ✍  Format code.
	@$(BIN)/isort ${NAME}/
	@$(BIN)/brunette ${NAME}/ --config=setup.cfg

.PHONY: lint
lint: $(BIN)/activate  ## 🔎 Lint code.
	@$(BIN)/mypy ${NAME}/ --config-file setup.cfg
	@$(BIN)/brunette ${NAME}/ --config=setup.cfg --check
	@$(BIN)/flake8 ${NAME}/ --config=setup.cfg --count --show-source --statistics --benchmark
	@$(BIN)/interrogate ${NAME}/ --config=setup.cfg
	@$(BIN)/vulture ${NAME}/ --ignore-names on_* --min-confidence 80

.PHONY: run
run: $(BIN)/activate  ## 🏃 Run the project in development mode.
	@. $(BIN)/activate & sh ./run.sh

.PHONY: test
test: $(BIN)/activate  ## 🧪 Run tests and generate coverage report.
	@$(BIN)/pytest -vv --cov=${NAME}/ -l --tb=short --maxfail=1

.PHONY: clean
clean:  ## 🧹 Clean unused files.
	@$(PYTHON) -Bc "for p in __import__('pathlib').Path('.').rglob('*.py[co]'): p.unlink()"
	@$(PYTHON) -Bc "for p in __import__('pathlib').Path('.').rglob('__pycache__'): p.rmdir()"
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .coverage
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

.PHONY: uninstall
uninstall:  ## 🗑️  Uninstall the virtual env project.
	@rm -rf $(VENV)
