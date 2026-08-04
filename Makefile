PYTHON ?= python3.10
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

.PHONY: bootstrap setup dev venv install test lint format clean

bootstrap: venv install

setup: bootstrap

dev: bootstrap

venv:
	$(PYTHON) -m venv $(VENV)
	$(PY) -m pip install --upgrade pip setuptools wheel

install:
	$(PIP) install -e ".[dev]"

test:
	$(PY) -m pytest -q

lint:
	$(PY) -m ruff check src/ tests/

format:
	$(PY) -m ruff format src/ tests/

clean:
	rm -rf $(VENV)
