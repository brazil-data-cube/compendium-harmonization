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

# Image: jupyter/base-notebook
# Image Tag: lab-3.1.13
# Image URL: https://hub.docker.com/layers/jupyter/base-notebook/lab-3.1.13/images/sha256-9a388da87e9d2b8019df20439977953d0576f6168348f621498ac62b45e2f88f?context=explore
FROM jupyter/base-notebook@sha256:9a388da87e9d2b8019df20439977953d0576f6168348f621498ac62b45e2f88f

USER root

#
# 1. Configuring the base dependencies
#
USER root
RUN apt-get update -y \
    && apt-get install -y git curl \
    && curl -fsSL https://get.docker.com | sh \
    && rm -rf /var/lib/apt/lists/*

#
# 2. Installing the research-processing library dependencies
#
COPY docker/notebook/environment.yml environment.yml

RUN conda env update --file environment.yml --prune

#
# 3. Installing the research-processing library.
#
COPY tools/auxiliary-library/ /opt/compendium/research_processing

RUN pip3 install /opt/compendium/research_processing

#
# 4. Changing the user.
#
USER ${NB_USER}
