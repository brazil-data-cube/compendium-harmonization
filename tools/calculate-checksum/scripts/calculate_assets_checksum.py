#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os
from toolbox import bagit_directory


if __name__ == "__main__":
    #
    # 1. Configuring the input/output directory. 
    #
    input_directory_to_bagit = os.environ.get("INPUT_DATA_DIRECTORY")
    output_directory_to_save_bagit = os.environ.get("OUTPUT_DATA_DIRECTORY")

    #
    # 2. Configuring bagit process
    #
    n_process = int(os.environ.get("BAGIT_HASH_PROCESSES", 8))

    #
    # 3. Bagit each available directory on `input directory`.
    #
    available_directories = os.listdir(input_directory_to_bagit)

    for available_directory in available_directories:
        print(f"Processing: {available_directory}")

        directory_path = os.path.join(input_directory_to_bagit, available_directory)
        output_path = os.path.join(output_directory_to_save_bagit, available_directory)

        bagit_directory(directory_path, output_path, {}, processes=n_process)
