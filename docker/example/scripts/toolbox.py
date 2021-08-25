#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import hashlib
import os
import shutil
from io import BytesIO
from pathlib import Path
from typing import Union

import multihash as _multihash
import requests
import tqdm


def check_sum(file_path: Union[str, BytesIO], chunk_size=16384) -> bytes:
    """Read a file and generate a checksum using `sha256`.

    Raises:
        IOError when could not open given file.

    Args:
        file_path (str|BytesIo): Path to the file
        chunk_size (int): Size in bytes to read per iteration. Default is 16384 (16KB).

    Returns:
        The digest value in bytes.

    See:
        https://github.com/brazil-data-cube/bdc-catalog/blob/master/bdc_catalog/utils.py
    """
    algorithm = hashlib.sha256()

    def _read(stream):
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            algorithm.update(chunk)

    if isinstance(file_path, str) or isinstance(file_path, Path):
        with open(str(file_path), "rb") as f:
            _read(f)
    else:
        _read(file_path)

    return algorithm.digest()


def multihash_checksum_sha256(file_path: Union[str, BytesIO]):
    """Generate the checksum multihash.

    This method follows the spec `multihash <https://github.com/multiformats/multihash>`_.
    We use `sha256` as described in ``check_sum``. The multihash spec defines the code `0x12` for `sha256` and
    must have `0x20` (32 chars) length.

    See more in https://github.com/multiformats/py-multihash/blob/master/multihash/constants.py#L4

    Args:
        file_path (str|BytesIo): Path to the file

    Returns:
        A string-like hash in hex-decimal

    See:
        https://github.com/brazil-data-cube/bdc-catalog/blob/master/bdc_catalog/utils.py
    """
    sha256 = 0x12
    sha256_length = 0x20

    _hash = _multihash.encode(digest=check_sum(file_path), code=sha256, length=sha256_length)

    return _multihash.to_hex_string(_hash)


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
