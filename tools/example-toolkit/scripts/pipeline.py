#
# This file is part of compendium-harmonization
# Copyright (C) 2021-2022 INPE.
#
# compendium-harmonization is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os

from pipeline_steps import (
    extract_data, 
    create_dagit_yaml_file, 
    replace_subdirectories_name,
    download_data_files_from_github,
    change_files_permission_recursive
)


if __name__ == "__main__":
    #
    # Data definitions
    #

    # Path to the JSON file with the definition of the data to be downloaded
    files_reference = os.environ.get("DOWNLOAD_REFERENCE_FILE")

    # Directory where the downloaded data will be saved.
    output_directory = os.environ.get("DOWNLOAD_OUTPUT_DIRECTORY")

    #
    # Dagster configuration file definitions.
    #

    # Path to the directory where the generated dagster configuration file will be saved.
    pipeline_dir = os.environ.get("PIPELINE_DIR")

    # Path to the input data directory.
    raw_data_dir = os.environ.get("RAW_DATA_DIR")
    
    # Path to the output data directory.
    derived_data_dir = os.environ.get("DERIVED_DATA_DIR")

    #
    # Checking if all variables is defined.
    #
    if not all([output_directory, files_reference, derived_data_dir, pipeline_dir, raw_data_dir]):
        raise RuntimeError("Please, to run this code you must provide the following environment variables:"
                           "`DOWNLOAD_OUTPUT_DIRECTORY`, "
                           "`RAW_DATA_DIR`, "
                           "`DERIVED_DATA_DIR`, "
                           "`PIPELINE_DIR`, and "
                           "`DOWNLOAD_REFERENCE_FILE` environment variables.")

    #
    # Step 1. Download and validate example files
    #
    downloaded_files = download_data_files_from_github(output_directory, files_reference)

    #
    # Step 2. Extract downloaded files (in case of landsat-8 and sentinel-2 compressed scenes)
    #
    extract_data(downloaded_files)

    #
    # Step 3. Rename files.
    #
    replace_subdirectories_name(output_directory, "minimal-example_", "")
    replace_subdirectories_name(output_directory, "replication-example_", "")

    #
    # Step 4. Change files permission.
    #
    change_files_permission_recursive(output_directory, 0o0777)

    #
    # Step 5. Create a dagit configuration file with the output directories)
    #
    dagit_file = os.path.join(pipeline_dir, "config.yaml")
    create_dagit_yaml_file(raw_data_dir, derived_data_dir, dagit_file)
