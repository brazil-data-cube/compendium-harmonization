#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from dagster import pipeline, ModeDefinition, fs_io_manager

from general.resources import cfactor_resource_repository, cfactor_resource_lads_auxiliary_data
from general.solids import *
from preprocessing.solids import *
from validation.solids import *


@pipeline(
    mode_defs=[
        ModeDefinition(
            resource_defs={
                "io_manager": fs_io_manager,
                "cfactor_repository": cfactor_resource_repository,
                "cfactor_lads_data": cfactor_resource_lads_auxiliary_data
            }
        )
    ],
    description="c-factor analysis pipeline."
)
def cfactor_pipeline():
    """c-factor analysis pipeline."""
    #
    # Load and validate the input config
    #
    landsat8_sceneids, sentinel2_sceneids = load_and_standardize_sceneids_input()

    #
    # Sentinel-2 Atmosphere correction (with sen2cor and LaSRC)
    #

    # sen2cor
    sen2cor_dir, sen2cor_sceneids = apply_sen2cor(sentinel2_sceneids)

    # LaSRC
    lasrc_dir, lasrc_sceneids = apply_lasrc(sentinel2_sceneids)

    #
    # NBAR (with Landsat-8/OLI and Sentinel-2/MSI)
    #

    # Landsat-8 NBAR
    scene_angles_lc8 = lc8_nbar_angles(landsat8_sceneids)
    lc8_nbar_dir, lc8_nbar_sceneids = lc8_nbar(scene_angles_lc8)

    # Sentinel-2/MSI (Sen2Cor)
    s2_sen2cor_nbar_dir, s2_sen2cor_nbar_sceneids = s2_sen2cor_nbar(sen2cor_dir, sen2cor_sceneids)

    # Sentinel-2/MSI (LaSRC)
    s2_lasrc_nbar_dir, s2_lasrc_nbar_sceneids = s2_lasrc_nbar(lasrc_dir, lasrc_sceneids)

    #
    # Validations
    #

    # Landsat-8 Surface Reflectance
    validation_sr_l8(landsat8_sceneids)

    # Landsat-8 NBAR
    validation_nbar_l8(lc8_nbar_dir, landsat8_sceneids)

    # Sentinel-2/MSI Surface Reflectance (Sen2Cor)
    validation_sr_s2_sen2cor(sen2cor_dir, sen2cor_dir, sentinel2_sceneids)

    # Sentinel-2/MSI NBAR (Sen2Cor)
    validation_nbar_s2_sen2cor(s2_sen2cor_nbar_dir, sen2cor_dir, sentinel2_sceneids)

    # Sentinel-2/MSI (LaSRC)
    validation_sr_s2_lasrc(lasrc_dir, sen2cor_dir, sentinel2_sceneids)

    # Sentinel-2/MSI NBAR (LaSRC)
    validation_nbar_s2_lasrc(s2_lasrc_nbar_dir, sen2cor_dir, sentinel2_sceneids)

    # Compare Sen2Cor SR (Landsat-8 and Sentinel-2)
    validation_sr_l8_s2_sen2cor(sen2cor_dir, sen2cor_dir, landsat8_sceneids, sentinel2_sceneids)

    # Compare LaSRC SR (Landsat-8 and Sentinel-2)
    validation_sr_l8_s2_lasrc(lasrc_dir, sen2cor_dir, landsat8_sceneids, sentinel2_sceneids)

    # Compare Sen2Cor NBAR (Landsat-8 and Sentinel-2)
    validation_nbar_l8_s2_sen2cor(lc8_nbar_dir, s2_sen2cor_nbar_dir, sen2cor_dir, landsat8_sceneids, sentinel2_sceneids)

    # Compare LaSRC NBAR (Landsat-8 and Sentinel-2)
    validation_nbar_l8_s2_lasrc(lc8_nbar_dir, s2_lasrc_nbar_dir, sen2cor_dir, landsat8_sceneids, sentinel2_sceneids)
