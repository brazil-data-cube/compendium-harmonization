#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from dagster import Field, List, String
from dagster import solid, InputDefinition

from cfactor import toolbox
from cfactor.validation import validation_funcs
from . import pipeline_utils


@solid(
    input_defs=[
        InputDefinition(name="sen2cor_dir",
                        dagster_type=String,
                        description="Full path to the directory where the scenes processed with sen2cor were saved."),
        InputDefinition(name="sen2cor_cloud_dir",
                        dagster_type=String,
                        description="Full path to the directory where the scenes processed with sen2cor were saved"),
        InputDefinition(name="scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for the validation. These names are equivalent to the Sentinel-2 scene directories"
                                    " defined in the `cfactor_repository` resource.")
    ],
    config_schema={
        "bands10m": Field(
            config=list,
            description="Name of the spectral bands (spectral resolution = 10m) that will be used in the validation. "
                        "These names should be equivalent to the standard ESA Sentinel-2 .SAFE file band naming "
                        "pattern (e.g. B01, B02)",
            default_value=[
                "B02", "B03", "B04", "B08"
            ]
        ),
        "bands20m": Field(
            config=list,
            description="Name of the spectral bands (spectral resolution = 20m) that will be used in the validation. "
                        "These names should be equivalent to the standard ESA Sentinel-2 .SAFE file band naming "
                        "pattern (e.g. B01, B02)",
            default_value=[
                "B8A", "B11", "B12"
            ]
        )
    },
    required_resource_keys={"cfactor_repository"},
    description="Validate Sentinel-2 (with Se2Cor atmosphere correction) Surface Reflectance data."  # ToDo: Update
)
def validation_sr_s2_sen2cor(context, sen2cor_dir: String, sen2cor_cloud_dir: String, scene_ids: List[String]) -> None:
    """Validate Sentinel-2 (with Sen2Cor atmosphere correction) Surface Reflectance data."""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_s2(pipeline_utils.create_a_temporary_file_with_lines(scene_ids))

    #
    # Prepare output directory.
    #
    output_dir = context.resources.cfactor_repository["outdir_sentinel2"]
    output_dir = toolbox.prepare_output_directory(output_dir, "validation_sr_s2_sen2cor")

    #
    # Validate the results
    #
    pipeline_utils.validation_sr_s2_sen2cor(sen2cor_dir, sen2cor_cloud_dir, output_dir, pairs, **context.solid_config)


@solid(
    input_defs=[
        InputDefinition(name="lasrc_dir",
                        dagster_type=String,
                        description="Full path to the directory where the scenes processed with lasrc were saved."),
        InputDefinition(name="sen2cor_cloud_dir",
                        dagster_type=String,
                        description="Full path to the directory where the scenes processed with sen2cor were saved"),
        InputDefinition(name="scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for the validation. These names are equivalent to the Sentinel-2 scene directories"
                                    " defined in the `cfactor_repository` resource.")
    ],
    config_schema={
        "bands": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. "
                        "These names should be equivalent to the standard LaSRC file band naming "
                        "pattern (e.g. sr_band2, sr_band3, sr_band8a)",
            default_value=[
                "sr_band2", "sr_band3", "sr_band4", "sr_band8", "sr_band8a", "sr_band11", "sr_band12"
            ]
        )
    },
    required_resource_keys={"cfactor_repository"},
    description="Validate Sentinel-2 (with LaSRC atmosphere correction) Surface Reflectance data."  # ToDo: Update
)
def validation_sr_s2_lasrc(context, lasrc_dir: String, sen2cor_cloud_dir: String, scene_ids: List) -> None:
    """Validate Sentinel-2 (with LaSRC atmosphere correction) Surface Reflectance data."""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_s2(pipeline_utils.create_a_temporary_file_with_lines(scene_ids))

    #
    # Prepare output directory.
    #
    output_dir = context.resources.cfactor_repository["outdir_sentinel2"]
    output_dir = toolbox.prepare_output_directory(output_dir, "validation_sr_s2_lasrc")

    #
    # Validate the results
    #
    pipeline_utils.validation_sr_s2_lasrc(lasrc_dir, sen2cor_cloud_dir, output_dir, pairs, **context.solid_config)


