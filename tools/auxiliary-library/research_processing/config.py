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

    LASRC_IMAGE = "marujore/lasrc@sha256:1b9d95a8a4956980a94cf06a75241e1a0257cd641cda8b9a87da68c83be594cd"
    SEN2COR_IMAGE = "marujore/sen2cor:2.9.0@sha256:253aa3e220ba9cfe2521b76b0dd5a4ba437f980271ec9ba60b9d591207982b8f"

    LANDSAT8_ANGLES_IMAGE = "marujore/landsat-angles@sha256:907666f17aaf236aeb4ddf4bf16ed4705c3ae42aa416c9b5879deb1c754c3a64"
