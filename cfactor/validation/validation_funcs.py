#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import json
import matplotlib.pyplot as plt
from datetime import datetime
from operator import itemgetter

# 3rd party
import numpy
import rasterio
from rasterio.enums import Resampling
from rasterio.io import MemoryFile
from rasterio.transform import Affine
from rasterio.warp import reproject, calculate_default_transform
from rasterio.windows import Window
from shapely.geometry import box
from typing import Dict, List, Optional, Tuple


def reproject_img(src: rasterio.io.DatasetReader, ref: rasterio.io.DatasetReader) -> rasterio.io.MemoryFile:
    """Reproject an image from a source dataset to a reference dataset.

    Args:
        src (rasterio.io.DatasetReader): Rasterio source dataset that will be reprojected into the reference projection.

        ref (rasterio.io.DatasetReader): Rasterio reference dataset.

    Returns:
        rasterio.io.MemoryFile: Reprojected dataset.

    """
    transform, width, height = calculate_default_transform(src.crs, ref.crs, src.width, src.height, *src.bounds,
                                                           resolution=ref.transform[0])
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': ref.crs,
        'transform': transform,
        'width': width,
        'height': height
    })
    with MemoryFile() as memfile:
        intermed_dataset = memfile.open(
            driver='GTiff',
            height=kwargs['height'],
            width=kwargs['width'],
            count=kwargs['count'],
            dtype=kwargs['dtype'],
            crs=kwargs['crs'],
            transform=kwargs['transform'],
            nodata=kwargs['nodata']
        )
        reproject(
            source=rasterio.band(src, 1),
            destination=rasterio.band(intermed_dataset, 1),
            src_transform=intermed_dataset.transform,
            src_crs=intermed_dataset.crs,
            dst_transform=transform,
            dst_crs=ref.crs,
            dst_resolution=transform[0],
            resampling=Resampling.nearest)

    return intermed_dataset


def resample_raster(src: rasterio.io.DatasetReader, res: int) -> rasterio.io.MemoryFile:
    """Resample an image from a source dataset to a reference dataset.

    Args:
        src (rasterio.io.DatasetReader): Rasterio Source dataset that will be resampled into the reference projection.

        res (int): Rasterio reference dataset.

    Returns:
        rasterio.io.MemoryFile: Resampled dataset.

    """
    transform, width, height = calculate_default_transform(src.crs, src.crs, src.width, src.height, *src.bounds,
                                                           resolution=res)
    kwargs = src.meta.copy()
    kwargs.update({
        'transform': transform,
        'width': width,
        'height': height
    })
    with MemoryFile() as memfile:
        intermed_dataset = memfile.open(
            driver='GTiff',
            height=kwargs['height'],
            width=kwargs['width'],
            count=kwargs['count'],
            dtype=kwargs['dtype'],
            crs=kwargs['crs'],
            transform=kwargs['transform'],
            nodata=kwargs['nodata']
        )
        reproject(
            source=rasterio.band(src, 1),
            destination=rasterio.band(intermed_dataset, 1),
            src_transform=intermed_dataset.transform,
            src_crs=intermed_dataset.crs,
            dst_transform=transform,
            dst_crs=src.crs,
            dst_resolution=transform[0],
            resampling=Resampling.nearest)

    return intermed_dataset


