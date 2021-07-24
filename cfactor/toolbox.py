#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os

from typing import List


def prepare_output_directory(base_output_dir: str, pattern: str) -> str:
    """Prepare a directory to receive new data.

    Creates a new directory in `base_output_dir` based on the `pattern`
    defined by the user. The new directory can be used to store output data
    from different processing steps.

    Args:
        base_output_dir (str): Base directory where the new directory will be created.

        pattern (str): Name of the new directory that will be created.

    Returns:
        str: path to the created directory
    """
    output_dir = os.path.join(base_output_dir, pattern)
    os.makedirs(output_dir, exist_ok=True)

    return output_dir


def standardize_filename(scene_list: List[str]) -> List[str]:
    """Standardizes filenames of files loaded from `.txt` files.

    The function removes any spaces or special characters at the start and
    end of the scene names.

    Args:
        scene_list (List[str]): List of scenes names that will be processed

    Returns:
        List[str]: Standardized filenames
    """
    return list(
        map(
            lambda x: x.strip(), scene_list
        )
    )


def filename(files_path: List[str]) -> List[str]:
    """Get the file/directory name of a given path.

    Get the basename of each files path into the `files_path`.

    Args:
        files_path (List[str]): List with path to the files

    Returns:
        List[str]: List with only file/directory names.
    """
    return list(
        map(
            os.path.basename, files_path
        )
    )
