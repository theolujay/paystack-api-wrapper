# ==================================================================================== #
# HELPERS
# ==================================================================================== #

## help: print this help message
.PHONY: help
help:
	@echo 'Usage:'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' | sed -e 's/^/ /'

.PHONY: confirm
confirm:
	@echo -n 'Are you sure? [y/N] ' && read ans && [ $${ans:-N} = y ]

# ==================================================================================== #
# DEVELOPMENT
# ==================================================================================== #

## install: install dependencies
.PHONY: install
install:
	@if command -v uv > /dev/null; then \
		uv sync --all-extras; \
	else \
		pip install -e ".[dev]"; \
	fi

## clean: remove build and cache artifacts
.PHONY: clean
clean:
	rm -rf dist/ build/ *.egg-info .pytest_cache .coverage .mypy_cache .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

# ==================================================================================== #
# QUALITY CONTROL
# ==================================================================================== #

## lint: run Ruff linter
.PHONY: lint
lint:
	@if command -v uv > /dev/null; then \
		uv run ruff check .; \
	else \
		ruff check .; \
	fi

## lint/fix: auto-fix lint issues
.PHONY: lint/fix
lint/fix:
	@if command -v uv > /dev/null; then \
		uv run ruff check --fix .; \
	else \
		ruff check --fix .; \
	fi

## format: format code with Ruff
.PHONY: format
format:
	@if command -v uv > /dev/null; then \
		uv run ruff format .; \
		uv run ruff check --select I --fix .; \
	else \
		ruff format .; \
		ruff check --select I --fix .; \
	fi

## format/check: check formatting without changes
.PHONY: format/check
format/check:
	@if command -v uv > /dev/null; then \
		uv run ruff format --check .; \
	else \
		ruff format --check .; \
	fi

## typecheck: run mypy type checking
.PHONY: typecheck
typecheck:
	@if command -v uv > /dev/null; then \
		uv run mypy paystack; \
	else \
		mypy paystack; \
	fi

## test: run tests with pytest
.PHONY: test
test:
	@if command -v uv > /dev/null; then \
		uv run pytest; \
	else \
		pytest; \
	fi

## test/coverage: run tests with coverage report
.PHONY: test/coverage
test/coverage:
	@if command -v uv > /dev/null; then \
		uv run pytest --cov=paystack --cov-report=term-missing; \
	else \
		pytest --cov=paystack --cov-report=term-missing; \
	fi

# ==================================================================================== #
# BUILD & RELEASE
# ==================================================================================== #

## build: build the package (wheel and sdist)
.PHONY: build
build: clean
	@if command -v uv > /dev/null; then \
		uv run python -m build; \
	else \
		python -m build; \
	fi

## publish: publish the package to PyPI
.PHONY: publish
publish: confirm build
	@if command -v uv > /dev/null; then \
		uv run twine upload dist/*; \
	else \
		twine upload dist/*; \
	fi
