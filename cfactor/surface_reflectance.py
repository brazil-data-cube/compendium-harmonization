#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os
from typing import List

from .config import EnvironmentConfig
from .environment import ContainerManager


def sen2cor(input_dir: str, output_dir: str, scene_ids: List[str]) -> List:
    """ToDo: Add description
    
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
    processed_scenes = []
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

        processed_scenes.append(os.path.join(output_dir, scene_id))
    return processed_scenes


def lasrc(input_dir: str, output_dir: str, scene_ids: List[str],
          aux_data_dir: str) -> List:
    """ToDo: Add description
    
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
    processed_scenes = []
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
                    "bind": "/mnt/atmcor_aux/lasrc/L8/LADS",
                    "mode": "ro"
                }
            },
            command=scene_id
        )

        processed_scenes.append(os.path.join(output_dir, scene_id))
    return processed_scenes
