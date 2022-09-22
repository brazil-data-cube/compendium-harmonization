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