def raster_intersection(raster1: rasterio.io.DatasetReader, raster2: rasterio.io.DatasetReader) -> Tuple[
    numpy.ndarray, numpy.ndarray]:
    """Obtain the intersection between two rasters.

    Args:
        raster1 (rasterio.io.DatasetReader): Rasterio dataset of the first raster.

        raster2 (rasterio.io.DatasetReader): Rasterio dataset of the second raster.

    Returns:
        raster1_arr (numpy.ndarray) - numpy.array containing values from raster1 on the intersection area.

        raster2_arr (numpy.ndarray) - numpy.array containing values from raster2 on the intersection area.

    """
    # Check if data on same crs, if different must reproject
    if raster1.crs != raster2.crs:
        raster2 = reproject_img(raster2, raster1)

    bb_raster1 = box(raster1.bounds[0], raster1.bounds[1], raster1.bounds[2], raster1.bounds[3])
    bb_raster2 = box(raster2.bounds[0], raster2.bounds[1], raster2.bounds[2], raster2.bounds[3])

    xminR1, yminR1, xmaxR1, ymaxR1 = raster1.bounds
    xminR2, yminR2, xmaxR2, ymaxR2 = raster2.bounds

    intersection = bb_raster1.intersection(bb_raster2)
    transform = Affine(raster1.res[0], 0.0, intersection.bounds[0], 0.0, -raster1.res[1], intersection.bounds[3])

    p1Y = intersection.bounds[3] - raster1.res[1] / 2
    p1X = intersection.bounds[0] + raster1.res[0] / 2
    p2Y = intersection.bounds[1] + raster1.res[1] / 2
    p2X = intersection.bounds[2] - raster1.res[0] / 2
    # row index raster1
    row1R1 = int((ymaxR1 - p1Y) / raster1.res[1])
    # row index raster2
    row1R2 = int((ymaxR2 - p1Y) / raster2.res[1])
    # column index raster1
    col1R1 = int((p1X - xminR1) / raster1.res[0])
    # column index raster2
    col1R2 = int((p1X - xminR2) / raster1.res[0])

    # row index raster1
    row2R1 = int((ymaxR1 - p2Y) / raster1.res[1])
    # row index raster2
    row2R2 = int((ymaxR2 - p2Y) / raster2.res[1])
    # column index raster1
    col2R1 = int((p2X - xminR1) / raster1.res[0])
    # column index raster2
    col2R2 = int((p2X - xminR2) / raster1.res[0])

    width1 = col2R1 - col1R1 + 1
    width2 = col2R2 - col1R2 + 1
    height1 = row2R1 - row1R1 + 1
    height2 = row2R2 - row1R2 + 1

    raster1_arr = raster1.read(1, window=Window(col1R1, row1R1, width1, height1))
    raster2_arr = raster2.read(1, window=Window(col1R2, row1R2, width2, height2))

    return raster1_arr.astype(float), raster2_arr.astype(float)


def load_file(file_path: str) -> List[str]:
    """Open and read all lines of a file.

    Args:
        file_path (str): File path to the archive that will be readed.

    Returns:
        List[str]: List containing all lines of a file.

    """
    elements = []  # define an empty list
    with open(file_path, 'r') as filehandle:  # open file and read the content in a list
        for line in filehandle:
            currentPlace = line[:-1]  # remove linebreak which is the last character of the string
            elements.append(currentPlace)  # add item to the list

    return elements


def sort_l8_sceneids(sceneids: List[str]) -> List[str]:
    """Sort Landsat-8 sceneids according to sensing date.

    Args:
        sceneids (List[str]): List of Landsat-8 sceneids.

    Returns:
        List[str]: List of Landsat-8 sceneids ordered according to sensing date.

    """
    l8_sceneids = []
    for sceneid in sceneids:
        splited_sceneid = sceneid.split('_')
        sensing_date = datetime.strptime(splited_sceneid[3], '%Y%m%d')
        orbit = int(splited_sceneid[2])
        l8_sceneids.append([sceneid, sensing_date, orbit])

    # Order by sensing_date
    l8_sceneids = sorted(l8_sceneids, key=itemgetter(1))
    return l8_sceneids


def search_pairs_l8(sceneids_file: str, day_diff: int = 10) -> List[Tuple[str, str]]:
    """Search for Landsat-8 sceneid pairs with sensing date close in time according to day_diff.

    Args:
        sceneids_file (str): File path to archive containing Landsat-8 sceneids.

        day_diff (int): Difference of sensing date, in days, to consider two sceneids a pair.

    Returns:
        List[Tuple[str, str]]: List of pairs of Landsat-8 sceneids.

    """
    sceneids = load_file(sceneids_file)
    l8_sceneids = sort_l8_sceneids(sceneids)

    pairs = []
    uniques = set()
    for i in range(0, len(l8_sceneids) - 1):
        # Select with day difference
        if abs((l8_sceneids[i][1] - l8_sceneids[i + 1][1]).days) < day_diff:
            # Select from other orbit
            if l8_sceneids[i][2] != l8_sceneids[i + 1][2]:
                pairs.append((l8_sceneids[i][0], l8_sceneids[i + 1][0]))
                uniques.add(l8_sceneids[i][0])
                uniques.add(l8_sceneids[i + 1][0])

    return pairs


