#!/bin/bash

#
# 1. Base user
#
export COMPENDIUM_UID=`id -u ${USER}`

#
# 2. Docker group
#
export COMPENDIUM_GID=`cut -d: -f3 < <(getent group docker)`
