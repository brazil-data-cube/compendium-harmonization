#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#


class EnvironmentConfig:
    """Execution environment configurations."""
    NBAR_IMAGE = "marujore/nbar@sha256:154d96558ee7131664eba78ad07f730765127393e6ea459a4c3bcb8b51a5c662"

    LASRC_IMAGE = "marujore/lasrc@sha256:718554a7bb7ec15a4fa5404242bf27d38e8c1b774558efcfe91ef32befebfb77"
    SEN2COR_IMAGE = "marujore/sen2cor@sha256:17c5932046d996fa72ec300aa531fd32b82325baf55ca3c7f389fb03b9f4b68c"

    LANDSAT8_ANGLES_IMAGE = "marujore/l8angs@sha256:940d6bcbd765acdb20a69ec140029d7e14bfaa8e668344fb674447b439cc36db"
