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


def sen2cor(input_dir: str, output_dir: str, scene_ids: List[str]) -> List:
    """Instantiate a docker container (`EnvironmentConfig.SEN2COR_IMAGE`) to generate Surface Reflectance products (Sen2cor atmosphere correction) for Sentinel-2 scenes.

    Args:
        input_dir (str): Directory where the directories of the scenes to be
        processed are located.

        output_dir (str): Directory where the results will be saved.

        scene_ids (List[str]): List with the scene_ids that should be processed.
        The scene_ids defined must be equivalent to the scene directory names in
        the `input_dir`.

    Returns:
        List: List with full path to each output scene.
    """
    for scene_id in scene_ids:
        ContainerManager.run_container(
            image=EnvironmentConfig.SEN2COR_IMAGE,
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


def lasrc(input_dir: str, output_dir: str, scene_ids: List[str],
          aux_data_dir: str) -> List:
    """Instantiate a docker container (`EnvironmentConfig.LASRC_IMAGE`) to generate Surface Reflectance (LaSRC atmosphere correction) products for Sentinel-2 scenes.

    Args:
        input_dir (str): Directory where the directories of the scenes to be
        processed are located.

        output_dir (str): Directory where the results will be saved.

        scene_ids (List[str]): List with the scene_ids that should be processed.
        The scene_ids defined must be equivalent to the scene directory names in
        the `input_dir`.

        aux_data_dir (str):Path to the directory where all the LaSRC auxiliary
        data directory `L8` is available.

    Returns:
        List: List with full path to each output scene.

    See:
        LaSRC Auxiliary Data: https://edclpdsftp.cr.usgs.gov/downloads/auxiliaries/lasrc_auxiliary/

    Note:
        The auxiliary data directory should contain all the content that is in
        the `L8` directory (https://edclpdsftp.cr.usgs.gov/downloads/auxiliaries/lasrc_auxiliary/L8/)
        provided by the USGS.
    """
    for scene_id in scene_ids:
        ContainerManager.run_container(
            image=EnvironmentConfig.LASRC_IMAGE,
            auto_remove=True,
            volumes={
                input_dir: {
                    "bind": "/mnt/input-dir",
                    "mode": "rw"
                },
                output_dir: {
                    "bind": "/mnt/output-dir",
                    "mode": "rw"
                },
                aux_data_dir: {
                    "bind": "/mnt/atmcor-aux/lasrc/L8",
                    "mode": "ro"
                }
            },
            command=scene_id
        )

    return [
        os.path.join(output_dir, fs_object) for fs_object in os.listdir(output_dir)
    ]
