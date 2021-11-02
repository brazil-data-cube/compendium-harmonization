#
# This file is part of research-processing library
# Copyright (C) 2021 INPE.
#
# research-processing is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""research-processing analysis processing solids."""

import os

from dagster import List, Tuple, String
from dagster import solid, OutputDefinition, InputDefinition

from research_processing import toolbox


@solid(
    input_defs=[
        InputDefinition(name="s2_scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2/MSI scenes that should be used "
                                    "for `sen2cor` processing.")
    ],
    output_defs=[
        OutputDefinition(name="s2_sen2cor_scene_path",
                         dagster_type=String,
                         description="Full path to the directory where the Sentinel-2/MSI scenes processed with "
                                    "`sen2cor` were saved."),
        OutputDefinition(name="s2_sen2cor_scene_ids",
                         dagster_type=List[String],
                         description="List with the name of each of the scenes that were processed. These names are"
                                     " equivalent to the name of the directories where each of the processed scenes "
                                     "were saved (Usually, you have the id of each of the scenes as the name of the "
                                     "directories)."),
    ],
    required_resource_keys={"repository"},
    description="Apply atmospheric correction using the `sen2cor` algorithm. The solid input indicates which scenes are "
                "to be processed from the Sentinel-2/MSI data repository."
)
def apply_sen2cor(context, s2_scene_ids: List[String]) -> Tuple[String, List[String]]:
    """Sen2Cor (Sentinel-2/MSI) Atmosphere correction."""
    from research_processing.surface_reflectance import sen2cor

    #
    # Prepare input/output directory.
    #
    input_dir = context.resources.repository["sentinel2_input_dir"]
    output_dir = context.resources.repository["outdir_sentinel2"]

    output_dir = toolbox.prepare_output_directory(output_dir, "s2_sen2cor_sr")

    #
    # Apply sen2cor.
    #
    sen2cor(input_dir, output_dir, s2_scene_ids)
    sen2cor_scene_ids = toolbox.filename(os.listdir(output_dir))

    return output_dir, sen2cor_scene_ids


@solid(
    input_defs=[
        InputDefinition(name="s2_scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2/MSI scenes that should be used "
                                    "for `LaSRC` processing.")
    ],
    output_defs=[
        OutputDefinition(name="s2_lasrc_scene_path",
                         dagster_type=String,
                         description="Full path to the directory where the Sentinel-2/MSI scenes processed with `LaSRC` were saved."),
        OutputDefinition(name="s2_lasrc_scene_ids",
                         dagster_type=List[String],
                         description="List with the name of each of the scenes that were processed. These names are"
                                     " equivalent to the name of the directories where each of the processed scenes "
                                     "were saved (Usually, you have the id of each of the scenes as the name of the "
                                     "directories)."
                         ),
    ],
    required_resource_keys={"lasrc_data", "repository"},
    description="Apply atmospheric correction using the `LaSRC` algorithm. The solid input indicates which scenes are "
                "to be processed from the Sentinel-2/MSI data repository."
)
def apply_lasrc(context, s2_scene_ids: List[String]) -> Tuple[String, List[String]]:
    """LaSRC (Sentinel-2/MSI) Atmosphere correction."""
    from research_processing.surface_reflectance import lasrc

    #
    # Prepare input/output directory.
    #
    input_dir = context.resources.repository["sentinel2_input_dir"]
    output_dir = context.resources.repository["outdir_sentinel2"]

    output_dir = toolbox.prepare_output_directory(output_dir, "s2_lasrc_sr")

    #
    # Defining the LaSRC auxiliary data.
    #
    auxiliary_data = context.resources.lasrc_data["lasrc_auxiliary_directory"]

    #
    # Applying LaSRC.
    #
    lasrc(input_dir, output_dir, s2_scene_ids, auxiliary_data)
    lasrc_scene_ids = toolbox.filename(os.listdir(output_dir))

    return output_dir, lasrc_scene_ids


@solid(
    input_defs=[
        InputDefinition(name="lc8_scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Landsat-8/OLI Level 2 scenes that should be used "
                                    "for NBAR Angles processing (Required step for NBAR processing "
                                    "on Landsat-8/OLI images).")
    ],
    output_defs=[
        OutputDefinition(name="lc8_nbar_angles",
                         dagster_type=List[String],
                         description="Name of each scene that had the angles generated."),
        OutputDefinition(name="lc8_nbar_angles_dir",
                         dagster_type=String,
                         description="Path to the directory where the generated scene angles were generated.")
    ],
    required_resource_keys={"repository"},
    description="Generate the angles of the Landsat-8/OLI scenes used for processing the NBAR products. The generated "
                "angles are saved in the scene directory."
)
def lc8_nbar_angles(context, lc8_scene_ids: List[String]) -> List[String]:
    """Landsat-8/OLI Angles for NBAR."""
    from research_processing.nbar import lc8_generate_angles

    #
    # Prepare input/output directory.
    #
    input_dir = context.resources.repository["landsat8_input_dir"]
    output_dir = context.resources.repository["outdir_landsat8"]

    output_dir = toolbox.prepare_output_directory(output_dir, "lc8_nbar_angles")

    #
    # Generate Landsat-8 Angles for NBAR calculation.
    #
    return output_dir, lc8_generate_angles(input_dir, output_dir, lc8_scene_ids)