@solid(
    input_defs=[
        InputDefinition(name="scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Landsat-8 scenes that should be used "
                                    "for the validation. These names are equivalent to the Landsat-8 scene directories"
                                    " defined in the `cfactor_repository` resource.")
    ],
    config_schema={
        "bands": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. These names should be "
                        "equivalent to the standard USGS Landsat-8 file band naming pattern (e.g. B1, B2)",
            default_value=["B2", "B3", "B4", "B5", "B6", "B7"]
        )
    },
    required_resource_keys={"cfactor_repository"},
    description="Validate Landsat-8 Surface Reflectance data."  # ToDo: Update
)
def validation_sr_l8(context, scene_ids: List) -> None:
    """Validate Landsat-8 Surface Reflectance data."""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8(pipeline_utils.create_a_temporary_file_with_lines(scene_ids))

    #
    # Prepare input/output directory.
    #
    landsat8_dir = context.resources.cfactor_repository["landsat8_input_dir"]
    output_dir = context.resources.cfactor_repository["outdir_landsat8"]

    output_dir = toolbox.prepare_output_directory(output_dir, "validation_sr_l8")

    #
    # Validate the results
    #
    pipeline_utils.validation_sr_l8(landsat8_dir, landsat8_dir, output_dir, pairs, context.solid_config["bands"])


@solid(
    input_defs=[
        InputDefinition(name="lc8_nbar_dir",
                        dagster_type=String,
                        description="Full path to the directory where the Landsat-8 NBAR products were saved."),
        InputDefinition(name="scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Landsat-8 scenes that should be used "
                                    "for the validation. These names are equivalent to the Landsat-8 scene directories"
                                    " defined in the `cfactor_repository` resource.")
    ],
    config_schema={
        "bands": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. These names should be "
                        "equivalent to the standard USGS Landsat-8 file band naming pattern (e.g. B1, B2)",
            default_value=["B2", "B3", "B4", "B5", "B6", "B7"]
        )
    },
    required_resource_keys={"cfactor_repository"},
    description="Validate Landsat-8 NBAR data."  # TODO: Update
)
def validation_nbar_l8(context, lc8_nbar_dir: String, scene_ids: List[String]) -> None:
    """Validate Landsat-8 NBAR data."""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8(pipeline_utils.create_a_temporary_file_with_lines(scene_ids))

    #
    # Prepare input/output directory.
    #
    landsat8_dir = context.resources.cfactor_repository["landsat8_input_dir"]
    output_dir = context.resources.cfactor_repository["outdir_landsat8"]

    output_dir = toolbox.prepare_output_directory(output_dir, "validation_nbar_l8")

    #
    # Validate the results
    #
    pipeline_utils.validation_nbar_l8(lc8_nbar_dir, landsat8_dir, output_dir, pairs, context.solid_config["bands"])


@solid(
    input_defs=[
        InputDefinition(name="s2_sen2cor_nbar_dir",
                        dagster_type=String,
                        description="Full path to the directory where the NBAR products, generated with Sen2Cor, "
                                    "were saved."),
        InputDefinition(name="sen2cor_cloud_dir",
                        dagster_type=String,
                        description="Full path to the directory where the scenes processed with sen2cor were saved."),
        InputDefinition(name="scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for the validation. These names are equivalent to the Sentinel-2 scene directories"
                                    " defined in the `cfactor_repository` resource.")
    ],
    config_schema={
        "bands10m": Field(
            config=list,
            description="Name of the spectral bands (spectral resolution = 10m) that will be used in the validation."
                        "These names should be equivalent to the standard ESA Sentinel-2 .SAFE file band naming "
                        "pattern (e.g. B01, B02)",
            default_value=[
                "B02", "B03", "B04", "B08"
            ]
        ),
        "bands20m": Field(
            config=list,
            description="Name of the spectral bands (spectral resolution = 20m) that will be used in the validation. "
                        "These names should be equivalent to the standard ESA Sentinel-2 .SAFE file band naming "
                        "pattern (e.g. B01, B02)",
            default_value=[
                "B8A", "B11", "B12"
            ]
        )
    },
    required_resource_keys={"cfactor_repository"},
    description="Validate Sentinel-2 (with Sen2Cor atmosphere correction) NBAR data."  # TODO: Update
)
def validation_nbar_s2_sen2cor(context, s2_sen2cor_nbar_dir: String, sen2cor_cloud_dir: String,
                               scene_ids: List[String]) -> None:
    """Validate Sentinel-2 (with Sen2Cor atmosphere correction) NBAR data."""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_s2(pipeline_utils.create_a_temporary_file_with_lines(scene_ids))

    #
    # Prepare output directory.
    #
    output_dir = context.resources.cfactor_repository["outdir_sentinel2"]
    output_dir = toolbox.prepare_output_directory(output_dir, "validation_nbar_s2_sen2cor")

    #
    # Validate the results
    #
    pipeline_utils.validation_nbar_s2_sen2cor(s2_sen2cor_nbar_dir, sen2cor_cloud_dir, output_dir, pairs,
                                              **context.solid_config)


