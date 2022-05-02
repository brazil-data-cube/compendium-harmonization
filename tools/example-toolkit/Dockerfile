#
# This file is part of compendium-harmonization
# Copyright (C) 2021-2022 INPE.
#
# compendium-harmonization is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

# Image: continuumio/miniconda3
# Image Tag: 4.10.3
# DockerHub: https://hub.docker.com/layers/continuumio/miniconda3/4.10.3/images/sha256-8ba38cba2d88e3e094e3e3c32f1daaacb57a331aaf17a5ee0194c30d774903e0?context=explore
FROM continuumio/miniconda3@sha256:8ba38cba2d88e3e094e3e3c32f1daaacb57a331aaf17a5ee0194c30d774903e0

#
# 1. Configuring the base dependencies
#
RUN apt-get update -y \
    && apt-get install -y libssl-dev wget curl \
    && rm -rf /var/lib/apt/lists/*

#
# 2. Installing the examples toolkit dependencies
#
COPY environment.yml environment.yml

RUN conda env update --file environment.yml --prune

#
# 3. Copying the examples toolkit scripts to container.
#
WORKDIR /opt/compendium/example-toolkit

COPY . /opt/compendium/example-toolkit

#
# 4. Configuring the CMD and Entrypoint the the base minimal example toolkit script.
#
CMD ["scripts/pipeline.py"]
ENTRYPOINT ["python3"]
