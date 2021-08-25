#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""c-factor analysis processing solids."""

import os

from dagster import List, Tuple, String
from dagster import solid, OutputDefinition, InputDefinition

from cfactor import toolbox


@solid(
    input_defs=[
        InputDefinition(name="scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for sen2cor processing.")
    ],
    output_defs=[
        OutputDefinition(name="sen2cor_scene_path",
                         dagster_type=String,
                         description="Full path to the directory where the scenes processed with sen2cor were saved."),
        OutputDefinition(name="sen2cor_sceneid",
                         dagster_type=List[String],
                         description="List with the name of each of the scenes that were processed. These names are"
                                     " equivalent to the name of the directories where each of the processed scenes "
                                     "were saved (Usually, you have the id of each of the scenes as the name of the "
                                     "directories)."),
    ],
    required_resource_keys={"cfactor_repository"},
    description="Apply atmospheric correction using the Sen2Cor algorithm. The solid input indicates which scenes are "
                "to be processed from the Sentinel-2 data repository."
)
def apply_sen2cor(context, scene_ids: List[String]) -> Tuple[String, List[String]]:
    """Sen2Cor (Sentinel-2) Atmosphere correction."""
    from cfactor.surface_reflectance import sen2cor

    #
    # Prepare input/output directory.
    #
    input_dir = context.resources.cfactor_repository["sentinel2_input_dir"]
    output_dir = context.resources.cfactor_repository["outdir_sentinel2"]

    output_dir = toolbox.prepare_output_directory(output_dir, "sen2cor_sr")

    #
    # Apply sen2cor.
    #
    sen2cor(input_dir, output_dir, scene_ids)
    sen2cor_scene_ids = toolbox.filename(os.listdir(output_dir))

    return output_dir, sen2cor_scene_ids


@solid(
    input_defs=[
        InputDefinition(name="scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for LaSRC processing.")
    ],
    output_defs=[
        OutputDefinition(name="lasrc_scene_path",
                         dagster_type=String,
                         description="Full path to the directory where the scenes processed with LaSRC were saved."),
        OutputDefinition(name="lasrc_sceneid",
                         dagster_type=List[String],
                         description="List with the name of each of the scenes that were processed. These names are"
                                     " equivalent to the name of the directories where each of the processed scenes "
                                     "were saved (Usually, you have the id of each of the scenes as the name of the "
                                     "directories)."
                         ),
    ],
    required_resource_keys={"cfactor_lads_data", "cfactor_repository"},
    description="Apply atmospheric correction using the LaSRC algorithm. The solid input indicates which scenes are "
                "to be processed from the Sentinel-2 data repository."
)
def apply_lasrc(context, scene_ids: List[String]) -> Tuple[String, List[String]]:
    """LaSRC (Sentinel-2) Atmosphere correction."""
    from cfactor.surface_reflectance import lasrc

    #
    # Prepare input/output directory.
    #
    input_dir = context.resources.cfactor_repository["sentinel2_input_dir"]
    output_dir = context.resources.cfactor_repository["outdir_sentinel2"]

    output_dir = toolbox.prepare_output_directory(output_dir, "lasrc_sr")

    #
    # Defining the auxiliary data.
    #
    auxiliary_data = context.resources.cfactor_lads_data["lads_auxiliary_directory"]

    #
    # Applying LaSRC.
    #
    lasrc(input_dir, output_dir, scene_ids, auxiliary_data)
    lasrc_scene_ids = toolbox.filename(os.listdir(output_dir))

    return output_dir, lasrc_scene_ids


@solid(
    input_defs=[
        InputDefinition(name="scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Landsat-8 scenes that should be used "
                                    "for NBAR Angles processing (Required step for NBAR processing "
                                    "on Landsat-8 images).")
    ],
    output_defs=[
        OutputDefinition(name="lc8_nbar_angles",
                         dagster_type=List[String],
                         description="List with full path for each scene that had the angles generated."),
    ],
    required_resource_keys={"cfactor_repository"},
    description="Generate the angles of the Landsat-8 scenes used for processing the NBAR products. The generated "
                "angles are saved in the scene directory."
)
def lc8_nbar_angles(context, scene_ids: List[String]) -> List[String]:
    """Landsat-8 Angles for NBAR."""
    from cfactor.nbar import lc8_generate_angles

    #
    # Prepare input/output directory.
    #
    input_dir = context.resources.cfactor_repository["landsat8_input_dir"]

    #
    # Generate Landsat-8 Angles for NBAR calculation.
    #
    return lc8_generate_angles(input_dir, scene_ids)


