ENV_NAME = $(shell basename $(shell pwd))
REQUIREMENTS = requirements.txt
REGISTRY = registry.github.com
PYTHON_VERSION = $(shell cat .python-version)
DOCKERFILE = Dockerfile
TAG = $(shell date +"%Y%m%d_%H%M")

# Conda environment activation command
ACTIVATE_ENV = . /home/yannick/miniconda3/etc/profile.d/conda.sh && conda activate $(ENV_NAME)

# Conda Channels
CONDA_CHANNELS = -c defaults -c conda-forge


# Default target
.PHONY: all
all: install


# Create conda environment and install requirements
install: $(REQUIREMENTS)
	. /home/yannick/miniconda3/etc/profile.d/conda.sh && conda create -y -n $(ENV_NAME) python=$(PYTHON_VERSION) $(CONDA_CHANNELS)
	$(ACTIVATE_ENV) && pip install -r $(REQUIREMENTS)
	$(ACTIVATE_ENV) && pip install pipreqs
	$(ACTIVATE_ENV) && pip install pytest
	$(ACTIVATE_ENV) && pip install black pylint


# Run the script using the conda environment
.PHONY: run
run:
	$(ACTIVATE_ENV) && python src/app.py 

# Print name
.PHONY: name
name:
	@echo $(ENV_NAME)


# Push to gitlab
# git remote add origin git@gitlab.de:group/project.git
# git remote remove origin
.PHONY: push
push:
	git init
	git add .
	git commit -m $(TAG)
	git push origin main
		

# Update requirements.txt using pipreqs
.PHONY: update
update:
	@echo "Updating requirements.txt using pipreqs..."; 
	@pipreqs --force --encoding=iso-8859-1 --ignore ".venv"
	@$(ACTIVATE_ENV) && conda env export > environment.yml


# Change master to main branch
.PHONY: mainmaster
mainmaster:
	git checkout master 
	git branch -m main


# Lint Python Files
.PHONY: lint 
lint:
	@$(ACTIVATE_ENV) && black src 
	@$(ACTIVATE_ENV) && black Tests 
	@$(ACTIVATE_ENV) && pylint src 
	@$(ACTIVATE_ENV) && pylint Tests 
	

# Add header and licence information
.PHONY: header
header:
	@$(ACTIVATE_ENV) && python Tests/header.py


# Print git Stats
.PHONY: stats
stats:
	@echo "-- Conda Channels --"
	@conda config --show channels
	@echo "-- Current Branch --"
	@git branch --show-current
	@echo "-- Git Origin --"
	@git remote -v


# Build the Docker container
# docker build -t $(IMAGE_NAME) -f $(DOCKERFILE) .
.PHONY: build
build:
	@echo "Updating Container-Tag"
	@sed -i "s|image:.*|image: ${REGISTRY}:v${TAG}|" docker-compose.yaml


# Test via PyTest
.PHONY: test
test:
	pytest


# Clean the virtual environment
.PHONY: clean
clean:
	@echo "Removing conda environment '$(ENV_NAME)' and cleaning up..."
	. $(shell conda info --base)/etc/profile.d/conda.sh && conda env remove -n $(ENV_NAME)


# Help message
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make install   - Create virtual environment and install requirements"
	@echo "  make run       - Run the script using the virtual environment"
	@echo "  make build     - Build the Docker container"
	@echo "  make clean     - Remove the virtual environment"
	@echo "  make help      - Display this help message"
