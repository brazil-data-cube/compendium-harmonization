#
# This file is part of research-processing library
# Copyright (C) 2021 INPE.
#
# research-processing is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

# Image: python:3.8-slim-buster
# DockerHub: https://hub.docker.com/layers/python/library/python/3.8-slim-buster/images/sha256-5498332eee6c73a465a253fe1d00c6dc6f79562e3ea23d105129d00e6ce8736b?context=explore
FROM python@sha256:3bc519ca3214d463ac521f838275e1070ab4b8dbb12e568b4739794db837dadb

EXPOSE 3000

ENV DAGSTER_APP=/opt/dagster/app/
ENV DAGSTER_HOME=/opt/dagster/dagster_home/
ENV DAGSTER_LOCAL_STORAGE=/opt/dagster/storage/

#
# Create base directories
#
RUN mkdir -p $DAGSTER_APP $DAGSTER_HOME

#
# Copy the article analysis files.
#
COPY analysis/pipeline $DAGSTER_APP

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
        dagit==0.12.2 \
        numpy==1.21.1 \
        dagster==0.12.2 \
        rasterio==1.2.6 \
        matplotlib==3.4.2 \
        shapely==1.7.1 \
        docker==5.0.0 \
        graphql-ws==0.3.1 \
    && cd /opt/article/ \
    && python3 setup.py install \
    && apt update -y \
    && apt install curl -y \
    && curl -fsSL https://get.docker.com | sh

#
# Copy Dagster configuration files
#
COPY docker/pipeline/config/dagster.yaml $DAGSTER_HOME/dagster.yaml
COPY docker/pipeline/config/workspace.yaml $DAGSTER_APP/workspace.yaml

WORKDIR $DAGSTER_APP
ENTRYPOINT ["dagit", "-h", "0.0.0.0", "-p", "3000"]
