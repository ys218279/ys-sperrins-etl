## Makefile to build the project

PROJECT_NAME = team-espresso-etl-project
REGION = eu-west-2
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}:${WD}/src
SHELL := /bin/bash
PROFILE = default
PIP:=pip

############################


## Create python interpreter environment.
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
		$(PIP) install -q virtualenv virtualenvwrapper; \
		virtualenv venv --python=$(PYTHON_INTERPRETER); \
	)



# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source ./venv/bin/activate

############################


# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

## Build the environment requirements
requirements: create-environment
#Installation of pip-tools for later use
	$(call execute_in_env, $(PIP) install pip-tools)
#Running of pip-compile (from pip-tools) to run the requirements.in, which creates a requirements.txt
	$(call execute_in_env, pip-compile requirements.in)
#Installation of the requirements.txt
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

############################

# Set Up

## Install black: formatter 
black:
	$(call execute_in_env, $(PIP) install black)

## Install coverage: report testing-coverage
coverage:
	$(call execute_in_env, $(PIP) install coverage)

## Install pip-audit: scanning for vulnerabilities in dependencies (security)
pip-audit:
	$(call execute_in_env, $(PIP) install pip-audit)

## Install bandit: scans the code for security vulnerabilities
bandit:
	$(call execute_in_env, $(PIP) install bandit)

## Set up dev requirements (coverage, pip-audit, black)
dev-setup: black coverage pip-audit bandit

############################


## Run the black code check
run-black:
	@echo ""
	$(call execute_in_env, find . -name "*.py" -not -path "./venv/*" -exec black {} +)

## Run the unit tests
unit-test:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest -v --testdox)

## Run the coverage check
check-coverage:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest --cov=src tests/)

## Run the dependency vulnerabilities check
check-dependencies:
	$(call execute_in_env, pip-audit -v)

## Run the code vulnerabilities check
check-code:
	$(call execute_in_env, bandit ./src/*.py ./tests/*.py)

## Run all checks
run-checks: run-black unit-test check-coverage check-dependencies check-code

############################

## Deployment
##terraform init, terraform plan, terraform apply etc etc 