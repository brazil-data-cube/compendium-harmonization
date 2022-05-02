#
# This file is part of compendium-harmonization
# Copyright (C) 2021-2022 INPE.
#
# compendium-harmonization is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import tqdm
import requests

import os
import shutil

from typing import Union


def download_file(url: str, file: str) -> None:
    """Download files from a given URL.

    Args:
        url (str): file URL

        file (str): file where the downloaded ntent will be saved.

    Returns:
        None
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with open(file, "wb") as f:
            pbar = tqdm.tqdm(ncols=100, unit_scale=True, unit="B",
                             leave=None, total=(int(r.headers['Content-Length'])))
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    pbar.update(len(chunk))
                    f.write(chunk)


def extract_packed_files(filename_zip: str, output_directory: str) -> Union[str, None]:
    """Extract packed files (in most common formats like "zip", "tar" and others).

    This function creates an output directory based on the name of the compressed file and extracts its contents.
    It builds on the functionality of shutil.unpack_archive, providing support for different file formats.

    Args:
        filename_zip (str): Path to the zip that will be extracted.

        output_directory (str): Directory where the extracted content will be saved.

    Returns:
        str: path to the extracted content
    """
    # create a directory to extract the values
    filename = os.path.splitext(os.path.basename(filename_zip))[0]

    output_directory = os.path.join(output_directory, filename)
    os.makedirs(output_directory, exist_ok=True)

    shutil.unpack_archive(filename_zip, output_directory)

    return output_directory
