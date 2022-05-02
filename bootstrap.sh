#!/bin/bash
#
# This file is part of compendium-harmonization
# Copyright (C) 2021-2022 INPE.
#
# compendium-harmonization is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

#
# 1. Updating the environment
#
apt-get update -y
apt-get install -y apt-get install \
            ca-certificates \
            curl \
            gnupg \
            lsb-release \
            vim \
            htop

#
# 2. Installing Docker
#

# 2.1. Download
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y
apt-get install docker-ce docker-ce-cli containerd.io -y

# 2.2. Configure the user to use Docker
groupadd docker
usermod -aG docker vagrant

#
# 3. Installing Docker Compose
#

# 3.1. Download
curl -L \
  "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose

# 3.2. Make it executable
chmod +x /usr/local/bin/docker-compose

# 3.3. Linking it
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
