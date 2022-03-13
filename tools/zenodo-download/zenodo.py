#
# This file is part of research-processing library
# Copyright (C) 2021 INPE.
#
# research-processing is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import urllib.parse

import hashlib

import requests
from tqdm import tqdm

from pathlib import Path
from typing import Union

from pydash import py_


def download_file(
    file_url: str,
    output_file: Union[str, Path],
    overwrite: bool = False,
    block_size: int = 1024**2,
    **kwargs
) -> Path:
    """Download file.

    Args:
        file_url (str): URL of the file to be downloaded.

        output_file (Union[str, Path]): File where the downloaded content will be saved.

        overwrite (bool): Flag indicating if already existing files should be overwritten.

        block_size (int): Block download size.

        **kwargs: Extra parameters to the `requests.get` function.
    Returns:
        Path: Path where the file are saved.

    Note:
        This function is adapted from: https://gist.github.com/hossainel/0d36a86246c83dc406897464cfc5b460
    """
    output_file = Path(output_file)

    if output_file.exists() and not overwrite:
        raise FileExistsError(
            "The specified `output_file` already exists! If needed, you can use the `overwrite=True` option."
        )

    response = requests.get(file_url, stream=True, **kwargs)

    # creating the progress bar
    total_size = int(response.headers.get("content-length", 0))
    progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)

    with output_file.open(mode="wb") as ofile:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))

            ofile.write(data)

    progress_bar.close()
    return output_file


def download_zenodo_record_files(
    zenodo_record_id: str,
    output_directory: Union[str, Path],
    zenodo_record_api_url: str = "https://zenodo.org/api/records/",
    validate_checksum: bool = True,
    overwrite: bool = False,
    **kwargs
) -> Path:
    """Download all files from a zenodo record.

    Args:
        zenodo_record_id (str): Zenodo Record ID.

        output_directory (Union[str, Path]): Directory where the downloaded files will be saved.

        zenodo_record_api_url (str): Zenodo Record API endpoint API (e.g., https://zenodo.org/api/records/).

        validate_checksum (bool): Flag indicating if the file checksum should be verified.

        overwrite (bool): Flag indicating if already existing files should be overwritten.

        **kwargs: Extra parameters to the `requests.get` function.
    Returns:
        Path: Directory where the files are saved.
    """
    output_directory = Path(output_directory)

    if output_directory.exists() and not overwrite:
        raise FileExistsError(
            "The specified `output_directory` already exists! If needed, you can use the `overwrite=True` option."
        )

    # creating the zenodo record url
    zenodo_record_url = urllib.parse.urljoin(zenodo_record_api_url, zenodo_record_id)

    response = requests.get(zenodo_record_url, **kwargs)
    response.raise_for_status()

    # getting the available files in the record
    record_document = response.json()

    record_files = (
        py_.chain(record_document)
        .get("files", [])
        .map(
            lambda file: {
                "name": py_.get(file, "key"),
                "url": py_.get(file, "links.self"),
                "checksum": py_.get(file, "checksum").replace("md5:", ""),
            }
        )
    ).value()

    # downloading the files
    output_directory.mkdir(exist_ok=True)

    for record_file in record_files:
        print(py_.get(record_file, "name"))
        output_file = output_directory / py_.get(record_file, "name")

        output_file = download_file(
            py_.get(record_file, "url"), output_file, True, **kwargs
        )

        if validate_checksum:
            file_md5 = hashlib.md5(output_file.open(mode="rb").read()).hexdigest()
            assert file_md5 == py_.get(record_file, "checksum")

    return output_directory
