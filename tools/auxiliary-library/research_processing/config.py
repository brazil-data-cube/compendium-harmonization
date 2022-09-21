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
    NBAR_IMAGE = "marujore/nbar@sha256:18100383032d43eb7d083e6d00357bccb7ef1879faaf917dcb444e579668946d"

    LASRC_IMAGE = "marujore/lasrc@sha256:e656dd89cd07a67cae86ece6a28ca70bbc15affc9064efa00ed13ed4337f5434"
    SEN2COR_IMAGE = "marujore/sen2cor@sha256:a4c689a4dcc5a353533a3b1f78c351e59a01a6febacffa398068e013be35d24b"

    LANDSAT8_ANGLES_IMAGE = "marujore/l8angs@sha256:6416006a777ab15d2ac98aac998f0c994068ca8b6febc2d625e8ca644e837559"
