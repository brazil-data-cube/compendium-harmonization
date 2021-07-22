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


def lc8_generate_angles(input_dir: str, scene_ids: List[str]) -> List[str]:
    """ToDo: Add description
    
    Args:
        input_dir (str): Directory where the directories of the scenes to be 
        processed are located.
                        
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
        (
            docker[
                "run", "--rm",
                "-v", f"{input_dir}:/mnt/input-dir:rw",
                "marujore/l8angs@sha256:940d6bcbd765acdb20a69ec140029d7e14bfaa8e668344fb674447b439cc36db", scene_id
            ]
        )()

        processed_scenes.append(scene_id)
    return processed_scenes


def lc8_nbar(input_dir: str, output_dir: str, scene_ids: List[str]) -> List[str]:
    """ToDo: Add description
    
    Args:
        input_dir (str): Directory where the directories of the scenes to be 
        processed are located.
                        
        output_dir (str): Directory where the results will be saved.

        scene_ids (List[str]): List with the scene_ids that should be processed.
        The scene_ids defined must be equivalent to the scene directory names in
        the `input_dir`.
            
    Returns:
        List[str]: List with full path for each nbar scene generated.
    """
    processed_scenes = []
    for scene_id in scene_ids:
        (
            docker[
                "run", "--rm",
                "-v", f"{os.path.join(input_dir, scene_id)}:/mnt/input-dir:ro",
                "-v", f"{output_dir}:/mnt/output-dir:rw",
                "marujore/nbar@sha256:154d96558ee7131664eba78ad07f730765127393e6ea459a4c3bcb8b51a5c662",
                scene_id
            ]
        )()

        processed_scenes.append(os.path.join(output_dir, scene_id))
    return processed_scenes


def s2_sen2cor_nbar(input_dir: str, output_dir: str, scene_ids: List[str]) -> List[str]:
    """ToDo: Add description

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
        (
            docker[
                "run", "--rm",
                "-v", f"{input_dir}:/mnt/input-dir:rw",
                "-v", f"{output_dir}:/mnt/output-dir:rw",
                "marujore/nbar@sha256:154d96558ee7131664eba78ad07f730765127393e6ea459a4c3bcb8b51a5c662",
                scene_id
            ]
        )()

        processed_scenes.append(os.path.join(output_dir, scene_id))
    return processed_scenes


def s2_lasrc_nbar(input_dir: str, output_dir: str, scene_ids: List[str]) -> List[str]:
    """ToDo: Add description

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
        (
            docker[
                "run", "--rm",
                "-v", f"{input_dir}:/mnt/input-dir:rw",
                "-v", f"{output_dir}:/mnt/output-dir:rw",
                "marujore/nbar@sha256:154d96558ee7131664eba78ad07f730765127393e6ea459a4c3bcb8b51a5c662",
                scene_id
            ]
        )()

        processed_scenes.append(os.path.join(output_dir, scene_id))
    return processed_scenes