@solid(
    input_defs=[
        InputDefinition(name="s2_lasrc_nbar_dir",
                        dagster_type=String,
                        description="Full path to the directory where the NBAR products, generated with LaSRC,"
                                    " were saved."),
        InputDefinition(name="sen2cor_cloud_dir",
                        dagster_type=String,
                        description="Full path to the directory where the scenes processed with sen2cor were saved."),
        InputDefinition(name="scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for the validation. These names are equivalent to the Sentinel-2 scene directories"
                                    " defined in the `cfactor_repository` resource.")
    ],
    config_schema={
        "bands": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. "
                        "These names should be equivalent to the standard LaSRC file band naming "
                        "pattern (e.g. sr_band2, sr_band3, sr_band8a)",
            default_value=[
                "sr_band2", "sr_band3", "sr_band4", "sr_band8", "sr_band8a", "sr_band11", "sr_band12"
            ]
        )
    },
    required_resource_keys={"cfactor_repository"},
    description="Validate Sentinel-2 (with LaSRC atmosphere correction) NBAR data."  # TODO: Update
)
def validation_nbar_s2_lasrc(context, s2_lasrc_nbar_dir: String, sen2cor_cloud_dir: String, scene_ids: List) -> None:
    """Validate Sentinel-2 (with LaSRC atmosphere correction) NBAR data."""
    #
    # Search for pairs.
    #
    pairs = validation_funcs.search_pairs_s2(pipeline_utils.create_a_temporary_file_with_lines(scene_ids))

    #
    # Prepare output directory.
    #
    output_dir = context.resources.cfactor_repository["outdir_sentinel2"]
    output_dir = toolbox.prepare_output_directory(output_dir, "validation_nbar_s2_lasrc")

    #
    # Validate the results.
    #
    pipeline_utils.validation_nbar_s2_lasrc(s2_lasrc_nbar_dir, sen2cor_cloud_dir, output_dir, pairs,
                                            context.solid_config["bands"])


@solid(
    input_defs=[
        InputDefinition(name="sen2cor_dir",
                        dagster_type=String,
                        description="Full path to the directory where the scenes processed with sen2cor were saved."),
        InputDefinition(name="sen2cor_cloud_dir",
                        dagster_type=String,
                        description="Full path to the directory where the scenes processed with sen2cor were saved"),
        InputDefinition(name="scene_ids_l8",
                        dagster_type=List[String],
                        description="List with the name of the Landsat-8 scenes that should be used "
                                    "for the validation. These names are equivalent to the Landsat-8 scene directories"
                                    " defined in the `cfactor_repository` resource."),
        InputDefinition(name="scene_ids_s2",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for the validation. These names are equivalent to the Sentinel-2 scene directories"
                                    " defined in the `cfactor_repository` resource.")
    ],
    config_schema={
        "bands_l8": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. These names should be "
                        "equivalent to the standard USGS Landsat-8 file band naming pattern (e.g. B1, B2)",
            default_value=[
                "B2", "B3", "B4", "B5", "B6", "B7"
            ],
        ),
        "bands_s2": Field(
            config=list,
            description="Name of the spectral bands (spectral resolution = 10m and 20m) that will be used in the "
                        "validation. These names should be equivalent to the standard ESA Sentinel-2 .SAFE file "
                        "band naming pattern (e.g. B01, B02, B8A)",
            default_value=[
                "B03", "B03", "B04", "B08", "B8A", "B11", "B12"
            ]
        )
    },
    required_resource_keys={"cfactor_repository"},
    description="Compare Sentinel-2 (with Sen2Cor atmosphere correction) and Landsat-8 SR."  # TODO: Update
)
def validation_sr_l8_s2_sen2cor(context, sen2cor_dir: String, sen2cor_cloud_dir: String, scene_ids_l8: List[String],
                                scene_ids_s2: List[String]) -> None:
    """Compare Sentinel-2 (with Sen2Cor atmosphere correction) and Landsat-8 SR."""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8_s2(
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_l8),
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_s2)
    )

    #
    # Prepare input/output directory.
    #
    landsat8_dir = context.resources.cfactor_repository["landsat8_input_dir"]

    output_dir_s2 = context.resources.cfactor_repository["outdir_sentinel2"]
    output_dir = toolbox.prepare_output_directory(output_dir_s2, "validation_sr_l8_s2_sen2cor")

    #
    # Validate the results
    #
    pipeline_utils.validation_sr_l8_s2_sen2cor(landsat8_dir, landsat8_dir, sen2cor_dir, sen2cor_cloud_dir, output_dir,
                                               pairs, **context.solid_config)


