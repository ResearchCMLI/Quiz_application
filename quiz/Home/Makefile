HIDE         := @
VENV         := env
PYVER        := 3
PIP          ?= $(VENV)/bin/pip
REQUIREMENTS := requirements.txt

REGISTRY     ?= artifactory.ciena.com
VENDOR       ?= blueplanet
NAME         ?= $(shell python -c "import tomli; print(tomli.load(open('pyproject.toml'), 'rb'))['project']['name']")
VERSION      ?= $(shell python -c "import tomli; print(tomli.load(open('pyproject.toml'), 'rb'))['project']['version']")

.PHONY: help clean requirements prepare-venv run-local

help:
	$(HIDE)echo "  help          this list"
	$(HIDE)echo "  clean         delete temporary files"
	$(HIDE)echo " --------------------------------------------------------"
	$(HIDE)echo "/ virtualenv backed commands                            /"
	$(HIDE)echo "--------------------------------------------------------"
	$(HIDE)echo "  requirements  generate requirements.txt from pyproject.toml"
	$(HIDE)echo "  prepare-venv  install requirements and self into virtualenv $(VENV)"
	$(HIDE)echo "  run-local     run the Streamlit app locally"

clean:
	$(HIDE)rm -rf build/
	$(HIDE)rm -rf dist/
	$(HIDE)rm -rf env/
	$(HIDE)rm -rf *.egg
	$(HIDE)rm -rf *.egg-info
	$(HIDE)find . -type d -name "__pycache__" -exec rm -rf {} +
	$(HIDE)find . -type f -name "*.pyc" -exec rm -f {} +

requirements:
	$(HIDE)echo "Generating pinned requirements.txt from pyproject.toml..."
	# Create a temporary venv to install pip-tools
	$(HIDE)python$(PYVER) -m venv $(VENV)_temp
	$(HIDE)$(VENV)_temp/bin/pip install pip-tools
	$(HIDE)echo "Compiling dependencies (including 'dev' extra)..."
	# Use pip-compile directly on pyproject.toml, including the 'dev' extra
	$(HIDE)$(VENV)_temp/bin/pip-compile \
		--resolver=backtracking \
		--output-file=$(REQUIREMENTS) \
		--extra dev \
		pyproject.toml
	$(HIDE)echo "Cleaning up temporary environment..."
	$(HIDE)rm -rf $(VENV)_temp
	$(HIDE)echo "Requirements file generated: $(REQUIREMENTS)"

prepare-venv: clean
	$(HIDE)echo "Creating virtual environment..."
	$(HIDE)python$(PYVER) -m venv $(VENV)
	$(HIDE)$(VENV)/bin/pip install --upgrade pip
	$(HIDE)echo "Installing project and dependencies..."
	# This command installs the project and reads pyproject.toml for dependencies
	# You might want to add optional dependencies like 'dev' here if needed
	$(HIDE)$(VENV)/bin/pip install -e ".[dev]" --no-cache-dir
	$(HIDE)echo "Virtual environment ready at: $(VENV)"

run-local:
	$(HIDE)$(VENV)/bin/streamlit run quesgen/main.py
