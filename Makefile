#
# This file is part of Brazil Data Cube compendium-harmonization.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

SHELL := /bin/bash

.PHONY: example_cleanup_data \
		example_download_data \
		example_pipeline \
		example_notebook \
		replication_cleanup_data \
		replication_download_data \
		replication_pipeline \
		replication_notebook

#
# Minimal example
#

# Utilities
example_cleanup_data:       ## Clean all input/output data generated during the minimal example execution
	rm -rf analysis/data/examples/minimal_example/* \
		&& mkdir -p analysis/data/examples/minimal_example/raw_data \
		&& mkdir -p analysis/data/examples/minimal_example/derived_data

# Data download targets
example_download_data:      ## Download data to use on the minimal example
	docker-compose -f composes/minimal/docker-compose.data.yaml up --build

# Environment - Dagster Pipeline
example_pipeline:           ## Create the Dagster for the minimal example execution.
	docker-compose -f composes/minimal/docker-compose.pipeline.yaml up --build

# Environment - Jupyter Notebook
example_notebook:           ## Create the Jupyter-Notebook for the minimal example execution.
	./setenv.sh \
		&& docker-compose \
			--project-directory ${PWD} \
			-f composes/minimal/docker-compose.notebook.yaml up \
			--build

#
# Replication example
#

# Utilities
replication_cleanup_data:   ## Clean all input/output data generated during the replication example execution
	rm -rf analysis/data/examples/replication_example/* \
		&& mkdir -p analysis/data/examples/replication_example/raw_data \
		&& mkdir -p analysis/data/examples/replication_example/derived_data

# Data download targets
replication_download_data:  ## Download data to use on the replication example
	docker-compose -f composes/replication/docker-compose.data.yaml up --build

# Environment - Dagster Pipeline
replication_pipeline:       ## Create the Dagster for the replication example execution.
	docker-compose -f composes/replication/docker-compose.pipeline.yaml up --build

# Environment - Jupyter Notebook
replication_notebook:       ## Create the Jupyter-Notebook for the replication example execution.
	./setenv.sh \
		&& docker-compose \
			--project-directory ${PWD} \
			-f composes/replication/docker-compose.notebook.yaml up \
			--build

#
# Documentation function (thanks for https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html)
#
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
