#
# This file is part of research-processing library
# Copyright (C) 2021 INPE.
#
# research-processing is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

# Image: jupyter/minimal-notebook:python-3.8.8
# DockerHub: https://hub.docker.com/layers/jupyter/minimal-notebook/python-3.8.8/images/sha256-60f7a194793fc473b168497c6d52ff1284a037c1b366e7310738966989eba1f5?context=explore
FROM jupyter/minimal-notebook:python-3.8.8@sha256:60f7a194793fc473b168497c6d52ff1284a037c1b366e7310738966989eba1f5

USER root

#
# Copy the research-processing article package files.
#
COPY research_processing /opt/article/research_processing
COPY setup.py /opt/article/setup.py

#
# Install dependencies
#
RUN pip install --upgrade \
    pip \
    setuptools \
    wheel \
    && pip install \
        pandas==1.3.2 \
        numpy==1.21.1 \
        rasterio==1.2.6 \
        matplotlib==3.4.2 \
        shapely==1.7.1 \
        docker==5.0.0 \
    && cd /opt/article/ \
    && python3 setup.py install \
    && apt update -y \
    && apt install curl -y \
    && curl -fsSL https://get.docker.com | sh

USER $NB_USER
