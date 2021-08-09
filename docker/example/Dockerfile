#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

# Image: python:3.8-slim-buster
# DockerHub: https://hub.docker.com/layers/python/library/python/3.8-slim-buster/images/sha256-5498332eee6c73a465a253fe1d00c6dc6f79562e3ea23d105129d00e6ce8736b?context=explore
FROM python@sha256:3bc519ca3214d463ac521f838275e1070ab4b8dbb12e568b4739794db837dadb

#
# Define directory for output
#
ENV CFACTOR_PIPELINE_DIR /opt/cfactor_article/pipeline
ENV CFACTOR_REPO_DOWNLOAD_OUTPUT /opt/cfactor_article/data
ENV CFACTOR_EXAMPLE_FILES_REFERENCE_FILE /opt/cfactor_article/exampleFiles.json

#
# Install dependencies
#
RUN apt update -y \
    && apt install -y \
        libssl-dev \
        wget \
        curl \
    && pip install --upgrade \
        pip \
        setuptools \
        wheel \
    && pip install \
        loguru==0.5.3 \
        py-multihash==2.0.1 \
        requests==2.26.0 \
        tqdm==4.61.2 \
        PyYAML==5.4.1

#
# Copy download script and example files reference
#
RUN mkdir -p /opt/cfactor_article/data

COPY docker/example/scripts /opt/cfactor_article/scripts
COPY docker/example/config/exampleFiles.json /opt/cfactor_article/exampleFiles.json

#
# Add script to CMD for run when container starts
#
WORKDIR /opt/cfactor_article/scripts

CMD ["pipeline.py"]
ENTRYPOINT ["python3"]
