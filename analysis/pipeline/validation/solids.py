#
# This file is part of research-processing library
# Copyright (C) 2021 INPE.
#
# research-processing is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from dagster import Field, List, String
from dagster import solid, InputDefinition

from research_processing import toolbox
from research_processing.validation import validation_funcs
from research_processing.validation import validation_routines


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
                                    " defined in the `repository` resource.")
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
        ),
        "day_difference": Field(
            config=int,
            description="Difference of sensing date, in days, to consider two sceneids a pair.",
            default_value=5,
        )
    },
    required_resource_keys={"repository"},
    description="Validate (Compare) Sentinel-2 (with Se2Cor atmosphere correction) Surface Reflectance images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."
)
def validation_sr_s2_sen2cor(context, sen2cor_dir: String, sen2cor_cloud_dir: String, scene_ids: List[String]) -> None:
    """Validate (Compare) Sentinel-2 (with Se2Cor atmosphere correction) Surface Reflectance images, of the same spatial location, acquired with a sensing date difference up to `day_difference`"""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_s2(validation_routines.create_a_temporary_file_with_lines(scene_ids),
                                             day_diff=context.solid_config["day_difference"])

    #
    # Prepare output directory.
    #
    output_dir = context.resources.repository["outdir_validation"]
    output_dir = toolbox.prepare_output_directory(output_dir, "validation_sr_s2_sen2cor")

    #
    # Validate the results
    #
    validation_routines.validation_sr_s2_sen2cor(sen2cor_dir, sen2cor_cloud_dir, output_dir, pairs,
                                                 **{
                                                     "bands10m": context.solid_config["bands10m"],
                                                     "bands20m": context.solid_config["bands20m"]
                                                 })


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
                                    " defined in the `repository` resource.")
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
        ),
        "day_difference": Field(
            config=int,
            description="Difference of sensing date, in days, to consider two sceneids a pair.",
            default_value=5,
        )
    },
    required_resource_keys={"repository"},
    description="Validate (Compare) Sentinel-2 (with LaSRC atmosphere correction) Surface Reflectance images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."
)
def validation_sr_s2_lasrc(context, lasrc_dir: String, sen2cor_cloud_dir: String, scene_ids: List) -> None:
    """Validate (Compare) Sentinel-2 (with LaSRC atmosphere correction) Surface Reflectance images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_s2(validation_routines.create_a_temporary_file_with_lines(scene_ids),
                                             day_diff=context.solid_config["day_difference"])

    #
    # Prepare output directory.
    #
    output_dir = context.resources.repository["outdir_validation"]
    output_dir = toolbox.prepare_output_directory(output_dir, "validation_sr_s2_lasrc")

    #
    # Validate the results
    #
    validation_routines.validation_sr_s2_lasrc(lasrc_dir, sen2cor_cloud_dir, output_dir, pairs,
                                               context.solid_config["bands"])


@solid(
    input_defs=[
        InputDefinition(name="scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Landsat-8 scenes that should be used "
                                    "for the validation. These names are equivalent to the Landsat-8 scene directories"
                                    " defined in the `repository` resource.")
    ],
    config_schema={
        "bands": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. These names should be "
                        "equivalent to the standard USGS Landsat-8 file band naming pattern (e.g. B1, B2)",
            default_value=["B2", "B3", "B4", "B5", "B6", "B7"]
        ),
        "day_difference": Field(
            config=int,
            description="Difference of sensing date, in days, to consider two sceneids a pair.",
            default_value=10,
        )
    },
    required_resource_keys={"repository"},
    description="Validate (Compare) Landsat-8 Surface Reflectance images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."
)
def validation_sr_l8(context, scene_ids: List) -> None:
    """Validate (Compare) Landsat-8 Surface Reflectance images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8(validation_routines.create_a_temporary_file_with_lines(scene_ids),
                                             day_diff=context.solid_config["day_difference"])

    #
    # Prepare input/output directory.
    #
    landsat8_dir = context.resources.repository["landsat8_input_dir"]
    output_dir = context.resources.repository["outdir_validation"]

    output_dir = toolbox.prepare_output_directory(output_dir, "validation_sr_l8")

    #
    # Validate the results
    #
    validation_routines.validation_sr_l8(landsat8_dir, landsat8_dir, output_dir, pairs, context.solid_config["bands"])


