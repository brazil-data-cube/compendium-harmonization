#
# This file is part of research-processing library
# Copyright (C) 2021 INPE.
#
# research-processing is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os
from typing import List

from .config import EnvironmentConfig
from .environment import ContainerManager


def lc8_generate_angles(input_dir: str, output_dir: str, scene_ids: List[str]) -> List[str]:
    """Instantiate a docker container (`EnvironmentConfig.LANDSAT8_ANGLES_IMAGE`) to generate angles for Landsat-8 scenes using USGS Angle Creation Tool.

    Args:
        input_dir (str): Directory where the directories of the scenes to be
        processed are located.

        output_dir (str): Directory where the results will be saved.

        scene_ids (List[str]): List with the scene_ids that should be processed.
        The scene_ids defined must be equivalent to the scene directory names in
        the `input_dir`.

    Returns:
        List: List with full path for each scene that had the angles generated.

    Note:
        The generated angle files are saved directly to the data directories
        specified in `input_dir`. It is expected that this directory
        organizational structure will follow the data standards provided
        by the USGS.
    """
    processed_scenes = []
    for scene_id in scene_ids:
        ContainerManager.run_container(
            image=EnvironmentConfig.LANDSAT8_ANGLES_IMAGE,
            auto_remove=True,
            volumes={
                input_dir: {
                    "bind": "/mnt/input-dir",
                    "mode": "rw"
                },
                output_dir: {
                    "bind": "/mnt/output-dir",
                    "mode": "rw"
                }
            },
            command=scene_id
        )

        processed_scenes.append(scene_id)
    return processed_scenes


def lc8_nbar(input_dir: str, output_dir: str, angle_dir: str, scene_ids: List[str]) -> List[str]:
    """Instantiate a docker container (`EnvironmentConfig.NBAR_IMAGE`) to generate NBAR products for Landsat-8 scenes.

    Args:
        input_dir (str): Directory where the directories of the scenes to be
        processed are located.

        output_dir (str): Directory where the results will be saved.

        angle_dir (str) - path to directory containing angle bands.

        scene_ids (List[str]): List with the scene_ids that should be processed.
        The scene_ids defined must be equivalent to the scene directory names in
        the `input_dir`.

    Returns:
        List[str]: List with full path for each nbar scene generated.
    """
    processed_scenes = []
    for scene_id in scene_ids:
        ContainerManager.run_container(
            image=EnvironmentConfig.NBAR_IMAGE,
            auto_remove=True,
            volumes={
                os.path.join(input_dir, scene_id): {
                    "bind": "/mnt/input-dir",
                    "mode": "ro"
                },
                output_dir: {
                    "bind": "/mnt/output-dir",
                    "mode": "rw"
                },
                angle_dir: {
                    "bind": "/mnt/input-dir-angles",
                    "mode": "rw"
                }
            },
            command=scene_id
        )

        processed_scenes.append(os.path.join(output_dir, scene_id))
    return processed_scenes


def s2_sen2cor_nbar(input_dir: str, output_dir: str, scene_ids: List[str]) -> List[str]:
    """Instantiate a docker container (`EnvironmentConfig.NBAR_IMAGE`) to generate NBAR products for Sentinel-2 scenes (with Sen2Cor atmosphere correction).

    Args:
        input_dir (str): Directory where the directories of the scenes to be
        processed are located.

        output_dir (str): Directory where the results will be saved.

        scene_ids (List[str]): List with the scene_ids that should be processed.
        The scene_ids defined must be equivalent to the scene directory names in
        the `input_dir`.

    Returns:
        List[str]: List with full path for each nbar (sen2cor) scene generated.
    """
    processed_scenes = []
    for scene_id in scene_ids:
        ContainerManager.run_container(
            image=EnvironmentConfig.NBAR_IMAGE,
            auto_remove=True,
            volumes={
                input_dir: {
                    "bind": "/mnt/input-dir",
                    "mode": "rw"
                },
                output_dir: {
                    "bind": "/mnt/output-dir",
                    "mode": "rw"
                }
            },
            command=scene_id
        )

        processed_scenes.append(os.path.join(output_dir, scene_id))
    return processed_scenes


def s2_lasrc_nbar(input_dir: str, output_dir: str, scene_ids: List[str]) -> List[str]:
    """Instantiate a docker container (`EnvironmentConfig.NBAR_IMAGE`) to generate NBAR products for Sentinel-2 scenes (with LaSRC atmosphere correction).

    Args:
        input_dir (str): Directory where the directories of the scenes to be
        processed are located.

        output_dir (str): Directory where the results will be saved.

        scene_ids (List[str]): List with the scene_ids that should be processed.
        The scene_ids defined must be equivalent to the scene directory names in
        the `input_dir`.

    Returns:
        List[str]: List with full path for each nbar (LaSRC) scene generated.
    """
    processed_scenes = []
    for scene_id in scene_ids:
        ContainerManager.run_container(
            image=EnvironmentConfig.NBAR_IMAGE,
            auto_remove=True,
            volumes={
                input_dir: {
                    "bind": "/mnt/input-dir",
                    "mode": "rw"
                },
                output_dir: {
                    "bind": "/mnt/output-dir",
                    "mode": "rw"
                }
            },
            command=scene_id
        )

        processed_scenes.append(os.path.join(output_dir, scene_id))
    return processed_scenes
