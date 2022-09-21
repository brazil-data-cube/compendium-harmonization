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

import bagit

import shutil
from typing import Dict


def bagit_directory(directory_path: str, output_file: str, metadata: Dict, **kwargs) -> str:
    """Create the BagIt of a directory and store it in a zip file.

    Args:
        directory_path (str): Full path to the directory from which the BagIt will be created.

        output_file (str): Full path to file where the BagIt (in zip format) will be saved.

        metadata (Dict): BagIt metadata.

        kwargs (Dict): Extra options for `bagit.make_bag` function.

    Returns:
        str: Path to the directory where the zip file will be saved.

    See:
        https://github.com/LibraryOfCongress/bagit-python
    """
    # create the directory bagit
    bagit.make_bag(directory_path, metadata, **kwargs)
    
    # creating a zip file from bagit directory
    shutil.make_archive(output_file, "zip", directory_path)

    return output_file
