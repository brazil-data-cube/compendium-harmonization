#
# This file is part of Brazil Data Cube compendium-harmonization.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
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
