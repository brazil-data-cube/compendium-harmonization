#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import json
import os
import shutil
from typing import List

import requests
from loguru import logger

from toolbox import multihash_checksum_sha256, download_file, extract_packed_files


def download_example_files(output_directory: str, example_files_reference: str) -> List:
    """
    """
    # load example files reference
    with open(example_files_reference, "r") as ifile:
        files_reference_definition = json.load(ifile)
        files_reference = files_reference_definition.get("exampleFiles")

        # load checksum reference file
        file_checksum_original = files_reference_definition.get("checksum")
        if not file_checksum_original:
            raise RuntimeError(f"Checksum reference not found! Please, check your configuration file.")

        checksum_reference = requests.get(file_checksum_original).json()

    # download and validate the example files
    downloaded_files = []

    for file_reference in files_reference:
        filename = os.path.basename(file_reference)
        file_output = os.path.join(output_directory, filename)

        file_checksum_original = checksum_reference.get(filename)
        if not file_checksum_original:
            raise RuntimeError(
                f"Checksum not found for {filename}! Please, check if you are using the right repository.")

        if not os.path.exists(file_output):
            logger.info(f"Downloading {filename}")

            # download files
            download_file(file_reference, file_output)

            # verify the checksum
            file_checksum = multihash_checksum_sha256(file_output)
            if file_checksum != file_checksum_original:
                raise RuntimeError(f"Invalid Checksum for {filename}! Try downloading the files again!")

            # extract downloaded file
            file_output_directory = extract_packed_files(file_output, output_directory)

            # removing downloaded .zip file
            os.remove(file_output)

            downloaded_files.append(file_output_directory)

    logger.info(f"All files are downloaded.")

    return downloaded_files


def extract_cfactor_example_data(downloaded_files: List) -> None:
    """Extracts data files needed for the minimum execution example of the c-factor article.

    Args:
        downloaded_files (List[str]): List with paths to the directories that were generated
        for each of the downloaded files.

    Returns:
        None

    Note:
        It is assumed by the function that these directories will contain the `LADS Auxiliary`,
        `Landsat-8` and `Sentinel-2` data.
    """
    for downloaded_file_directory in downloaded_files:

        if "LADS" in downloaded_file_directory or "Reference" in downloaded_file_directory:
            # LADS auxiliary data and Reference files does not require extra extraction.
            continue

        files_to_extract = [
            os.path.join(downloaded_file_directory, x) for x in os.listdir(downloaded_file_directory)
        ]

        # extracting files.
        extracted_directories = [
            extract_packed_files(x, downloaded_file_directory) for x in files_to_extract
        ]

        # search for extracted directories and move to the root `output_dir` only the sentinel-2 data.
        for extracted_obj in extracted_directories:
            if os.path.isdir(extracted_obj) and "S2" in extracted_obj:
                # During extraction, the image directory that comes out of the zip is stored at
                # a lower level than needed. Then the file is moved to the directory above.
                internal_folder = os.path.join(extracted_obj, os.listdir(extracted_obj)[0])
                shutil.move(internal_folder, downloaded_file_directory)

                shutil.rmtree(extracted_obj)

        # removing .zip files
        [os.remove(x) for x in files_to_extract]
