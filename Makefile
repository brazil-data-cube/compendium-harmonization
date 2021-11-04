SHELL := /bin/bash

.PHONY: documentation_build \
				documentation_rstudio \
				example_download_data \
				example_base_notebook \
				example_base_pipeline \
				example_pipeline \
				example_notebook

# 
# Documentation (HTML pages)
# 
documentation_build:     ## Build the HTML documentation
	cd docs \
		&& ./_build.sh

# 
# Documentation (Environment - RStudio)
# 
documentation_rstudio:     ## Create the RStudio Docker instance, used to develop the documentation.
	docker-compose -f docker-compose.documentation.yaml up

# 
# Minimal example (Download data)
# 
analysis/data/raw_data/%/:
	docker-compose -f docker-compose.example.yaml up --build
	
example_download_data: analysis/data/raw_data/%/  ## Download data to use on the minimal example

# 
# Minimal example (Environment - Jupyter Notebook)
# 
example_base_notebook:     ## Create the Jupyter-Notebook minimal example instance
	# Configuring the `.env` used to define required Docker permissions on Jupyter Container.
	rm -f .env
	echo "UID=`id -u ${USER}`" > .env
	echo "GID=`cut -d: -f3 < <(getent group docker)`" >> .env
	
	docker-compose -f docker-compose.notebook.yaml up --build

# 
# Minimal example (Environment - Dagster Pipeline)
# 
example_base_pipeline:     ## Create the Dagster minimal example instance
	docker-compose -f docker-compose.pipeline.yaml up --build

# 
# Complete options for download and execute the minimal example.
# 
example_pipeline: example_download_data example_base_pipeline    ## Configure the minimal example data and create the Jupyter-Notebook instance
example_notebook: example_download_data example_base_notebook    ## Configure the minimal example data and create the Dagster instance

#
# Documentation function (thanks for https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html)
#
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
