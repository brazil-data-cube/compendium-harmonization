#!/bin/bash
#
# This file is part of compendium-harmonization
# Copyright (C) 2021-2022 INPE.
#
# compendium-harmonization is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

#
# 1. Base user
#
echo "UID=`id -u ${USER}`" > .env

#
# 2. Docker group
#
echo "GID=`cut -d: -f3 < <(getent group docker)`" >> .env
