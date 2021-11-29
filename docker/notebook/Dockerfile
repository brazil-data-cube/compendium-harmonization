#
# This file is part of research-processing library
# Copyright (C) 2021 INPE.
#
# research-processing is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
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

RUN cd /opt/compendium/research_processing \
    && python3 setup.py install

#
# 4. Changing the user.
#
USER ${NB_USER}
