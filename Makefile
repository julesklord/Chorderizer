.PHONY: install test lint format clean

install:
	pip install -e .

test:
	pytest tests/

lint:
	flake8 src/ tests/

format:
	black src/ tests/

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .flake8 .pre-commit-config.yaml
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete
