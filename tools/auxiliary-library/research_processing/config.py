#
# This file is part of compendium-harmonization
# Copyright (C) 2021-2022 INPE.
#
# compendium-harmonization is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#


class EnvironmentConfig:
    """Execution environment configurations."""
    NBAR_IMAGE = "marujore/nbar@sha256:18100383032d43eb7d083e6d00357bccb7ef1879faaf917dcb444e579668946d"

    LASRC_IMAGE = "marujore/lasrc@sha256:e656dd89cd07a67cae86ece6a28ca70bbc15affc9064efa00ed13ed4337f5434"
    SEN2COR_IMAGE = "marujore/sen2cor@sha256:a4c689a4dcc5a353533a3b1f78c351e59a01a6febacffa398068e013be35d24b"

    LANDSAT8_ANGLES_IMAGE = "marujore/l8angs@sha256:6416006a777ab15d2ac98aac998f0c994068ca8b6febc2d625e8ca644e837559"
