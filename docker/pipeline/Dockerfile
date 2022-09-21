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

# Image: continuumio/miniconda3
# Image Tag: :4.10.3
# DockerHub: https://hub.docker.com/layers/continuumio/miniconda3/4.10.3/images/sha256-8ba38cba2d88e3e094e3e3c32f1daaacb57a331aaf17a5ee0194c30d774903e0?context=explore
FROM continuumio/miniconda3@sha256:8ba38cba2d88e3e094e3e3c32f1daaacb57a331aaf17a5ee0194c30d774903e0


#
# 1. Defining the DagIt network port.
#
EXPOSE 3000

#
# 2. Configuring the Dagster environment variables.
#

# Directory where the dagster files (pipeline definition and configurations) will be saved.
ENV DAGSTER_APP=/opt/dagster/app/

# Dagster configuration directory.
ENV DAGSTER_HOME=/opt/dagster/dagster_home/

# Dagster persistance storage location (To save the pipeline status and other related files).
ENV DAGSTER_LOCAL_STORAGE=/opt/dagster/storage/

#
# 3. Creating directories from the environment variables.
#
RUN mkdir -p $DAGSTER_APP $DAGSTER_HOME

#
# 4. Copying the pipeline definitions.
#

# Pipeline scripts
COPY analysis/pipeline $DAGSTER_APP

# Configuration files
COPY docker/pipeline/config/dagster.yaml $DAGSTER_HOME/dagster.yaml
COPY docker/pipeline/config/workspace.yaml $DAGSTER_APP/workspace.yaml

#
# 5. Configuring the base dependencies
#
USER root
RUN apt-get update -y \
    && apt-get install -y git curl \
    && curl -fsSL https://get.docker.com | sh \
    && rm -rf /var/lib/apt/lists/*

#
# 6. Installing the research-processing library dependencies.
#
COPY docker/pipeline/environment.yml environment.yml

RUN conda env update --file environment.yml --prune

#
# 7. Installing the research-processing library.
#
COPY tools/auxiliary-library/ /opt/compendium/research_processing

RUN pip3 install /opt/compendium/research_processing

#
# 8. Defining the working directory and DagIt entrypoint
#
WORKDIR $DAGSTER_APP
ENTRYPOINT ["dagit", "-h", "0.0.0.0", "-p", "3000"]
