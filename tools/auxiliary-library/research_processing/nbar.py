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

    return [
        os.path.join(output_dir, fs_object) for fs_object in os.listdir(output_dir)
    ]


def lc8_nbar(input_dir: str, angle_dir: str, output_dir: str, scene_ids: List[str]) -> List[str]:
    """Instantiate a docker container (`EnvironmentConfig.NBAR_IMAGE`) to generate NBAR products for Landsat-8 scenes.

    Args:
        input_dir (str): Directory where the directories of the scenes to be
        processed are located.

        angle_dir (str): Path to directory containing angle bands.

        output_dir (str): Directory where the results will be saved.

        scene_ids (List[str]): List with the scene_ids that should be processed.
        The scene_ids defined must be equivalent to the scene directory names in
        the `input_dir`.

    Returns:
        List[str]: List with full path for each nbar scene generated.
    """
    for scene_id in scene_ids:
        ContainerManager.run_container(
            image=EnvironmentConfig.NBAR_IMAGE,
            auto_remove=True,
            volumes={
                input_dir: {
                    "bind": "/mnt/input-dir",
                    "mode": "ro"
                },
                output_dir: {
                    "bind": "/mnt/output-dir",
                    "mode": "rw"
                },
                angle_dir: {
                    "bind": "/mnt/angles-dir",
                    "mode": "rw"
                }
            },
            command=scene_id
        )

    return [
        os.path.join(output_dir, fs_object) for fs_object in os.listdir(output_dir)
    ]


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

    return [
        os.path.join(output_dir, fs_object) for fs_object in os.listdir(output_dir)
    ]


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

    return [
        os.path.join(output_dir, fs_object) for fs_object in os.listdir(output_dir)
    ]
