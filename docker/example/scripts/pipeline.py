#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os

from pipeline_steps import download_example_files, extract_cfactor_example_data

if __name__ == "__main__":
    # get output directory and example files reference from env file
    output_directory = os.environ.get("CFACTOR_REPO_DOWNLOAD_OUTPUT")
    files_reference = os.environ.get("CFACTOR_EXAMPLE_FILES_REFERENCE_FILE")

    if not output_directory or not files_reference:
        raise RuntimeError("Please, to run this code you must provide the "
                           "`CFACTOR_REPO_DOWNLOAD_OUTPUT` and "
                           "`CFACTOR_EXAMPLE_FILES_REFERENCE_FILE` environment variables.")

    # step 1. Download and validate example files
    downloaded_files = download_example_files(output_directory, files_reference)

    # step 2. Extract downloaded files (in case of landsat-8 and sentinel-2 compressed scenes)
    extract_cfactor_example_data(downloaded_files)
