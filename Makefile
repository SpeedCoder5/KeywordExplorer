# HELP
.PHONY: help
.ONESHELL:
.SHELLFLAGS := -e -c
SHELL := /bin/bash
PROJECT_NAME=kwe
DB_NAMES := gpt_summary narrative_maps twitter_v2

help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: ## Removes build artifacts
	find . | grep -E "(__pycache__|\.pyc|\.pyo|\.egg-info|\dist|\.pytest_cache)" | xargs rm -rf;

clean-all: clean ## Remove the virtual environment and build artifacts
	rm -rf $(HOME)/.virtualenvs/$(PROJECT_NAME);

venv: ## Create/update project's virtual enviornment. To activate, run: source activate.sh
	python3 -m venv $(HOME)/.virtualenvs/$(PROJECT_NAME); \
	. $(HOME)/.virtualenvs/$(PROJECT_NAME)/bin/activate; \
	python -m pip install --upgrade pip; \
	python -m pip install -v -r requirements.txt; \
	python -m pip install -e .; \
	sudo chmod 775 activate;

test: venv ## Run unit tests
	. $(HOME)/.virtualenvs/$(PROJECT_NAME)/bin/activate;\
	pytest;

dist: clean test ## Create python package and run unit tests
	. $(HOME)/.virtualenvs/$(PROJECT_NAME)/bin/activate;\
	python -m build;

publish: dist ## Create/publish python package to test pypi repo
	. $(HOME)/.virtualenvs/$(PROJECT_NAME)/bin/activate;\
	python -m twine upload --repository testpypi dist/*; \

show-databases: ## show existing databases (also tests database connection)
	echo "showing databases";\
	mysql -e "SHOW DATABASES;";

create-databases: ## create databases
	cd data; \
	for db_name in $(DB_NAMES); do \
		if [ -f error.log ]; then rm error.log; fi; \
		echo "creating $$db_name"; \
		mysql -v -e "CREATE DATABASE IF NOT EXISTS $$db_name;"; \
		mysql -v -D $$db_name -e "SOURCE $${db_name}_schema.sql" 2> >(tee error.log); \
		if [ -s error.log ]; then \
			echo "Error occurred during MySQL execution. Check data/error.log for details."; \
			cat error.log; \
			exit 1; \
		fi; \
	done; \
	cd -

drop-databases: ## drop databases
	for db_name in $(DB_NAMES); do \
		mysql -v -e "DROP DATABASE $$db_name;";
	done; \
