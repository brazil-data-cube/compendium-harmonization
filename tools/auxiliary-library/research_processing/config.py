#
# This file is part of compendium-harmonization
# Copyright (C) 2021-2022 INPE.
#
# compendium-harmonization is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#


class EnvironmentConfig:
    """Execution environment configurations."""
    NBAR_IMAGE = "marujore/sensor-harm@sha256:184959139eb6671a865c2223d3e488572a2c5a257af8805e337a5efbe15b7281"

    LASRC_IMAGE = "marujore/lasrc@sha256:e98b53614d12dfb1272a8045365439c9621a979feff27cb0d6f9a928e9f12c12"
    SEN2COR_IMAGE = "marujore/sen2cor:2.9.0@sha256:1572353cdab0d73661f1d83f71cffe4e35906cd969cbc85ad2903111f57f9110"

    LANDSAT8_ANGLES_IMAGE = "marujore/landsat-angles@sha256:907666f17aaf236aeb4ddf4bf16ed4705c3ae42aa416c9b5879deb1c754c3a64"
