#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from typing import List

from dagster import solid, Field

from cfactor.toolbox import prepare_output_directory
from cfactor.validation import validation_funcs
from . import pipeline_utils


@solid(
    config_schema={
        "bands10m": Field(list, default_value=[
            "B02", "B03", "B04", "B08"
        ]),
        "bands20m": Field(list, default_value=[
            "B8A", "B11", "B12"
        ])
    }
)
def validation_sr_s2_sen2cor(context, input_dir: str, cloud_dir: str, output_dir: str, scene_ids: List) -> None:
    """
    """

    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_s2(pipeline_utils.create_a_temporary_file_with_lines(scene_ids))

    #
    # Prepare output directory
    #
    output_dir = prepare_output_directory(output_dir, "validation_sr_s2_sen2cor")

    #
    # Validate the results
    #
    pipeline_utils.validation_sr_s2_sen2cor(input_dir, cloud_dir, output_dir, pairs, **context.solid_config)


@solid(
    config_schema={
        "bands": Field(list, default_value=[
            "sr_band2", "sr_band3", "sr_band4", "sr_band8", "sr_band8a", "sr_band11", "sr_band12"
        ])
    }
)
def validation_sr_s2_lasrc(context, input_dir: str, cloud_dir: str, output_dir: str, scene_ids: List) -> None:
    """
    """

    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_s2(pipeline_utils.create_a_temporary_file_with_lines(scene_ids))

    #
    # Prepare output directory
    #
    output_dir = prepare_output_directory(output_dir, "validation_sr_s2_lasrc")

    #
    # Validate the results
    #
    pipeline_utils.validation_sr_s2_lasrc(input_dir, cloud_dir, output_dir, pairs, **context.solid_config)


@solid(
    config_schema={
        "bands": Field(list, default_value=["B2", "B3", "B4", "B5", "B6", "B7"])
    }
)
def validation_sr_l8(context, input_dir: str, cloud_dir: str, output_dir: str, scene_ids: List) -> None:
    """
    """
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8(pipeline_utils.create_a_temporary_file_with_lines(scene_ids))

    #
    # Prepare output directory
    #
    output_dir = prepare_output_directory(output_dir, "validation_sr_l8")

    #
    # Validate the results
    #
    pipeline_utils.validation_sr_l8(input_dir, cloud_dir, output_dir, pairs, context.solid_config["bands"])


@solid(
    config_schema={
        "bands": Field(list, default_value=["B2", "B3", "B4", "B5", "B6", "B7"])
    }
)
def validation_nbar_l8(context, input_dir: str, cloud_dir: str, output_dir: str, scene_ids: List) -> None:
    """
    """
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8(pipeline_utils.create_a_temporary_file_with_lines(scene_ids))

    #
    # Prepare output directory
    #
    output_dir = prepare_output_directory(output_dir, "validation_nbar_l8")

    #
    # Validate the results
    #
    pipeline_utils.validation_nbar_l8(input_dir, cloud_dir, output_dir, pairs, context.solid_config["bands"])


@solid(
    config_schema={
        "bands10m": Field(list, default_value=["B02", "B03", "B04", "B08"]),
        "bands20m": Field(list, default_value=["B8A", "B11", "B12"])
    }
)
def validation_nbar_s2_sen2cor(context, input_dir: str, cloud_dir: str, output_dir: str, scene_ids: List) -> None:
    """
    """
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_s2(pipeline_utils.create_a_temporary_file_with_lines(scene_ids))

    #
    # Prepare output directory
    #
    output_dir = prepare_output_directory(output_dir, "validation_nbar_s2_sen2cor")

    #
    # Validate the results
    #
    pipeline_utils.validation_nbar_s2_sen2cor(input_dir, cloud_dir, output_dir, pairs, **context.solid_config)


@solid(
    config_schema={
        "bands": Field(list, default_value=[
            "sr_band2", "sr_band3", "sr_band4", "sr_band8", "sr_band8a", "sr_band11", "sr_band12"
        ])
    }
)
def validation_nbar_s2_lasrc(context, input_dir: str, cloud_dir: str, output_dir: str, scene_ids: List) -> None:
    """
    """
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_s2(pipeline_utils.create_a_temporary_file_with_lines(scene_ids))

    #
    # Prepare output directory
    #
    output_dir = prepare_output_directory(output_dir, "validation_nbar_s2_lasrc")

    #
    # Validate the results
    #
    pipeline_utils.validation_nbar_s2_lasrc(input_dir, cloud_dir, output_dir, pairs, context.solid_config["bands"])