def sort_s2_sceneids(sceneids: List[str]) -> List[str]:
    """Sort Sentinel-2 sceneids according to sensing date.

    Args:
        sceneids (List[str]): List of Sentinel-2 sceneids.

    Returns:
        List[str]: List of Sentinel-2 sceneids ordered according to sensing date.

    """
    s2_sceneids = []
    for sceneid in sceneids:
        splited_sceneid = sceneid.split('_')
        sensing_date = datetime.strptime(splited_sceneid[2], '%Y%m%dT%H%M%S')
        orbit = int(splited_sceneid[4][1:])
        s2_sceneids.append([sceneid, sensing_date, orbit])

    # Order by sensing_date
    s2_sceneids = sorted(s2_sceneids, key=itemgetter(1))

    return s2_sceneids


def search_pairs_s2(sceneids_file: str, day_diff: int = 5) -> List[Tuple[str, str]]:
    """Search for Sentinel-2 sceneid pairs with sensing date close in time according to day_diff.

    Args:
        sceneids_file (str): File path to archive containing Sentinel-2 sceneids.
        day_diff (int): Difference of sensing date, in days, to consider two sceneids a pair.

    Returns:
        List[Tuple[str, str]]: List of pairs of Sentinel-2 sceneids.

    """
    sceneids = load_file(sceneids_file)
    s2_sceneids = sort_s2_sceneids(sceneids)

    pairs = []
    uniques = set()
    for i in range(0, len(s2_sceneids) - 1):
        # Select with day difference
        if abs((s2_sceneids[i][1] - s2_sceneids[i + 1][1]).days) < day_diff:
            # Select from other orbit
            if s2_sceneids[i][2] != s2_sceneids[i + 1][2]:
                pairs.append((s2_sceneids[i][0], s2_sceneids[i + 1][0]))
                uniques.add(s2_sceneids[i][0])
                uniques.add(s2_sceneids[i + 1][0])

    return pairs


def search_pairs_l8_s2(l8_sceneids_file: str, s2_sceneids_file: str, day_diff: int = 5) -> List[Tuple[str, str]]:
    """Search for Landsat-8 and Sentinel-2 sceneid pairs with sensing date close in time according to day_diff.

    Args:
        l8_sceneids_file (str): File path to archive containing Landsat-8 sceneids.

        s2_sceneids_file (str): File path to archive containing Sentinel-2 sceneids.

        day_diff (int): Difference of sensing date, in days, to consider two sceneids a pair.

    Returns:
        List[Tuple[str, str]]: List of Landsat-8 and Sentinel-2 sceneid pairs.

    """
    sceneids = load_file(l8_sceneids_file)
    l8_sceneids = sort_l8_sceneids(sceneids)

    sceneids = load_file(s2_sceneids_file)
    s2_sceneids = sort_s2_sceneids(sceneids)

    pairs = []
    for i in range(0, len(l8_sceneids)):
        for j in range(0, len(s2_sceneids)):
            # Select with day difference
            if abs((l8_sceneids[i][1] - s2_sceneids[j][1]).days) < day_diff:
                pairs.append((l8_sceneids[i][0], s2_sceneids[j][0]))

    return pairs


def mask_pixel_bitwise(mask: numpy.ndarray, flags_list: Optional[Dict] = None,
                       nodata: Optional[int] = None) -> numpy.ndarray:
    """Apply Landsat bitwise mask according to flags_list, if no flags_list is provided mask using default configuration.

    Args:
        mask (numpy.ndarray): numpy ndarray containing cloud mask.

        flags_list (Dict) (optional): Dict containing bitwise mapping.

        nodata (int) (optional): mask parameter nodata value.

    Returns:
        numpy.array (bool): Boolean numpy ndarray in which True should be masked and False contains clear observations.

    """
    if flags_list is None:
        L8_flag = {
            'fill': 1 << 0,
            'dilated_cloud': 1 << 1,
            'cirrus': 1 << 2,
            'cloud': 1 << 3,
            'shadow': 1 << 4,
            'snow': 1 << 5  # ,
            #             'clear': 1<<6,
            #             'water': 1<<7
        }
        flags_list = L8_flag
    # first we will create the result mask filled with zeros and the same shape as the mask
    final_mask = numpy.zeros_like(mask)
    if nodata is not None:
        final_mask[mask == nodata] = 1

    # then we will loop through the flags and add the
    for flag in flags_list:
        # get the mask for this flag
        flag_mask = numpy.bitwise_and(mask, flags_list[flag])

        # add it to the final flag
        final_mask = final_mask | flag_mask

    final_mask[final_mask > 0] = 1

    return final_mask.astype(bool)


