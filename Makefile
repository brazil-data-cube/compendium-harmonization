SHELL := /bin/bash

.PHONY: documentation_build \
			documentation_rstudio \
			example_pipeline \
			example_notebook \
			replication_pipeline \
			replication_notebook

# 
# Documentation (HTML pages)
# 
documentation_build:     ## Build the HTML documentation
	cd docs \
		&& ./_build.sh

# 
# Minimal example
# 

# Data download targets
analysis/data/examples/minimal_example/raw_data/%/:
	docker-compose -f composes/minimal/docker-compose.data.yaml up --build

example_download_data: analysis/data/examples/minimal_example/raw_data/%/  ## Download data to use on the minimal example

# Environment - Jupyter Notebook
example_notebook: example_download_data     ## Create the Jupyter-Notebook minimal example instance
	docker-compose -f composes/minimal/docker-compose.notebook.yaml up --build

# Environment - Dagster Pipeline
example_pipeline: example_download_data   ## Create the Dagster minimal example instance
	docker-compose -f composes/minimal/docker-compose.pipeline.yaml up --build

#
# Replication example
#

# Data download targets
analysis/data/examples/replication_example/raw_data/%:
	docker-compose -f composes/replication/docker-compose.data.yaml up --build

replication_download_data: analysis/data/examples/replication_example/raw_data/%  ## Download data to use on the replication example

# Environment - Jupyter Notebook
replication_notebook: replication_download_data     ## Create the Jupyter-Notebook minimal example instance
	source setenv.sh \
		&& docker-compose -f composes/replication/docker-compose.notebook.yaml up --build

# Environment - Dagster Pipeline
replication_pipeline: replication_download_data   ## Create the Dagster minimal example instance
	docker-compose -f composes/replication/docker-compose.pipeline.yaml up --build

#
# Documentation function (thanks for https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html)
#
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
