SHELL := /bin/bash

# 
# Documentation
# 
documentation:
	cd docs \
		&& ./_build.sh

# 
# Minimal example
# 
example_download_data:
	if [ ! -d analysis/data/Landsat8Data ] & \
	[ ! -d analysis/data/Sentinel2Data ] & \
	[ ! -d analysis/data/LADS_AuxiliaryData ]; then \
		echo "Downloading the minimum example files."; sleep 5; \
		docker-compose -f docker-compose.example.yaml up --build; \
	else \
		echo "The files have already been downloaded"; \
	fi

example_base_notebook:
	# Configuring the `.env` used to define required Docker permissions on
	# Jupyter Container.
	rm -f .env
	echo "UID=`id -u ${USER}`" > .env
	echo "GID=`cut -d: -f3 < <(getent group docker)`" >> .env
	
	docker-compose -f docker-compose.notebook.yaml up --build

example_base_pipeline:
	docker-compose -f docker-compose.pipeline.yaml up --build

# 
# Complete options for download and execute the minimal example.
# 
example_pipeline: example_download_data example_base_pipeline
example_notebook: example_download_data example_base_notebook
