#
# This file is part of research-processing library
# Copyright (C) 2021 INPE.
#
# research-processing is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

# Image: continuumio/miniconda3
# Image Tag: 4.10.3
# DockerHub: https://hub.docker.com/layers/continuumio/miniconda3/4.10.3/images/sha256-8ba38cba2d88e3e094e3e3c32f1daaacb57a331aaf17a5ee0194c30d774903e0?context=explore
FROM continuumio/miniconda3@sha256:8ba38cba2d88e3e094e3e3c32f1daaacb57a331aaf17a5ee0194c30d774903e0

#
# 1. Install scripts dependencies.
#
COPY environment.yml environment.yml
RUN conda env update --file environment.yml --prune

#
# 2. Copy download the minimal example toolkit scripts.
#
WORKDIR /opt/compendium/calculate-checksum
COPY scripts scripts

#
# 3. Configuring the entrypoint.
#
ENTRYPOINT ["python3"]
