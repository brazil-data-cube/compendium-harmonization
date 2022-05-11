#
# This file is part of compendium-harmonization
# Copyright (C) 2021-2022 INPE.
#
# compendium-harmonization is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""research-processing resources."""

import os

from dagster import resource
from dagster import Field, Dict, String
from dagster import DagsterResourceFunctionError


@resource(config_schema={
    "landsat8_input_dir": Field(
        config=String,
        description="Directory path where the Landsat-8/OLI scenes for processing are available. "
                    "The scenes must be in separate directories with unzipped content."
    ),
    "sentinel2_input_dir": Field(
        config=String,
        description="Directory path where the Sentinel-2/MSI scenes for processing are available. "
                    "The scenes must be in separate .SAFE directories with unzipped content."
    ),
    "derived_data_dir": Field(
        config=String,
        description="Base directory where the result of the processing steps will be saved."
    )
},
    description="Data Access Resource. Registers the directories to be used as input/output for the "
                "processing stream. This ResourceDefinition returns a dictionary with the input keys and also "
                "the `outdir_landsat8` and `outdir_sentinel2` keys. The extra keys added, represent the base "
                "directory where the result of processing each of the sensors will be saved.")
def resource_repository(_init_context) -> Dict:
    """Data Access Resource.

    Returns:
        Dict: Dictionary with the input keys and also the `outdir_landsat8`, `outdir_sentinel2`, `outdir_validation`
              keys. The extra keys added, represent the base directory where the result of processing each of the
              sensors will be saved. The output looks like:
                {
                    "landsat8_input_dir": "...",
                    "sentinel2_input_dir": "...",
                    "derived_data_dir": "...",
                    "outdir_landsat8": "...",
                    "outdir_sentinel2": "...",
                    "outdir_validation": "..."
                }
    """
    # validate the defined resources
    for resource_dir in _init_context.resource_config.keys():
        if not os.path.isdir(_init_context.resource_config[resource_dir]):
            raise DagsterResourceFunctionError(
                f"The {resource_dir} directory, does not exist or cannot be found.")

    # create base output directories (for each sensor)
    base_out_dir = _init_context.resource_config["derived_data_dir"]

    s2_outputs = os.path.join(base_out_dir, "s2")
    lc8_outputs = os.path.join(base_out_dir, "l8")
    validation_outputs = os.path.join(base_out_dir, "validation")

    return {
        **_init_context.resource_config,
        **{
            "outdir_landsat8": lc8_outputs,
            "outdir_sentinel2": s2_outputs,
            "outdir_validation": validation_outputs
        }
    }


@resource(config_schema={
    "lasrc_auxiliary_data_dir": Field(
        config=String,
        description="Directory where the LaSRC auxiliary data is stored. The contents of this directory should follow "
                    "the structure definition found on the `USGS` website "
                    "(L8 directory - https://edclpdsftp.cr.usgs.gov/downloads/auxiliaries/lasrc_auxiliary/L8/)"
    ),
})
def resource_lasrc_auxiliary_data(_init_context) -> Dict:
    """LaSRC auxiliary data resource.

    Resource for defining the directory where the LaSRC auxiliary data is stored. This directory is 
    expected to be valid and contains the files, directories, and subdirectories provided by the 
    USGS (https://edclpdsftp.cr.usgs.gov/downloads/auxiliaries/lasrc_auxiliary/L8/). As such, 
    the expected directory should look like the content shown below:

            lasrc_auxiliary/L8/
                - LADS/
                - LDCMLUT/
                - MSILUT/ 
                - CMGDEM.hdf
                - ratiomapndwiexp.hdf

    Note: 
        You **don't** need to have all LADS data. You only need to have available the data that concerns your input data.

    Returns:
        Dict: Dict with the `lasrc_auxiliary_directory` key, which contains the reference to the LaSRC auxiliary 
        data directory.

    See:
        https://edclpdsftp.cr.usgs.gov/downloads/auxiliaries/lasrc_auxiliary/L8/
    """
    lasrc_auxiliary_directory = _init_context.resource_config["lasrc_auxiliary_data_dir"]

    if not os.path.isdir(lasrc_auxiliary_directory):
        raise DagsterResourceFunctionError(
            f"The directory {lasrc_auxiliary_directory} indicated as a resource does not exist or cannot be found.")

    return {
        "lasrc_auxiliary_directory": lasrc_auxiliary_directory
    }


__all__ = (
    "resource_repository",
    "resource_lasrc_auxiliary_data"
)
