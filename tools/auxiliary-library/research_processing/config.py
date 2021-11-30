#
# This file is part of research-processing library
# Copyright (C) 2021 INPE.
#
# research-processing is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#


class EnvironmentConfig:
    """Execution environment configurations."""
    NBAR_IMAGE = "marujore/nbar@sha256:154d96558ee7131664eba78ad07f730765127393e6ea459a4c3bcb8b51a5c662"

    LASRC_IMAGE = "marujore/lasrc@sha256:e656dd89cd07a67cae86ece6a28ca70bbc15affc9064efa00ed13ed4337f5434"
    SEN2COR_IMAGE = "marujore/sen2cor@sha256:a4c689a4dcc5a353533a3b1f78c351e59a01a6febacffa398068e013be35d24b"

    LANDSAT8_ANGLES_IMAGE = "marujore/l8angs@sha256:940d6bcbd765acdb20a69ec140029d7e14bfaa8e668344fb674447b439cc36db"