@solid(
    config_schema={
        "bands_l8": Field(list, default_value=[
            "B2", "B3", "B4", "B5", "B6", "B7"
        ]),
        "bands_s2": Field(list, default_value=[
            "B03", "B03", "B04", "B08", "B8A", "B11", "B12"
        ])
    }
)
def validation_sr_l8_s2_sen2cor(context, input_dir_l8: str, cloud_dir_l8: str, input_dir_s2: str, cloud_dir_s2: str,
                                output_dir: str, scene_ids_l8: List, scene_ids_s2: List) -> None:
    """
    """

    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8_s2(
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_l8),
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_s2)
    )

    #
    # Prepare output directory
    #
    output_dir = prepare_output_directory(output_dir, "validation_sr_l8_s2_sen2cor")

    #
    # Validate the results
    #
    pipeline_utils.validation_sr_l8_s2_sen2cor(input_dir_l8, cloud_dir_l8, input_dir_s2, cloud_dir_s2, output_dir,
                                               pairs, **context.solid_config)


@solid(
    config_schema={
        "bands_l8": Field(list, default_value=[
            "B2", "B3", "B4", "B5", "B6", "B7"
        ]),
        "bands_s2": Field(list, default_value=[
            "sr_band2", "sr_band3", "sr_band4", "sr_band8", "sr_band8a", "sr_band11", "sr_band12"
        ])
    }
)
def validation_sr_l8_s2_lasrc(context, input_dir_l8: str, cloud_dir_l8: str, input_dir_s2: str, cloud_dir_s2: str,
                              output_dir: str, scene_ids_l8: List, scene_ids_s2: List) -> None:
    """
    """

    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8_s2(
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_l8),
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_s2)
    )

    #
    # Prepare output directory
    #
    output_dir = prepare_output_directory(output_dir, "validation_sr_l8_s2_lasrc")

    #
    # Validate the results
    #
    pipeline_utils.validation_sr_l8_s2_lasrc(input_dir_l8, cloud_dir_l8, input_dir_s2, cloud_dir_s2, output_dir,
                                             pairs, **context.solid_config)


@solid(
    config_schema={
        "bands_l8": Field(list, default_value=[
            "B2", "B3", "B4", "B5", "B6", "B7"
        ]),
        "bands_s2": Field(list, default_value=[
            "sr_band2", "sr_band3", "sr_band4", "sr_band8", "sr_band8a", "sr_band11", "sr_band12"
        ])
    }
)
def validation_nbar_l8_s2_lasrc(context, input_dir_l8: str, cloud_dir_l8: str, input_dir_s2: str, cloud_dir_s2: str,
                                output_dir: str, scene_ids_l8: List, scene_ids_s2: List) -> None:
    """
    """

    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8_s2(
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_l8),
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_s2)
    )

    #
    # Prepare output directory
    #
    output_dir = prepare_output_directory(output_dir, "validation_nbar_l8_s2_lasrc")

    #
    # Validate the results
    #
    pipeline_utils.validation_nbar_l8_s2_lasrc(input_dir_l8, cloud_dir_l8, input_dir_s2, cloud_dir_s2, output_dir,
                                               pairs, **context.solid_config)


@solid(
    config_schema={
        "bands_l8": Field(list, default_value=[
            "B2", "B3", "B4", "B5", "B6", "B7"
        ]),
        "bands_s2": Field(list, default_value=[
            "B03", "B03", "B04", "B08", "B8A", "B11", "B12"
        ])
    }
)
def validation_nbar_l8_s2_sen2cor(context, input_dir_l8: str, cloud_dir_l8: str, input_dir_s2: str, cloud_dir_s2: str,
                                  output_dir: str, scene_ids_l8: List, scene_ids_s2: List) -> None:
    """
    """

    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8_s2(
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_l8),
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_s2)
    )

    #
    # Prepare output directory
    #
    output_dir = prepare_output_directory(output_dir, "validation_nbar_l8_s2_sen2cor")

    #
    # Validate the results
    #
    pipeline_utils.validation_nbar_l8_s2_sen2cor(input_dir_l8, cloud_dir_l8, input_dir_s2, cloud_dir_s2, output_dir,
                                                 pairs, **context.solid_config)
