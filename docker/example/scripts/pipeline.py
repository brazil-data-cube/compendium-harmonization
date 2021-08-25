#
# This file is part of research-processing library
# Copyright (C) 2021 INPE.
#
# research-processing is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os

from pipeline_steps import (
    create_dagit_yaml_file, download_example_files,
    extract_example_data, change_files_permission_recursive
)

if __name__ == "__main__":
    # get output directory and example files reference from env file
    output_directory = os.environ.get("REPO_DOWNLOAD_OUTPUT")
    files_reference = os.environ.get("EXAMPLE_FILES_REFERENCE_FILE")

    pipeline_dir = os.environ.get("PIPELINE_DIR")
    raw_data_dir = os.environ.get("RAW_DATA_DIR")
    derived_data_dir = os.environ.get("DERIVED_DATA_DIR")

    if not all([output_directory, files_reference, derived_data_dir, pipeline_dir, raw_data_dir]):
        raise RuntimeError("Please, to run this code you must provide the following environment variables:"
                           "`REPO_DOWNLOAD_OUTPUT`, "
                           "`RAW_DATA_DIR`, "
                           "`DERIVED_DATA_DIR`, "
                           "`PIPELINE_DIR`, and "
                           "`EXAMPLE_FILES_REFERENCE_FILE` environment variables.")

    # step 1. Download and validate example files
    downloaded_files = download_example_files(output_directory, files_reference)

    # step 2. Extract downloaded files (in case of landsat-8 and sentinel-2 compressed scenes)
    extract_example_data(downloaded_files)

    # step 3. Change files permission.
    change_files_permission_recursive(output_directory, 0o0777)

    # step 4. Create a dagit configuration file with the output directories)
    dagit_file = os.path.join(pipeline_dir, "config.yaml")
    create_dagit_yaml_file(raw_data_dir, derived_data_dir, dagit_file)