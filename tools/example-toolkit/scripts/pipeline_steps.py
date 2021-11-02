#
# This file is part of research-processing library
# Copyright (C) 2021 INPE.
#
# research-processing is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os

import yaml
import json

import bagit
import shutil

from typing import List

from loguru import logger
import base32_lib as base32
from toolbox import download_file, extract_packed_files


def download_data_files_from_github(output_directory: str, download_files_reference: str) -> List[str]:
    """Download data from the Research Compendium Github Repository. 

    Args:
        output_directory (str): Directory where the downloaded files will be saved.

        download_files_reference (str): Path to the JSON file containing the data definitions that should be downloaded from 
        the Research Compendium GitHub repository. This JSON must be contains the following structure:
            {
              "repositoryTag": "...",
              "dataFiles": [
                "...",
              ]
            }

        where:
            - `repositoryTag`: Is the github tag where files is saved;
            - `dataFiles`: List of the Github tag asset files that should be downloaded;

    Returns:
        list: list with path of the downloaded files.
    """
    # Load download configurations.
    with open(download_files_reference, "r") as ifile:
        files_reference_definition = json.load(ifile)
        data_files_to_download = files_reference_definition.get("dataFiles")

    # Download and validate the data files.
    downloaded_files = []

    for data_file_to_download in data_files_to_download:
        file_name = os.path.basename(data_file_to_download)
        file_output = os.path.join(output_directory, file_name)

        if not os.path.exists(file_output):
            logger.info(f"Downloading {file_name} (Sometimes the progress bar may not appear. Please, be patient.)")

            # Downloading files.
            download_file(data_file_to_download, file_output)

            # Extracting downloaded file.
            file_output_directory = extract_packed_files(file_output, output_directory)

            # Checking the checksum.
            bagit.Bag(file_output_directory).validate()

            # Move bagit `data directory` to `output_directory`
            bagit_data = os.path.join(file_output_directory, "data")

            # Moving data to a temporary directory
            temporary_dir = base32.generate(length=10, split_every=5, checksum=True)
            temporary_dir = os.path.join(output_directory, temporary_dir)

            os.makedirs(temporary_dir)
            for fs_object in os.listdir(bagit_data):
                shutil.move(os.path.join(bagit_data, fs_object), temporary_dir)

            # Removing bagit folder
            shutil.rmtree(file_output_directory)

            # Rename temporary directory to the original filename
            os.rename(temporary_dir, file_output_directory)

            # Removing downloaded .zip file.
            os.remove(file_output)

            downloaded_files.append(file_output_directory)

    logger.info(f"All files are downloaded.")
    return downloaded_files


def extract_data(downloaded_files: List) -> None:
    """Extract the zip files downloaded from GitHub.

    Args:
        downloaded_files (List[str]): List with the path of files downloaded from the Research Compendium GitHub Repository.

    Returns:
        None
    """
    for downloaded_file_directory in downloaded_files:

        if "lasrc" in downloaded_file_directory or "scene_id_list" in downloaded_file_directory:
            # `lasrc_auxiliary_data auxiliary data` and `scene id list` does not require extra extraction.
            continue

        files_to_extract = [
            os.path.join(downloaded_file_directory, x) for x in os.listdir(downloaded_file_directory)
        ]

        # Extracting files.
        extracted_directories = [
            extract_packed_files(x, downloaded_file_directory) for x in files_to_extract
        ]

        # Searching for extracted directories and move to the root `output_dir` only the sentinel-2 data.
        for extracted_obj in extracted_directories:
            if os.path.isdir(extracted_obj) and "S2" in extracted_obj:
                # During extraction, the image directory that comes out of the zip is stored at
                # a lower level than needed. Then the file is moved to the directory above.
                internal_folder = os.path.join(extracted_obj, os.listdir(extracted_obj)[0])
                shutil.move(internal_folder, downloaded_file_directory)

                shutil.rmtree(extracted_obj)

        # Removing .zip files
        [os.remove(x) for x in files_to_extract]


def change_files_permission_recursive(root_path: str, permission: int):
    """Change files permission recursively.

    Args:
        root_path (str): Base path where the recursively change permission starts.

        permission (int): Permission applied to all files/directories below `root_path`.

    Returns:
        None: Files permission will be changed directly in the files.
    """
    for obj in os.listdir(root_path):
        obj_path = os.path.join(root_path, obj)
        if os.path.isdir(obj_path):
            change_files_permission_recursive(obj_path, permission)
        os.chmod(obj_path, permission)


def replace_subdirectories_name(base_directory: str, in_pattern: str, out_pattern: str):
    """Replace the subdirectories names of a directory based on a pattern. 

    In this function every subdirectory of the `base_directory` that has the specified pattern (`in_pattern`) will be renamed 
    to the newly defined pattern (`out_pattern`). For example, for the call:

            >> replace_subdirectories_name('/my/path', 'local', 'online')

        All directories at the first level below `/my/path`, which contain in their name the pattern `local` 
        will be renamed with the new pattern `online`:

            `Original subfolders names`

            /my/path
                - subdir_local
                - subdir2_local

            `Will be renamed to`

            /my/path
                - subdir_online
                - subdir2_online

    Args:
        base_directory (str): Base directory

        in_pattern (str): The Pattern that will be replaced.

        out_pattern (str): The Pattern that replaces the `in_pattern` values.

    Returns:
        None
    """
    for subdirectory in os.listdir(base_directory):
        subdirectory_old_name = os.path.join(base_directory, subdirectory)

        # preparing the new directory name
        subdirectory_new_name = subdirectory.replace(in_pattern, out_pattern)
        subdirectory_new_name = os.path.join(base_directory, subdirectory_new_name)

        os.rename(subdirectory_old_name, subdirectory_new_name)


def create_dagit_yaml_file(raw_data_dir: str, derived_data_dir: str, output_file: str):
    """Create a Dagster configuration file based on specified data directories.

    Args:
        raw_data_dir (str): Directory where the raw data is stored.

        derived_data_dir (str): Directory where the processing results will be saved.

        output_file (str): File where the Dagster YAML configuration content will be saved.

    Returns:
        None: The configuration content will be saved on the `output_file`.

    Note:
        In the version of Dagster used to produce the article (0.12.2), the tool uses the concept of 
        `Solids` to express operations.
    """
    # Defining path to the LADS auxiliary data (LaSRC).
    lads_auxiliary_data_dir = os.path.join(raw_data_dir, "lasrc_auxiliary_data")

    # Preparing the data directory for Landsat-8 and Sentinel-2.
    landsat8_input_dir = os.path.join(raw_data_dir, "landsat8_data")
    sentinel2_input_dir = os.path.join(raw_data_dir, "sentinel2_data")

    # Defining the path to the scene ids.
    landsat8_sceneid_list = os.path.join(raw_data_dir, "scene_id_list", "l8-sceneids.txt")
    sentinel2_sceneid_list = os.path.join(raw_data_dir, "scene_id_list", "s2-sceneids.txt")

    # Write the configuration
    pipeline_config = {
        "resources": {
            "lads_data": {
                "config": {
                    "lads_auxiliary_data_dir": lads_auxiliary_data_dir
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
