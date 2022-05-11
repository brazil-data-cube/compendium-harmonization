#
# This file is part of compendium-harmonization
# Copyright (C) 2021-2022 INPE.
#
# compendium-harmonization is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from dagster import pipeline, ModeDefinition, fs_io_manager

from validation.solids import *
from preprocessing.solids import *

from general.solids import load_and_standardize_sceneids_input
from general.resources import resource_repository, resource_lasrc_auxiliary_data


@pipeline(
    mode_defs=[
        ModeDefinition(
            resource_defs={
                "io_manager": fs_io_manager,
                "repository": resource_repository,
                "lasrc_data": resource_lasrc_auxiliary_data
            }
        )
    ],
    description="analysis pipeline."
)
def research_pipeline():
    """analysis pipeline."""
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
    angles_lc8_dir, scene_angles_lc8 = lc8_nbar_angles(landsat8_sceneids)
    lc8_nbar_dir, lc8_nbar_sceneids = lc8_nbar(angles_lc8_dir, landsat8_sceneids)

    # Sentinel-2/MSI (Sen2Cor)
    s2_sen2cor_nbar_dir, s2_sen2cor_nbar_sceneids = s2_sen2cor_nbar(sen2cor_dir, sen2cor_sceneids)

    # Sentinel-2/MSI (LaSRC)
    s2_lasrc_nbar_dir, s2_lasrc_nbar_sceneids = s2_lasrc_nbar(lasrc_dir, lasrc_sceneids)

    #
    # Validations
    #

    # Landsat-8 Surface Reflectance
    v1 = validation_sr_l8(landsat8_sceneids)

    # Landsat-8 NBAR
    v2 = validation_nbar_l8(lc8_nbar_dir, landsat8_sceneids)

    # Sentinel-2/MSI Surface Reflectance (Sen2Cor)
    v3 = validation_sr_s2_sen2cor(sen2cor_dir, sen2cor_dir, sentinel2_sceneids)

    # Sentinel-2/MSI NBAR (Sen2Cor)
    v4 = validation_nbar_s2_sen2cor(s2_sen2cor_nbar_dir, sen2cor_dir, sentinel2_sceneids)

    # Sentinel-2/MSI (LaSRC)
    v5 = validation_sr_s2_lasrc(lasrc_dir, sen2cor_dir, sentinel2_sceneids)

    # Sentinel-2/MSI NBAR (LaSRC)
    v6 = validation_nbar_s2_lasrc(s2_lasrc_nbar_dir, sen2cor_dir, sentinel2_sceneids)

    # Compare Sen2Cor SR (Landsat-8 and Sentinel-2)
    v7 = validation_sr_l8_s2_sen2cor(sen2cor_dir, sen2cor_dir, landsat8_sceneids, sentinel2_sceneids)

    # Compare LaSRC SR (Landsat-8 and Sentinel-2)
    v8 = validation_sr_l8_s2_lasrc(lasrc_dir, sen2cor_dir, landsat8_sceneids, sentinel2_sceneids)

    # Compare Sen2Cor NBAR (Landsat-8 and Sentinel-2)
    v9 = validation_nbar_l8_s2_sen2cor(lc8_nbar_dir, s2_sen2cor_nbar_dir, sen2cor_dir, landsat8_sceneids,
                                       sentinel2_sceneids)

    # Compare LaSRC NBAR (Landsat-8 and Sentinel-2)
    v10 = validation_nbar_l8_s2_lasrc(lc8_nbar_dir, s2_lasrc_nbar_dir, sen2cor_dir, landsat8_sceneids,
                                      sentinel2_sceneids)

    # Merge the results and save it
    validation_data_to_tidy([v1, v2, v3, v4, v5, v6, v7, v8, v9, v10])
