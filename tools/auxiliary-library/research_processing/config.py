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


class EnvironmentConfig:
    """Execution environment configurations."""
    NBAR_IMAGE = "marujore/sensor-harm@sha256:184959139eb6671a865c2223d3e488572a2c5a257af8805e337a5efbe15b7281"

    LASRC_IMAGE = "marujore/lasrc@sha256:e98b53614d12dfb1272a8045365439c9621a979feff27cb0d6f9a928e9f12c12"
    SEN2COR_IMAGE = "marujore/sen2cor:2.9.0@sha256:1572353cdab0d73661f1d83f71cffe4e35906cd969cbc85ad2903111f57f9110"

    LANDSAT8_ANGLES_IMAGE = "marujore/landsat-angles@sha256:907666f17aaf236aeb4ddf4bf16ed4705c3ae42aa416c9b5879deb1c754c3a64"
