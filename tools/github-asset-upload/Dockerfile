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

# Image: rocker/r-ver
# Image Tag: 4.0.2
# Dockerhub URL: https://hub.docker.com/layers/rocker/r-ver/4.0.2/images/sha256-a1d68ac7723fdc3dbbbbf2ff8214a97ccfa66f75b32a35c1e280d29357c87cef?context=explore
FROM rocker/r-ver@sha256:a1d68ac7723fdc3dbbbbf2ff8214a97ccfa66f75b32a35c1e280d29357c87cef

#
# 1. Configuring the base dependencies
#
RUN apt-get update -y \
    && apt-get install -y libssl-dev wget curl libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

#
# 2. Defining the working dir
#
WORKDIR /opt/compendium/upload-github-assets

#
# 3. Configuring the dependencies
#
COPY . .
RUN Rscript -e "install.packages('renv'); renv::restore()"

#
# 4. Configuring the CMD and Entrypoint.
#
CMD ["R/upload_github_assets.R"]
ENTRYPOINT ["Rscript"]