@solid(
    input_defs=[
        InputDefinition(name="lasrc_dir",
                        dagster_type=String,
                        description="Full path to the directory where the scenes processed with lasrc were saved."),
        InputDefinition(name="sen2cor_cloud_dir",
                        dagster_type=String,
                        description="Full path to the directory where the scenes processed with sen2cor were saved"),
        InputDefinition(name="scene_ids_l8",
                        dagster_type=List[String],
                        description="List with the name of the Landsat-8 scenes that should be used "
                                    "for the validation. These names are equivalent to the Landsat-8 scene directories"
                                    " defined in the `cfactor_repository` resource."),
        InputDefinition(name="scene_ids_s2",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for the validation. These names are equivalent to the Sentinel-2 scene directories"
                                    " defined in the `cfactor_repository` resource.")
    ],
    config_schema={
        "bands_l8": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. These names should be "
                        "equivalent to the standard USGS Landsat-8 file band naming pattern (e.g. B1, B2).",
            default_value=[
                "B2", "B3", "B4", "B5", "B6", "B7"
            ]
        ),
        "bands_s2": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. "
                        "These names should be equivalent to the standard LaSRC file band naming "
                        "pattern (e.g. sr_band2, sr_band3, sr_band8a).",
            default_value=[
                "sr_band2", "sr_band3", "sr_band4", "sr_band8", "sr_band8a", "sr_band11", "sr_band12"
            ]
        )
    },
    required_resource_keys={"cfactor_repository"},
    description="Compare Sentinel-2 (with LaSRC atmosphere correction) and Landsat-8 SR."  # TODO: Update
)
def validation_sr_l8_s2_lasrc(context, lasrc_dir: String, sen2cor_cloud_dir: String, scene_ids_l8: List[String],
                              scene_ids_s2: List[String]) -> None:
    """Compare Sentinel-2 (with LaSRC atmosphere correction) and Landsat-8 SR."""
    #
    # Search for pairs.
    #
    pairs = validation_funcs.search_pairs_l8_s2(
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_l8),
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_s2)
    )

    #
    # Prepare input/output directory.
    #
    landsat8_dir = context.resources.cfactor_repository["landsat8_input_dir"]

    output_dir_s2 = context.resources.cfactor_repository["outdir_sentinel2"]
    output_dir = toolbox.prepare_output_directory(output_dir_s2, "validation_sr_l8_s2_lasrc")

    #
    # Validate the results
    #
    pipeline_utils.validation_sr_l8_s2_lasrc(landsat8_dir, landsat8_dir, lasrc_dir, sen2cor_cloud_dir, output_dir,
                                             pairs, **context.solid_config)


