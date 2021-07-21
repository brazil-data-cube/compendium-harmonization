#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from dagster import pipeline, ModeDefinition, fs_io_manager

from preprocessing.solids import *
from validation.solids import *


@pipeline(
    mode_defs=[
        ModeDefinition(
            resource_defs={
                "io_manager": fs_io_manager
            }
        )
    ]
)
def cfactor_pipeline():
    #
    # Load and validate the input config
    #
    (
        lc8_inputs, lc8_scenes, s2_inputs, s2_scenes, lc8_outputs, s2_outputs,
    ) = config_gatter()

    #
    # Sentinel-2 Atmosphere correction (with sen2cor and LaSRC)
    #

    # sen2cor
    sen2cor_dir, sen2cor_sceneids = apply_sen2cor(
        s2_inputs, s2_outputs, s2_scenes
    )

    # LaSRC
    lasrc_dir, lasrc_sceneids = apply_lasrc(
        s2_inputs, s2_outputs, s2_scenes
    )

    #
    # NBAR (with Landsat-8/OLI and Sentinel-2/MSI)
    #

    # Sentinel-2/MSI (Sen2Cor)
    s2_sen2cor_nbar_dir, s2_sen2cor_nbar_sceneids = s2_sen2cor_nbar(
        sen2cor_dir, s2_outputs, sen2cor_sceneids
    )

    # Sentinel-2/MSI (LaSRC)
    s2_lasrc_nbar_dir, s2_lasrc_nbar_sceneids = s2_lasrc_nbar(
        lasrc_dir, s2_outputs, lasrc_sceneids
    )

    # Landsat-8 NBAR
    scene_angles_lc8 = lc8_nbar_angles(lc8_inputs, lc8_scenes)
    lc8_nbar_dir, lc8_nbar_sceneids = lc8_nbar(lc8_inputs, lc8_outputs, scene_angles_lc8)

    #
    # Validations
    #

    # Landsat-8 NBAR
    validation_nbar_l8(lc8_nbar_dir, lc8_inputs, lc8_outputs, lc8_scenes)

    # Sentinel-2/MSI (Sen2Cor)
    validation_nbar_s2_sen2cor(s2_sen2cor_nbar_dir, sen2cor_dir, s2_outputs, s2_sen2cor_nbar_sceneids)

    # Sentinel-2/MSI (LaSRC)
    validation_nbar_s2_lasrc(s2_lasrc_nbar_dir, sen2cor_dir, s2_outputs, s2_lasrc_nbar_sceneids)
