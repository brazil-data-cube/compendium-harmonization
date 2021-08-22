#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""c-factor resources."""

import os

from dagster import DagsterResourceFunctionError
from dagster import Field, Dict, String
from dagster import resource


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
                "cfactor processing stream. This ResourceDefinition returns a dictionary with the input keys and also "
                "the `outdir_landsat8` and `outdir_sentinel2` keys. The extra keys added, represent the base "
                "directory where the result of processing each of the sensors will be saved.")
def cfactor_resource_repository(_init_context) -> Dict:
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
    "lands_auxiliary_data_dir": Field(
        config=String,
        description="Directory where the LADS auxiliary data is stored. The contents of this directory should follow "
                    "the structure definition found on the `USGS` website, where it reads: `Year/.hdf_fused`. This "
                    "data will be used for the application of LaSRC to the Sentinel-2 scenes."
    ),
})
def cfactor_resource_lads_auxiliary_data(_init_context) -> Dict:
    """LADS auxiliary files resource.

    Returns:
        Dict: A dictionary with the `lads_auxiliary_directory` key, containing the directory where
        the LADS auxiliary data is stored. It is expected that this directory will have the same structure as
        the USGS site (`Year/.hdf_fused`). The structure looks like this:

             - LADS (path you will pass in the resource configuration)
               - 2013
                  - L8ANC2013001.hdf_fused
               - 2014
                  - ...
               - ...

        Not all `hdf_fused` files need to be in these directories. Only those equivalent to the images used in
        processing should be present.

    See:
        https://edclpdsftp.cr.usgs.gov/downloads/auxiliaries/lasrc_auxiliary/L8/LADS/
    """
    lads_auxiliary_directory = _init_context.resource_config["lands_auxiliary_data_dir"]

    if not os.path.isdir(lads_auxiliary_directory):
        raise DagsterResourceFunctionError(
            f"The directory {lads_auxiliary_directory} indicated as a resource does not exist or cannot be found.")

    return {
        "lads_auxiliary_directory": lads_auxiliary_directory
    }
