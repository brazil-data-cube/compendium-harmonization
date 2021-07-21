#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os
from typing import Any, List, Tuple

from dagster import solid, OutputDefinition

from . import pipeline_utils


@solid(
    config_schema={
        "landsat8_input_dir": str,
        "landsat8_sceneid_list": str,

        "sentinel2_input_dir": str,
        "sentinel2_sceneid_list": str,

        "derived_data_dir": str
    }, output_defs=[
        # Landsat-8
        OutputDefinition(name="landsat8_input_dir"),
        OutputDefinition(name="landsat8_sceneid_list"),

        # Sentinel-2
        OutputDefinition(name="sentinel2_input_dir"),
        OutputDefinition(name="sentinel2_sceneid_list"),

        # General
        OutputDefinition(name="outdir_landsat8"),
        OutputDefinition(name="outdir_sentinel2"),
    ])
def config_gatter(context) -> Tuple[Any, List[str], Any, List[str], str, str]:
    """Configure and validate the input data before start pipeline"""

    #
    # Load Sentinel-2 scenes
    #
    with open(context.solid_config["sentinel2_sceneid_list"]) as file:
        scene_list = file.readlines()
        sentinel2_sceneids = pipeline_utils.standardize_filename(scene_list)

    #
    # Load Landsat-8 scenes
    #
    with open(context.solid_config["landsat8_sceneid_list"]) as file:
        scene_list = file.readlines()
        landsat8_sceneids = pipeline_utils.standardize_filename(scene_list)

    if len(landsat8_sceneids) != len(sentinel2_sceneids):
        raise RuntimeError("It is necessary to have the same amount of "
                           "landsat-8 and sentinel-2 scenes")

    # create base output directories (for each sensor)
    base_out_dir = context.solid_config["derived_data_dir"]

    s2_outputs = os.path.join(base_out_dir, "s2")
    lc8_outputs = os.path.join(base_out_dir, "lc8")

    return (
        context.solid_config["landsat8_input_dir"],
        landsat8_sceneids,

        context.solid_config["sentinel2_input_dir"],
        sentinel2_sceneids,

        lc8_outputs,
        s2_outputs
    )


@solid(
    output_defs=[
        OutputDefinition(name="sen2cor_sceneid"),
        OutputDefinition(name="sen2cor_scene_path"),
    ]
)
def apply_sen2cor(input_dir: str, output_dir: str,
                  scene_ids: List) -> Tuple[str, List[str]]:
    from cfactor.surface_reflectance import sen2cor

    #
    # Prepare output directory
    #
    output_dir = pipeline_utils.prepare_output_directory(
        output_dir, "sen2cor_sr"
    )

    sen2cor(input_dir, output_dir, scene_ids)
    sen2cor_scene_ids = pipeline_utils.filename(os.listdir(output_dir))

    return output_dir, sen2cor_scene_ids


@solid(config_schema={
    "auxiliary_data": str,
}, output_defs=[
    OutputDefinition(name="lasrc_sceneid"),
    OutputDefinition(name="lasrc_scene_path"),
])
def apply_lasrc(context, input_dir: str, output_dir: str,
                scene_ids: List) -> Tuple[str, List[str]]:
    """
    """
    from cfactor.surface_reflectance import lasrc

    #
    # Prepare output directory
    #
    output_dir = pipeline_utils.prepare_output_directory(
        output_dir, "lasrc_sr"
    )

    # select auxiliary data
    auxiliary_data = context.solid_config["auxiliary_data"]

    lasrc(input_dir, output_dir, scene_ids, auxiliary_data)
    lasrc_scene_ids = pipeline_utils.filename(os.listdir(output_dir))

    return output_dir, lasrc_scene_ids


@solid(output_defs=[
    OutputDefinition(name="lc8_nbar_angles"),
])
def lc8_nbar_angles(input_dir: str, scene_ids: List[str]) -> List[str]:
    """
    """

    from cfactor.nbar import lc8_generate_angles

    return lc8_generate_angles(input_dir, scene_ids)


@solid(
    output_defs=[
        OutputDefinition(name="lc8_nbar_sceneid"),
        OutputDefinition(name="lc8_nbar_scene_path"),
    ])
def lc8_nbar(input_dir: str, output_dir: str, scene_ids: List[str]) -> Tuple[str, List[str]]:
    """
    """

    from cfactor.nbar import lc8_nbar

    #
    # Prepare output directory
    #
    output_dir = pipeline_utils.prepare_output_directory(
        output_dir, "lc8_nbar"
    )

    lc8_nbar(input_dir, output_dir, scene_ids)
    lc8_nbar_scene_ids = pipeline_utils.filename(os.listdir(output_dir))

    return output_dir, lc8_nbar_scene_ids


@solid(
    output_defs=[
        OutputDefinition(name="s2_sen2cor_nbar_sceneid"),
        OutputDefinition(name="s2_sen2cor_nbar_scene_path"),
    ]
)
def s2_sen2cor_nbar(input_dir: str, output_dir: str, scene_ids: List[str]):
    """
    """
    from cfactor.nbar import s2_sen2cor_nbar

    #
    # Prepare output directory
    #
    output_dir = pipeline_utils.prepare_output_directory(
        output_dir, "s2_sen2cor_nbar"
    )

    s2_sen2cor_nbar(input_dir, output_dir, scene_ids)
    s2_sen2cor_nbar_scene_ids = pipeline_utils.filename(os.listdir(output_dir))

    return output_dir, s2_sen2cor_nbar_scene_ids


@solid(
    output_defs=[
        OutputDefinition(name="s2_lasrc_nbar_sceneid"),
        OutputDefinition(name="s2_lasrc_nbar_scene_path"),
    ]
)
def s2_lasrc_nbar(input_dir: str, output_dir: str, scene_ids: List[str]):
    """
    """
    from cfactor.nbar import s2_lasrc_nbar

    #
    # Prepare output directory
    #
    output_dir = pipeline_utils.prepare_output_directory(
        output_dir, "s2_lasrc_nbar"
    )

    s2_lasrc_nbar(input_dir, output_dir, scene_ids)
    s2_lasrc_nbar_scene_ids = pipeline_utils.filename(os.listdir(output_dir))

    return output_dir, s2_lasrc_nbar_scene_ids
