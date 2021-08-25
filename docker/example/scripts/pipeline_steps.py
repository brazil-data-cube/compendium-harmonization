#
# This file is part of research-processing library
# Copyright (C) 2021 INPE.
#
# research-processing is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import json
import os
import shutil
from typing import List

import requests
import yaml
from loguru import logger

from toolbox import multihash_checksum_sha256, download_file, extract_packed_files


def download_example_files(output_directory: str, example_files_reference: str) -> List[str]:
    """Download the example data for running the processing flow presented in the article.

    Args:
        output_directory (str): Directory where the downloaded files will be saved.

        example_files_reference (str): JSON file with the reference to example files. This JSON
        must be contains the following structure:
            {
              "repositoryTag": "...",
              "repositoryTagCommitChecksum": "...",
              "exampleFiles": [
                "...",
              ],
              "checksum": "..."
            }

        where:
            - `repositoryTag`: Is the github tag where files is saved
            - `repositoryTagCommitChecksum`: Github tag commit checksum
            - `exampleFiles`: Github tag asset files that will be downloaded
            - `checksum`:  Github tag asset file that contains the checksum of other assets files

    Returns:
        list: list with path of the downloaded files.
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
            logger.info(f"Downloading {filename} (Sometimes the progress bar may not appear. Please, be patient.)")

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


def extract_example_data(downloaded_files: List) -> None:
    """Extracts data files needed for the minimum execution example of the article.

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


def change_files_permission_recursive(root_path: str, permission: int):
    """Change files permission recursively.

    Args:
        root_path (str): Base path where the recursively change permission starts.

        permission (int): Permission applied to all files/directories below `root_path`.

    Returns:
        None: Files permission will be applied in files.
    """
    for obj in os.listdir(root_path):
        obj_path = os.path.join(root_path, obj)
        if os.path.isdir(obj_path):
            change_files_permission_recursive(obj_path, permission)
        os.chmod(obj_path, permission)


def create_dagit_yaml_file(raw_data_dir: str, derived_data_dir: str, output_file: str):
    """Create a Dagster configuration file based on specified data directories.

    Args:
        raw_data_dir (str): Directory where the raw data is stored.

        derived_data_dir (str): Directory where the processing results will be saved.

        output_file (str): File where the Dagster YAML configuration content will be saved.

    Returns:
        None: The configuration content will be saved on the `output_file`.
    """
    #
    # Resources
    #

    # LADS
    lands_auxiliary_data_dir = os.path.join(raw_data_dir, "LADS_AuxiliaryData")

    # Repository
    landsat8_input_dir = os.path.join(raw_data_dir, "Landsat8Data")
    sentinel2_input_dir = os.path.join(raw_data_dir, "Sentinel2Data")

    # solids

    # Load and standardize the scene ids
    landsat8_sceneid_list = os.path.join(raw_data_dir, "ReferenceFiles_L8-S2", "l8-sceneids.txt")
    sentinel2_sceneid_list = os.path.join(raw_data_dir, "ReferenceFiles_L8-S2", "s2-sceneids.txt")

    # Write the configuration
    pipeline_config = {
        "resources": {
            "lads_data": {
                "config": {
                    "lands_auxiliary_data_dir": lands_auxiliary_data_dir
                }
            },
            "repository": {
                "config": {
                    "derived_data_dir": derived_data_dir,
                    "landsat8_input_dir": landsat8_input_dir,
                    "sentinel2_input_dir": sentinel2_input_dir
                }
            }
        },
        "solids": {
            "load_and_standardize_sceneids_input": {
                "config": {
                    "landsat8_sceneid_list": landsat8_sceneid_list,
                    "sentinel2_sceneid_list": sentinel2_sceneid_list
                }
            }
        }
    }

    with open(output_file, "w") as ofile:
        yaml.dump(pipeline_config, ofile)