@solid(
    input_defs=[
        InputDefinition(name="lc8_nbar_dir",
                        dagster_type=String,
                        description="Full path to the directory where the Landsat-8 NBAR products were saved."),
        InputDefinition(name="scene_ids",
                        dagster_type=List[String],
                        description="List with the name of the Landsat-8 scenes that should be used "
                                    "for the validation. These names are equivalent to the Landsat-8 scene directories"
                                    " defined in the `repository` resource.")
    ],
    config_schema={
        "bands": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. These names should be "
                        "equivalent to the standard USGS Landsat-8 file band naming pattern (e.g. B1, B2)",
            default_value=["B2", "B3", "B4", "B5", "B6", "B7"]
        ),
        "day_difference": Field(
            config=int,
            description="Difference of sensing date, in days, to consider two sceneids a pair.",
            default_value=10,
        )
    },
    required_resource_keys={"repository"},
    description="Validate (Compare) Landsat-8 NBAR images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."
)
def validation_nbar_l8(context, lc8_nbar_dir: String, scene_ids: List[String]) -> None:
    """Validate (Compare) Landsat-8 NBAR images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8(validation_routines.create_a_temporary_file_with_lines(scene_ids),
                                             day_diff=context.solid_config["day_difference"])

    #
    # Prepare input/output directory.
    #
    landsat8_dir = context.resources.repository["landsat8_input_dir"]
    output_dir = context.resources.repository["outdir_validation"]

    output_dir = toolbox.prepare_output_directory(output_dir, "validation_nbar_l8")

    #
    # Validate the results
    #
    validation_routines.validation_nbar_l8(lc8_nbar_dir, landsat8_dir, output_dir, pairs, context.solid_config["bands"])


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
                                    " defined in the `repository` resource.")
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
        ),
        "day_difference": Field(
            config=int,
            description="Difference of sensing date, in days, to consider two sceneids a pair.",
            default_value=5,
        )
    },
    required_resource_keys={"repository"},
    description="Validate (Compare) Sentinel-2 (with Sen2Cor atmosphere correction) NBAR images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."
)
def validation_nbar_s2_sen2cor(context, s2_sen2cor_nbar_dir: String, sen2cor_cloud_dir: String,
                               scene_ids: List[String]) -> None:
    """Validate (Compare) Sentinel-2 (with Sen2Cor atmosphere correction) NBAR images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_s2(validation_routines.create_a_temporary_file_with_lines(scene_ids),
                                             day_diff=context.solid_config["day_difference"])

    #
    # Prepare output directory.
    #
    output_dir = context.resources.repository["outdir_validation"]
    output_dir = toolbox.prepare_output_directory(output_dir, "validation_nbar_s2_sen2cor")

    #
    # Validate the results
    #
    validation_routines.validation_nbar_s2_sen2cor(s2_sen2cor_nbar_dir, sen2cor_cloud_dir, output_dir, pairs,
                                                   **{
                                                       "bands10m": context.solid_config["bands10m"],
                                                       "bands20m": context.solid_config["bands20m"]
                                                   })


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
                                    " defined in the `repository` resource.")
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
        ),
        "day_difference": Field(
            config=int,
            description="Difference of sensing date, in days, to consider two sceneids a pair.",
            default_value=5,
        )
    },
    required_resource_keys={"repository"},
    description="Validate (Compare) Sentinel-2 (with LaSRC atmosphere correction) NBAR images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."
)
def validation_nbar_s2_lasrc(context, s2_lasrc_nbar_dir: String, sen2cor_cloud_dir: String, scene_ids: List) -> None:
    """Validate (Compare) Sentinel-2 (with LaSRC atmosphere correction) NBAR images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."""
    #
    # Search for pairs.
    #
    pairs = validation_funcs.search_pairs_s2(validation_routines.create_a_temporary_file_with_lines(scene_ids),
                                             day_diff=context.solid_config["day_difference"])

    #
    # Prepare output directory.
    #
    output_dir = context.resources.repository["outdir_validation"]
    output_dir = toolbox.prepare_output_directory(output_dir, "validation_nbar_s2_lasrc")

    #
    # Validate the results.
    #
    validation_routines.validation_nbar_s2_lasrc(s2_lasrc_nbar_dir, sen2cor_cloud_dir, output_dir, pairs,
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
                                    " defined in the `repository` resource."),
        InputDefinition(name="scene_ids_s2",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for the validation. These names are equivalent to the Sentinel-2 scene directories"
                                    " defined in the `repository` resource.")
    ],
    config_schema={
        "bands_l8": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. These names should be "
                        "equivalent to the standard USGS Landsat-8 file band naming pattern (e.g. B1, B2)",
            default_value=[
                "B2", "B3", "B4", "B5", "B5", "B6", "B7"
            ],
        ),
        "bands_s2": Field(
            config=list,
            description="Name of the spectral bands (spectral resolution = 10m and 20m) that will be used in the "
                        "validation. These names should be equivalent to the standard ESA Sentinel-2 .SAFE file "
                        "band naming pattern (e.g. B01, B02, B8A)",
            default_value=[
                "B02", "B03", "B04", "B08", "B8A", "B11", "B12"
            ]
        ),
        "day_difference": Field(
            config=int,
            description="Difference of sensing date, in days, to consider two sceneids a pair.",
            default_value=5,
        )
    },
    required_resource_keys={"repository"},
    description="Validate (Compare) Sentinel-2 (with Sen2Cor atmosphere correction) and Landsat-8 Surface Reflectance images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."
)
def validation_sr_l8_s2_sen2cor(context, sen2cor_dir: String, sen2cor_cloud_dir: String, scene_ids_l8: List[String],
                                scene_ids_s2: List[String]) -> None:
    """Validate (Compare) Sentinel-2 (with Sen2Cor atmosphere correction) and Landsat-8 Surface Reflectance images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8_s2(
        validation_routines.create_a_temporary_file_with_lines(scene_ids_l8),
        validation_routines.create_a_temporary_file_with_lines(scene_ids_s2),
        day_diff=context.solid_config["day_difference"])

    #
    # Prepare input/output directory.
    #
    landsat8_dir = context.resources.repository["landsat8_input_dir"]

    output_dir_s2 = context.resources.repository["outdir_validation"]
    output_dir = toolbox.prepare_output_directory(output_dir_s2, "validation_sr_l8_s2_sen2cor")

    #
    # Validate the results
    #
    validation_routines.validation_sr_l8_s2_sen2cor(landsat8_dir, landsat8_dir, sen2cor_dir, sen2cor_cloud_dir,
                                                    output_dir,
                                                    pairs, **
                                                    {
                                                        "bands_l8": context.solid_config["bands_l8"],
                                                        "bands_s2": context.solid_config["bands_s2"]
                                                    })


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
                                    " defined in the `repository` resource."),
        InputDefinition(name="scene_ids_s2",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for the validation. These names are equivalent to the Sentinel-2 scene directories"
                                    " defined in the `repository` resource.")
    ],
    config_schema={
        "bands_l8": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. These names should be "
                        "equivalent to the standard USGS Landsat-8 file band naming pattern (e.g. B1, B2).",
            default_value=[
                "B2", "B3", "B4", "B5", "B5", "B6", "B7"
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
        ),
        "day_difference": Field(
            config=int,
            description="Difference of sensing date, in days, to consider two sceneids a pair.",
            default_value=5,
        )
    },
    required_resource_keys={"repository"},
    description="Validate (Compare) Sentinel-2 (with LaSRC atmosphere correction) and Landsat-8 Surface Reflectance images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."
)
def validation_sr_l8_s2_lasrc(context, lasrc_dir: String, sen2cor_cloud_dir: String, scene_ids_l8: List[String],
                              scene_ids_s2: List[String]) -> None:
    """Validate (Compare) Sentinel-2 (with LaSRC atmosphere correction) and Landsat-8 Surface Reflectance images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."""
    #
    # Search for pairs.
    #
    pairs = validation_funcs.search_pairs_l8_s2(
        validation_routines.create_a_temporary_file_with_lines(scene_ids_l8),
        validation_routines.create_a_temporary_file_with_lines(scene_ids_s2),
        day_diff=context.solid_config["day_difference"])

    #
    # Prepare input/output directory.
    #
    landsat8_dir = context.resources.repository["landsat8_input_dir"]

    output_dir_s2 = context.resources.repository["outdir_validation"]
    output_dir = toolbox.prepare_output_directory(output_dir_s2, "validation_sr_l8_s2_lasrc")

    #
    # Validate the results
    #
    validation_routines.validation_sr_l8_s2_lasrc(landsat8_dir, landsat8_dir, lasrc_dir, sen2cor_cloud_dir, output_dir,
                                                  pairs, **
                                                  {
                                                      "bands_l8": context.solid_config["bands_l8"],
                                                      "bands_s2": context.solid_config["bands_s2"]
                                                  })


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
                                    " defined in the `repository` resource."),
        InputDefinition(name="scene_ids_s2",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for the validation. These names are equivalent to the Sentinel-2 scene directories"
                                    " defined in the `repository` resource.")
    ],
    config_schema={
        "bands_l8": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. These names should be "
                        "equivalent to the standard USGS Landsat-8 file band naming pattern (e.g. B1, B2).",
            default_value=[
                "B2", "B3", "B4", "B5", "B5", "B6", "B7"
            ]
        ),
        "bands_s2": Field(
            config=list,
            description="Name of the spectral bands (spectral resolution = 10m and 20m) that will be used in the "
                        "validation. These names should be equivalent to the standard ESA Sentinel-2 .SAFE file "
                        "band naming pattern (e.g. B01, B02, B8A)",
            default_value=[
                "B02", "B03", "B04", "B08", "B8A", "B11", "B12"
            ]
        ),
        "day_difference": Field(
            config=int,
            description="Difference of sensing date, in days, to consider two sceneids a pair.",
            default_value=5,
        )
    },
    required_resource_keys={"repository"},
    description="Validate (Compare) Sentinel-2 (with LaSRC atmosphere correction) and Landsat-8 NBAR images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."
)
def validation_nbar_l8_s2_sen2cor(context, lc8_nbar_dir: String, s2_sen2cor_nbar_dir: str,
                                  sen2cor_cloud_dir: String, scene_ids_l8: List[String],
                                  scene_ids_s2: List[String]) -> None:
    """Validate (Compare) Sentinel-2 (with LaSRC atmosphere correction) and Landsat-8 NBAR images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8_s2(
        validation_routines.create_a_temporary_file_with_lines(scene_ids_l8),
        validation_routines.create_a_temporary_file_with_lines(scene_ids_s2),
        day_diff=context.solid_config["day_difference"])

    #
    # Prepare input/output directory.
    #
    landsat8_dir = context.resources.repository["landsat8_input_dir"]

    output_dir_s2 = context.resources.repository["outdir_validation"]
    output_dir = toolbox.prepare_output_directory(output_dir_s2, "validation_nbar_l8_s2_sen2cor")

    #
    # Validate the results
    #
    validation_routines.validation_nbar_l8_s2_sen2cor(lc8_nbar_dir, landsat8_dir, s2_sen2cor_nbar_dir,
                                                      sen2cor_cloud_dir,
                                                      output_dir, pairs, **
                                                      {
                                                          "bands_l8": context.solid_config["bands_l8"],
                                                          "bands_s2": context.solid_config["bands_s2"]
                                                      })


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
                                    " defined in the `repository` resource."),
        InputDefinition(name="scene_ids_s2",
                        dagster_type=List[String],
                        description="List with the name of the Sentinel-2 scenes that should be used "
                                    "for the validation. These names are equivalent to the Sentinel-2 scene directories"
                                    " defined in the `repository` resource.")
    ],
    config_schema={
        "bands_l8": Field(
            config=list,
            description="Name of the spectral bands that will be used in the validation. These names should be "
                        "equivalent to the standard USGS Landsat-8 file band naming pattern (e.g. B1, B2).",
            default_value=[
                "B2", "B3", "B4", "B5", "B5", "B6", "B7"
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
        ),
        "day_difference": Field(
            config=int,
            description="Difference of sensing date, in days, to consider two sceneids a pair.",
            default_value=5,
        )
    },
    required_resource_keys={"repository"},
    description="Validate (Compare) Sentinel-2 (with Sen2Cor atmosphere correction) and Landsat-8 NBAR images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."
)
def validation_nbar_l8_s2_lasrc(context, lc8_nbar_dir: String, s2_lasrc_nbar_dir: String, sen2cor_cloud_dir: String,
                                scene_ids_l8: List, scene_ids_s2: List) -> None:
    """Validate (Compare) Sentinel-2 (with Sen2Cor atmosphere correction) and Landsat-8 NBAR images, of the same spatial location, acquired with a sensing date difference up to `day_difference`."""
    #
    # Search for pairs
    #
    pairs = validation_funcs.search_pairs_l8_s2(
        validation_routines.create_a_temporary_file_with_lines(scene_ids_l8),
        validation_routines.create_a_temporary_file_with_lines(scene_ids_s2),
        day_diff=context.solid_config["day_difference"])

    #
    # Prepare input/output directory.
    #
    landsat8_dir = context.resources.repository["landsat8_input_dir"]

    output_dir_s2 = context.resources.repository["outdir_validation"]
    output_dir = toolbox.prepare_output_directory(output_dir_s2, "validation_nbar_l8_s2_lasrc")

    #
    # Validate the results
    #
    validation_routines.validation_nbar_l8_s2_lasrc(lc8_nbar_dir, landsat8_dir, s2_lasrc_nbar_dir, sen2cor_cloud_dir,
                                                    output_dir, pairs,
                                                    **{
                                                        "bands_l8": context.solid_config["bands_l8"],
                                                        "bands_s2": context.solid_config["bands_s2"]
                                                    })