@solid(
    input_defs=[
        InputDefinition(name="lc8_nbar_dir",
                        dagster_type=String,
                        description="Full path to the directory where the Landsat-8 NBAR products were saved."),
        InputDefinition(name="s2_sen2cor_nbar_dir",
                        dagster_type=String,
                        description="Full path to the directory where the NBAR products, generated with Sen2Cor, "
                                    "were saved."),
        InputDefinition(name="sen2cor_cloud_dir",
                        dagster_type=String,
                        description="Full path to the directory where the scenes processed with sen2cor were saved"),
        InputDefinition(name="scene_ids_l8",
                        dagster_type=List[String],
                        description="List with the name of the Landsat-8 scenes that should be used "
                                    "for the validation. These names are equivalent to the Landsat-8 scene directories"
                                    " defined in the `cfactor_repository` resource."),
        InputDefinition(name="scene_ids_s2",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for the validation. These names are equivalent to the Sentinel-2 scene directories"
                                    " defined in the `cfactor_repository` resource.")
    ],
    config_schema={
        "bands_l8": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. These names should be "
                        "equivalent to the standard USGS Landsat-8 file band naming pattern (e.g. B1, B2).",
            default_value=[
                "B2", "B3", "B4", "B5", "B6", "B7"
            ]
        ),
        "bands_s2": Field(
            config=list,
            description="Name of the spectral bands (spectral resolution = 10m and 20m) that will be used in the "
                        "validation. These names should be equivalent to the standard ESA Sentinel-2 .SAFE file "
                        "band naming pattern (e.g. B01, B02, B8A)",
            default_value=[
                "B03", "B03", "B04", "B08", "B8A", "B11", "B12"
            ]
        )
    },
    required_resource_keys={"cfactor_repository"},
    description="Compare NBAR Products of Sentinel-2 (with Sen2Cor atmosphere correction) and Landsat-8."
    # TODO: Update
)
def validation_nbar_l8_s2_sen2cor(context, lc8_nbar_dir: String, s2_sen2cor_nbar_dir: str,
                                  sen2cor_cloud_dir: String, scene_ids_l8: List[String],
                                  scene_ids_s2: List[String]) -> None:
    """Compare NBAR Products of Sentinel-2 (with Sen2Cor atmosphere correction) and Landsat-8."""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8_s2(
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_l8),
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_s2)
    )

    #
    # Prepare input/output directory.
    #
    landsat8_dir = context.resources.cfactor_repository["landsat8_input_dir"]

    output_dir_s2 = context.resources.cfactor_repository["outdir_sentinel2"]
    output_dir = toolbox.prepare_output_directory(output_dir_s2, "validation_nbar_l8_s2_sen2cor")

    #
    # Validate the results
    #
    pipeline_utils.validation_nbar_l8_s2_sen2cor(lc8_nbar_dir, landsat8_dir, s2_sen2cor_nbar_dir, sen2cor_cloud_dir,
                                                 output_dir, pairs, **context.solid_config)


@solid(
    input_defs=[
        InputDefinition(name="lc8_nbar_dir",
                        dagster_type=String,
                        description="Full path to the directory where the Landsat-8 NBAR products were saved."),
        InputDefinition(name="s2_lasrc_nbar_dir",
                        dagster_type=String,
                        description="Full path to the directory where the NBAR products, generated with LaSRC, "
                                    "were saved."),
        InputDefinition(name="sen2cor_cloud_dir",
                        dagster_type=String,
                        description="Full path to the directory where the scenes processed with sen2cor were saved"),
        InputDefinition(name="scene_ids_l8",
                        dagster_type=List[String],
                        description="List with the name of the Landsat-8 scenes that should be used "
                                    "for the validation. These names are equivalent to the Landsat-8 scene directories"
                                    " defined in the `cfactor_repository` resource."),
        InputDefinition(name="scene_ids_s2",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for the validation. These names are equivalent to the Sentinel-2 scene directories"
                                    " defined in the `cfactor_repository` resource.")
    ],
    config_schema={
        "bands_l8": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. These names should be "
                        "equivalent to the standard USGS Landsat-8 file band naming pattern (e.g. B1, B2).",
            default_value=[
                "B2", "B3", "B4", "B5", "B6", "B7"
            ]
        ),
        "bands_s2": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. "
                        "These names should be equivalent to the standard LaSRC file band naming "
                        "pattern (e.g. sr_band2, sr_band3, sr_band8a).",
            default_value=[
                "sr_band2", "sr_band3", "sr_band4", "sr_band8", "sr_band8a", "sr_band11", "sr_band12"
            ]
        )
    },
    required_resource_keys={"cfactor_repository"},
    description="Compare NBAR Products of Sentinel-2 (with Sen2Cor atmosphere correction) and Landsat-8."
    # TODO: Update
)
def validation_nbar_l8_s2_lasrc(context, lc8_nbar_dir: String, s2_lasrc_nbar_dir: String, sen2cor_cloud_dir: String,
                                scene_ids_l8: List, scene_ids_s2: List) -> None:
    """Compare NBAR Products of Sentinel-2 (with Sen2Cor atmosphere correction) and Landsat-8."""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8_s2(
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_l8),
        pipeline_utils.create_a_temporary_file_with_lines(scene_ids_s2)
    )

    #
    # Prepare input/output directory.
    #
    landsat8_dir = context.resources.cfactor_repository["landsat8_input_dir"]

    output_dir_s2 = context.resources.cfactor_repository["outdir_sentinel2"]
    output_dir = toolbox.prepare_output_directory(output_dir_s2, "validation_nbar_l8_s2_lasrc")

    #
    # Validate the results
    #
    pipeline_utils.validation_nbar_l8_s2_lasrc(lc8_nbar_dir, landsat8_dir, s2_lasrc_nbar_dir, sen2cor_cloud_dir,
                                               output_dir, pairs, **context.solid_config)