def mask_pixel_scl(mask: numpy.ndarray, flags_list: Optional[Dict] = None) -> numpy.ndarray:
    """Apply Scene Classificaton Layer (SCL) mask according to flags_list, if no flags_list is provided mask using default configuration.

    Args:
        mask (numpy.ndarray): numpy.array containing cloud mask.

        flags_list (Dict) (optional): Dict containing bitwise mapping.

    Returns:
        numpy.array (bool): Boolean numpy ndarray in which True should be masked and False contains clear observations.

    """
    if flags_list is None:
        scl_flag = {
            'nodata': 0,
            'saturated_or_defective': 1,
            'dark_area_pixels': 2,
            'cloud_shadows': 3,
            # 'vegetation': 4,
            # 'not_vegetated': 5,
            # 'water': 6,
            'unclassified': 7,
            'cloud_medium_probability': 8,
            'cloud_high_probability': 9,
            'thin_cirrus': 10,
            'snow': 11,
        }
        flags_list = scl_flag
    # first we will create the result mask filled with zeros and the same shape as the mask
    final_mask = numpy.zeros_like(mask)

    # then we will loop through the flags and add the
    for flag in flags_list:
        # get the mask for this flag
        final_mask[numpy.where(mask == scl_flag[flag])] = 1

    return final_mask.astype(bool)


def write_dict(dict: Dict, file_path: str):
    """Write a dictionary into a file.

    Args:
        dict: Dictionary of values to be saved in a file.

        file_path: File path in which the dictionary will be written.

    """
    with open(file_path, 'w') as file:
        file.write(json.dumps(dict))


def calc_all_pairs(comparison_metrics: Dict, bands: List[str], pairs: Tuple[str, str]) -> Dict:
    """Calculate absolute difference mean (abs_dif_mean) and relative absolute percentage mean (relative_abs_perc_mean) of a dictionary containing abs_dif_mean and relative_abs_perc_mean of several comparisons.

    Args:
        comparison_metrics (Dict): Dictionary of abs_dif_mean and relative_abs_perc_mean values organized by band.

        bands (List[str]): Band name.

        pairs (Tuple[str, str]): Tuple of sceneid pairs.

    Returns:
        Dict: Dictionary containing the mean value of abs_dif_mean and relative_abs_perc_mean organized by band.

    """
    comparison_metrics['all_pairs'] = {}
    for b in range(len(bands)):
        comparison_metrics['all_pairs'][bands[b]] = {}
        sum_abs_dif = []
        sum_relative_abs_perc = []
        for pair in pairs:
            sum_abs_dif.append(comparison_metrics[pair[0] + '_x_' + pair[1]][bands[b]]['abs_dif_mean'])
            sum_relative_abs_perc.append(comparison_metrics[pair[0] + '_x_' + pair[1]][bands[b]]['rel_abs_perc_mean'])
        comparison_metrics['all_pairs'][bands[b]]['abs_dif_mean'] = numpy.nanmean(sum_abs_dif)
        comparison_metrics['all_pairs'][bands[b]]['rel_abs_perc_mean'] = numpy.nanmean(sum_relative_abs_perc)
    print(comparison_metrics['all_pairs'])
    return comparison_metrics


def remove_negative_vals(raster1_arr: numpy.ndarray, raster2_arr: numpy.ndarray) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """Remove negative reflectance artifacts.

    Args:
        raster1_arr (numpy.ndarray): numpy.array of the first raster.

        raster2_arr (numpy.ndarray): numpy.array of the second raster.

    Returns:
        raster1_arr (numpy.ndarray): numpy ndarray containing values from raster1_arr only on the positions where raster1_arr and raster2_arr where not negative.

        raster2_arr (numpy.ndarray): numpy ndarray containing values from raster2_arr only on the positions where raster1_arr and raster2_arr where not negative.

    """
    raster2_arr[raster1_arr < 0] = numpy.nan
    raster1_arr[raster1_arr < 0] = numpy.nan
    raster1_arr[raster2_arr < 0] = numpy.nan
    raster2_arr[raster2_arr < 0] = numpy.nan

    return raster1_arr, raster2_arr