@solid(
    input_defs=[
        InputDefinition(name="lc8_nbar_angles_dir",
                        dagster_type=String,
                        description="Path to the directory where the generated scene angles are stored."),
        InputDefinition(name="lc8_scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Landsat-8/OLI scenes that should be used "
                                    "for NBAR processing.")
    ],
    output_defs=[
        OutputDefinition(name="lc8_nbar_scene_path",
                         dagster_type=String,
                         description="Full path to the directory where the Landsat-8/OLI NBAR products were saved."),
        OutputDefinition(name="lc8_nbar_sceneid",
                         dagster_type=List[String],
                         description="List with the name of each NBAR product that were processed. These names are"
                                     " equivalent to the name of the directories where each of the processed scenes "
                                     "were saved."
                         ),
    ],
    required_resource_keys={"repository"},
    description="Generate the NBAR products using Landsat-8/OLI scenes."
)
def lc8_nbar(context, lc8_nbar_angles_dir: String, lc8_scene_ids: List[String]) -> Tuple[String, List[String]]:
    """Landsat-8/OLI NBAR."""
    from research_processing.nbar import lc8_nbar

    #
    # Prepare input/output directory.
    #
    input_dir = context.resources.repository["landsat8_input_dir"]
    output_dir = context.resources.repository["outdir_landsat8"]

    output_dir = toolbox.prepare_output_directory(output_dir, "lc8_nbar")

    #
    # Generate NBAR product for Landsat-8 scenes.
    #
    lc8_nbar(input_dir, lc8_nbar_angles_dir, output_dir, lc8_scene_ids)
    lc8_nbar_scene_ids = toolbox.filename(os.listdir(output_dir))

    return output_dir, lc8_nbar_scene_ids


@solid(
    input_defs=[
        InputDefinition(name="s2_sen2cor_dir",
                        dagster_type=String,
                        description="Path to the directory where the Sentinel-2/MSI scenes corrected "
                                    "with Sen2Cor are located. It is expected that the scenes used as input will have "
                                    "the influence of the atmosphere corrected with `sen2cor`."),
        InputDefinition(name="s2_scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2/MSI scenes that should be used "
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
                                     "Sentinel-2/MSI scenes. These names are equivalent to the name of the directories "
                                     "where each of the processed scenes were saved."
                         ),
    ],
    required_resource_keys={"repository"},
    description="Generate the NBAR products using Sentinel-2/MSI scenes (with sen2cor atmosphere correction)."
)
def s2_sen2cor_nbar(context, s2_sen2cor_dir: String, s2_scene_ids: List[String]) -> Tuple[String, List[String]]:
    """Sentinel-2 (with sen2cor atmosphere correction) NBAR."""
    from research_processing.nbar import s2_sen2cor_nbar

    #
    # Prepare output directory.
    #
    output_dir = context.resources.repository["outdir_sentinel2"]
    output_dir = toolbox.prepare_output_directory(output_dir, "s2_sen2cor_nbar")

    #
    # Generate NBAR product for Sentinel-2 scenes (corrected with LaSRC).
    #
    s2_sen2cor_nbar(s2_sen2cor_dir, output_dir, s2_scene_ids)
    s2_sen2cor_nbar_scene_ids = toolbox.filename(os.listdir(output_dir))

    return output_dir, s2_sen2cor_nbar_scene_ids


@solid(
    input_defs=[
        InputDefinition(name="s2_lasrc_dir",
                        dagster_type=String,
                        description="Path to the directory where the Sentinel-2/MSI scenes corrected "
                                    "with LaSRC are located. It is expected that the scenes used as input will have "
                                    "the influence of the atmosphere corrected with LaSRC."),
        InputDefinition(name="s2_scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2/MSI scenes that should be used "
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
                                     "Sentinel-2/MSI scenes. These names are equivalent to the name of the directories "
                                     "where each of the processed scenes were saved."
                         ),
    ],
    required_resource_keys={"repository"},
    description="Generate the NBAR products using Sentinel-2 scenes (with LaSRC atmosphere correction)."
)
def s2_lasrc_nbar(context, s2_lasrc_dir: String, s2_scene_ids: List[String]) -> Tuple[String, List[String]]:
    """Sentinel-2 (with LaSRC atmosphere correction) NBAR."""
    from research_processing.nbar import s2_lasrc_nbar

    #
    # Prepare output directory.
    #
    output_dir = context.resources.repository["outdir_sentinel2"]
    output_dir = toolbox.prepare_output_directory(output_dir, "s2_lasrc_nbar")

    #
    # Generate NBAR product for Sentinel-2 scenes (corrected with LaSRC).
    #
    s2_lasrc_nbar(s2_lasrc_dir, output_dir, s2_scene_ids)
    s2_lasrc_nbar_scene_ids = toolbox.filename(os.listdir(output_dir))

    return output_dir, s2_lasrc_nbar_scene_ids
