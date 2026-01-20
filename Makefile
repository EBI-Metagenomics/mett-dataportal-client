.PHONY: help docs docs-generate docs-render docs-preview docs-clean install test

help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

docs-generate: ## Generate API documentation from OpenAPI spec
	@echo "Generating API documentation..."
	python3 scripts/generate-api-docs.py

docs-render: docs-generate ## Render documentation to HTML
	@echo "Rendering documentation..."
	quarto render docs/reference/api-reference.qmd

docs-preview: docs-generate ## Preview documentation in browser (watch mode)
	@echo "Starting documentation preview server..."
	quarto preview docs/reference/api-reference.qmd

docs-clean: ## Clean generated documentation files
	@echo "Cleaning generated files..."
	rm -rf docs/_site
	rm -f docs/reference/api-reference.html
	rm -rf docs/reference/api-reference_files

docs: docs-render ## Generate and render documentation (default)

install: ## Install the package in development mode
	pip install -e .

test: ## Run tests
	pytest tests/

lint: ## Run linters
	ruff check mett_dataportal/
	ruff check scripts/

format: ## Format code
	ruff format mett_dataportal/
	ruff format scripts/
