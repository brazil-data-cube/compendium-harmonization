#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os

from typing import List
from plumbum.cmd import docker


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
        (
            docker[
                "run", "--rm",
                "-v", f"{input_dir}:/mnt/input-dir:rw", 
                "-v", f"{output_dir}:/mnt/output-dir:rw", 
                "sen2cor-fmask-2.9.0", 
                scene_id
            ]
        )()
        
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
        (
            docker[
                "run", "--rm",
                "-v", f"{input_dir}:/mnt/input-dir:rw", 
                "-v", f"{output_dir}:/mnt/output-dir:rw", 
                "-v", f"{aux_data_dir}:/mnt/lasrc-aux:ro", 
                "-t", "lasrc_ledaps_fmask43:latest", 
                scene_id
            ]
        )()
        
        processed_scenes.append(os.path.join(output_dir, scene_id))
    return processed_scenes