@solid(
    input_defs=[
        InputDefinition(name="scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Landsat-8 scenes that should be used "
                                    "for NBAR processing.")
    ],
    output_defs=[
        OutputDefinition(name="lc8_nbar_scene_path",
                         dagster_type=String,
                         description="Full path to the directory where the NBAR products were saved."),
        OutputDefinition(name="lc8_nbar_sceneid",
                         dagster_type=List[String],
                         description="List with the name of each NBAR product that were processed. These names are"
                                     " equivalent to the name of the directories where each of the processed scenes "
                                     "were saved."
                         ),
    ],
    required_resource_keys={"cfactor_repository"},
    description="Generate the NBAR products using Landsat-8 scenes."
)
def lc8_nbar(context, scene_ids: List[String]) -> Tuple[String, List[String]]:
    """Landsat-8 NBAR."""
    from cfactor.nbar import lc8_nbar

    #
    # Prepare input/output directory.
    #
    input_dir = context.resources.cfactor_repository["landsat8_input_dir"]
    output_dir = context.resources.cfactor_repository["outdir_landsat8"]

    output_dir = toolbox.prepare_output_directory(output_dir, "lc8_nbar")

    #
    # Generate NBAR product for Landsat-8 scenes.
    #
    lc8_nbar(input_dir, output_dir, scene_ids)
    lc8_nbar_scene_ids = toolbox.filename(os.listdir(output_dir))

    return output_dir, lc8_nbar_scene_ids


@solid(
    input_defs=[
        InputDefinition(name="sen2cor_dir",
                        dagster_type=String,
                        description="Path to the directory where the Sentinel-2 scenes corrected "
                                    "with Sen2Cor are located. It is expected that the scenes used as input will have "
                                    "the influence of the atmosphere corrected with sen2cor."),
        InputDefinition(name="scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for NBAR processing. The scene name must be equivalent to the name of the "
                                    "scene directories in the `sen2cor_dir` directory.")
    ],
    output_defs=[
        OutputDefinition(name="s2_sen2cor_nbar_scene_path",
                         dagster_type=String,
                         description="Full path to the directory where the NBAR products were saved."),
        OutputDefinition(name="s2_sen2cor_nbar_sceneid",
                         dagster_type=List[String],
                         description="List with the name of each NBAR product that were processed with "
                                     "Sentinel-2 scenes. These names are equivalent to the name of the directories "
                                     "where each of the processed scenes were saved."
                         ),
    ],
    required_resource_keys={"cfactor_repository"},
    description="Generate the NBAR products using Sentinel-2 scenes (with sen2cor atmosphere correction)."
)
def s2_sen2cor_nbar(context, sen2cor_dir: String, scene_ids: List[String]) -> Tuple[String, List[String]]:
    """Sentinel-2 (with sen2cor atmosphere correction) NBAR."""
    from cfactor.nbar import s2_sen2cor_nbar

    #
    # Prepare output directory.
    #
    output_dir = context.resources.cfactor_repository["outdir_sentinel2"]
    output_dir = toolbox.prepare_output_directory(output_dir, "s2_sen2cor_nbar")

    #
    # Generate NBAR product for Sentinel-2 scenes (corrected with LaSRC).
    #
    s2_sen2cor_nbar(sen2cor_dir, output_dir, scene_ids)
    s2_sen2cor_nbar_scene_ids = toolbox.filename(os.listdir(output_dir))

    return output_dir, s2_sen2cor_nbar_scene_ids


@solid(
    input_defs=[
        InputDefinition(name="lasrc_dir",
                        dagster_type=String,
                        description="Path to the directory where the Sentinel-2 scenes corrected "
                                    "with LaSRC are located. It is expected that the scenes used as input will have "
                                    "the influence of the atmosphere corrected with LaSRC."),
        InputDefinition(name="scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for NBAR processing. The scene name must be equivalent to the name of the "
                                    "scene directories in the `lasrc_dir` directory.")
    ],
    output_defs=[
        OutputDefinition(name="s2_lasrc_nbar_scene_path",
                         dagster_type=String,
                         description="Full path to the directory where the NBAR products were saved."),
        OutputDefinition(name="s2_lasrc_nbar_sceneid",
                         dagster_type=List[String],
                         description="List with the name of each NBAR product that were processed with "
                                     "Sentinel-2 scenes. These names are equivalent to the name of the directories "
                                     "where each of the processed scenes were saved."
                         ),
    ],
    required_resource_keys={"cfactor_repository"},
    description="Generate the NBAR products using Sentinel-2 scenes (with LaSRC atmosphere correction)."
)
def s2_lasrc_nbar(context, lasrc_dir: String, scene_ids: List[String]) -> Tuple[String, List[String]]:
    """Sentinel-2 (with LaSRC atmosphere correction) NBAR."""
    from cfactor.nbar import s2_lasrc_nbar

    #
    # Prepare output directory.
    #
    output_dir = context.resources.cfactor_repository["outdir_sentinel2"]
    output_dir = toolbox.prepare_output_directory(output_dir, "s2_lasrc_nbar")

    #
    # Generate NBAR product for Sentinel-2 scenes (corrected with LaSRC).
    #
    s2_lasrc_nbar(lasrc_dir, output_dir, scene_ids)
    s2_lasrc_nbar_scene_ids = toolbox.filename(os.listdir(output_dir))

    return output_dir, s2_lasrc_nbar_scene_ids
