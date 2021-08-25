#
# This file is part of c-factor library
# Copyright (C) 2021 INPE.
#
# c-factor is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os
from re import A

import numpy
import rasterio
from typing import Dict, List, Tuple

from tempfile import mktemp

from cfactor.validation import navigate, validation_funcs


def create_a_temporary_file_with_lines(lines: List[str]) -> str:
    """Create a temporary text file.

    Args:
        lines (List[str]): Text lines that will be added on the file.

    Returns:
        str: Path to the temporary file.
    """

    file = mktemp()
    with open(file, "w") as stream:
        stream.writelines(list(
            map(
                lambda x: f"{x}\n", lines
            )
        ))
    return file


def validation(raster1_arr: numpy.ndarray, raster2_arr: numpy.ndarray) -> Tuple[float, float]:
    """Calculate absolute difference mean (abs_dif_mean) and relative absolute percentage mean (relative_abs_perc_mean) from two arrays.

    Args:
        raster1_arr (numpy.ndarray): First numpy.array.

        raster2_arr (numpy.ndarray): Second numpy.array.

    Returns:
        abs_dif_mean (float): Absolute difference mean (abs_dif_mean).

        relative_abs_perc_mean (float): Relative absolute percentage mean (relative_abs_perc_mean).
    """

    raster1_arr, raster2_arr = validation_funcs.remove_negative_vals(raster1_arr, raster2_arr)

    # Compare
    abs_dif = abs(raster1_arr - raster2_arr)
    abs_dif_mean = numpy.nanmean(abs_dif)
    abs_sum = abs(raster1_arr + raster2_arr)
    relative_abs_perc = numpy.divide((2 * abs_dif), abs_sum, out=numpy.zeros_like(2 * abs_dif),
                                     where=abs_sum != 0)
    relative_abs_perc_mean = numpy.nanmean(relative_abs_perc) * 100

    return abs_dif_mean, relative_abs_perc_mean


def add_comparison(obj: Dict, name: str, band: str, **kwargs: Dict) -> None:
    """Store values into a dict organized by name and bands, or create a new one if it doesn't
    exist, and store values in it.

    Args:
        obj (Dict): Dictionary object that will store the values.

        name (str): key name.

        band (str): key band.

        **kwargs (Dict): values that will be stored.

    Returns:
        None: The values will be stored in-place on the `obj` dictionary.
    """
    if not obj.get(name):
        obj[name] = {}
    obj[name][band] = kwargs


def validation_sr_l8(input_dir: str, cloud_dir: str, output_dir: str, pairs: Tuple[str, str], bands: List[str]):
    """Performs validation on Landsat-8 Surface Reflectance data.

    Args:
        input_dir (str): Directory containing Landsat-8 Surface Reflectance folders.

        cloud_dir (str): Directory containing Landsat-8 folders that contains cloud masks.

        output_dir (str): Directory in which the validation values will be written.

        pairs (Tuple[str,str]): Tuple containing a pair of sceneids that will be evaluated.

        bands (List[str]): name of the bands that will be evaluated.

    """
    comparison_metrics = {}

    for pair in pairs:
        name = pair[0] + '_x_' + pair[1]
        # Prepare Cloud Mask
        cloud1_ds = rasterio.open(navigate.path_to_l8cloud(cloud_dir, pair[0]))
        cloud2_ds = rasterio.open(navigate.path_to_l8cloud(cloud_dir, pair[1]))
        cloud1_arr, cloud2_arr = validation_funcs.raster_intersection(cloud1_ds, cloud2_ds)
        mask1 = validation_funcs.mask_pixel_bitwise(cloud1_arr.astype(int), nodata=0)
        mask2 = validation_funcs.mask_pixel_bitwise(cloud2_arr.astype(int), nodata=0)
        mask = numpy.logical_or(mask1, mask2)  # Combined mask

        for b in bands:
            # Load files
            print(f"Comparing pair {pair} band {b}")
            raster1_path = navigate.path_to_l8srband(input_dir, pair[0], b)
            raster2_path = navigate.path_to_l8srband(input_dir, pair[1], b)
            raster1_ds = rasterio.open(raster1_path)
            raster2_ds = rasterio.open(raster2_path)

            # Get raster intersection
            raster1_arr, raster2_arr = validation_funcs.raster_intersection(raster1_ds, raster2_ds)

            # Apply Cloud mask
            raster1_arr[mask] = numpy.nan
            raster2_arr[mask] = numpy.nan

            # Rescale
            raster1_arr = ((raster1_arr * 0.275) - 2000)  # Rescale data to 0-10000 -> ((raster1_arr * 0.0000275)-0.2)
            raster2_arr = ((raster2_arr * 0.275) - 2000)  # Rescale data to 0-10000 -> ((raster1_arr * 0.0000275)-0.2)

            abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr)

            # Store
            add_comparison(comparison_metrics, name, b, abs_dif_mean=abs_dif_mean,
                           rel_abs_perc_mean=relative_abs_perc_mean)

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands, pairs)
    validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics_sr_l8.json'))


# OK
def validation_nbar_l8(input_dir: str, cloud_dir: str, output_dir: str, pairs: Tuple[str, str], bands: List[str]):
    """Performs validation on Landsat-8 NBAR data.

    Args:
        input_dir (str): Directory containing Landsat-8 NBAR folders.

        cloud_dir (str): Directory containing Landsat-8 folders that contains cloud masks.

        output_dir (str): Directory in which the validation values will be written.

        pairs (Tuple[str,str]): Tuple containing a pair of sceneids that will be evaluated.

        bands (List[str]): name of the bands that will be evaluated.

    """
    comparison_metrics = {}

    for pair in pairs:
        name = pair[0] + '_x_' + pair[1]
        # Prepare Cloud Mask
        cloud1_ds = rasterio.open(navigate.path_to_l8cloud(cloud_dir, pair[0]))
        cloud2_ds = rasterio.open(navigate.path_to_l8cloud(cloud_dir, pair[1]))
        cloud1_arr, cloud2_arr = validation_funcs.raster_intersection(cloud1_ds, cloud2_ds)
        mask1 = validation_funcs.mask_pixel_bitwise(cloud1_arr.astype(int), nodata=0)
        mask2 = validation_funcs.mask_pixel_bitwise(cloud2_arr.astype(int), nodata=0)
        mask = numpy.logical_or(mask1, mask2)  # Combined mask

        for b in bands:
            # Load files
            print(f"Comparing pair {pair} band {b}")
            raster1_path = navigate.path_to_l8nbarband(input_dir, pair[0], b)
            raster2_path = navigate.path_to_l8nbarband(input_dir, pair[1], b)
            raster1_ds = rasterio.open(raster1_path)
            raster2_ds = rasterio.open(raster2_path)

            # Get raster intersection
            raster1_arr, raster2_arr = validation_funcs.raster_intersection(raster1_ds, raster2_ds)

            # Apply Cloud mask
            raster1_arr[mask] = numpy.nan
            raster2_arr[mask] = numpy.nan

            abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr)

            # Store
            add_comparison(comparison_metrics, name, b, abs_dif_mean=abs_dif_mean,
                           rel_abs_perc_mean=relative_abs_perc_mean)

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands, pairs)
    validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics_nbar_l8.json'))


def validation_sr_s2_sen2cor(input_dir: str, cloud_dir: str, output_dir: str, pairs: Tuple[str, str],
                             bands10m: List[str], bands20m: List[str]) -> None:
    """Performs validation on Sentinel-2 (Sen2cor) Surface Reflectance data.

    Args:
        input_dir (str): Directory containing Sentinel-2 (Sen2cor) Surface Reflectance folders.

        cloud_dir (str): Directory containing Sentinel-2 folders that contains cloud masks.

        output_dir (str): Directory in which the validation values will be written.

        pairs (Tuple[str,str]): Tuple containing a pair of sceneids that will be evaluated.

        bands10m (List[str]): name of the 10 meter bands that will be evaluated.

        bands20m (List[str]): name of the 20 meter bands that will be evaluated.

    """

    bands = bands10m + bands20m
    comparison_metrics = {}

    for pair in pairs:
        name = pair[0] + '_x_' + pair[1]
        comparison_metrics[pair[0] + '_x_' + pair[1]] = {}
        # Prepare Cloud Mask
        cloud1_path = navigate.path_to_s2l2a_cloud(cloud_dir, pair[0])
        cloud2_path = navigate.path_to_s2l2a_cloud(cloud_dir, pair[1])

        for b in bands:
            cloud1_ds = rasterio.open(cloud1_path)
            cloud2_ds = rasterio.open(cloud2_path)
            print(f"Comparing pair {pair} band {b}")
            if b in bands20m:
                res = 20
            elif b in bands10m:
                res = 10
                cloud1_ds = validation_funcs.resample_raster(cloud1_ds, res)
                cloud2_ds = validation_funcs.resample_raster(cloud2_ds, res)
            cloud1_arr, cloud2_arr = validation_funcs.raster_intersection(cloud1_ds, cloud2_ds)
            mask1 = validation_funcs.mask_pixel_scl(cloud1_arr)
            mask2 = validation_funcs.mask_pixel_scl(cloud2_arr)
            mask = numpy.logical_or(mask1, mask2)  # Combined mask

            # Load files
            raster1_ds = rasterio.open(navigate.path_to_s2srsen2cor_band(input_dir, pair[0], b)[0])
            raster2_ds = rasterio.open(navigate.path_to_s2srsen2cor_band(input_dir, pair[1], b)[0])

            # Get raster intersection
            raster1_arr, raster2_arr = validation_funcs.raster_intersection(raster1_ds, raster2_ds)

            # Apply Cloud mask
            raster1_arr[mask] = numpy.nan
            raster2_arr[mask] = numpy.nan

            abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr)

            # Store
            add_comparison(comparison_metrics, name, b, abs_dif_mean=abs_dif_mean,
                           rel_abs_perc_mean=relative_abs_perc_mean)

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands, pairs)

    validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics_sr_s2_sen2cor.json'))


def validation_nbar_s2_sen2cor(input_dir: str, cloud_dir: str, output_dir: str, pairs: Tuple[str, str],
                               bands10m: List[str], bands20m: List[str]) -> None:
    """Performs validation on Sentinel-2 (Sen2cor) NBAR data.

    Args:
        input_dir (str): Directory containing Sentinel-2 (Sen2cor) NBAR folders.

        cloud_dir (str): Directory containing Sentinel-2 folders that contains cloud masks.

        output_dir (str): Directory in which the validation values will be written.

        pairs (Tuple[str,str]): Tuple containing a pair of sceneids that will be evaluated.

        bands10m (List[str]): name of the 10 meter bands that will be evaluated.

        bands20m (List[str]): name of the 20 meter bands that will be evaluated.

    """

    bands = bands10m + bands20m
    comparison_metrics = {}

    for pair in pairs:
        name = pair[0] + '_x_' + pair[1]
        comparison_metrics[pair[0] + '_x_' + pair[1]] = {}
        # Prepare Cloud Mask
        cloud1_path = navigate.path_to_s2l2a_cloud(cloud_dir, pair[0])
        cloud2_path = navigate.path_to_s2l2a_cloud(cloud_dir, pair[1])

        for b in bands:
            cloud1_ds = rasterio.open(cloud1_path)
            cloud2_ds = rasterio.open(cloud2_path)
            print(f"Comparing pair {pair} band {b}")
            if b in bands20m:
                res = 20
            elif b in bands10m:
                res = 10
                cloud1_ds = validation_funcs.resample_raster(cloud1_ds, res)
                cloud2_ds = validation_funcs.resample_raster(cloud2_ds, res)
            cloud1_arr, cloud2_arr = validation_funcs.raster_intersection(cloud1_ds, cloud2_ds)
            mask1 = validation_funcs.mask_pixel_scl(cloud1_arr)
            mask2 = validation_funcs.mask_pixel_scl(cloud2_arr)
            mask = numpy.logical_or(mask1, mask2)  # Combined mask

            # Load files
            raster1_ds = rasterio.open(navigate.path_to_s2nbarsen2cor_band(input_dir, pair[0], b)[0])
            raster2_ds = rasterio.open(navigate.path_to_s2nbarsen2cor_band(input_dir, pair[1], b)[0])

            # Get raster intersection
            raster1_arr, raster2_arr = validation_funcs.raster_intersection(raster1_ds, raster2_ds)

            # Apply Cloud mask
            raster1_arr[mask] = numpy.nan
            raster2_arr[mask] = numpy.nan

            abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr)

            # Store
            add_comparison(comparison_metrics, name, b, abs_dif_mean=abs_dif_mean,
                           rel_abs_perc_mean=relative_abs_perc_mean)

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands, pairs)

    validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics_nbar_s2_sen2cor.json'))


def validation_sr_s2_lasrc(input_dir: str, cloud_dir: str, output_dir: str, pairs: Tuple[str, str],
                           bands: List[str]) -> None:
    """Performs validation on Sentinel-2 (LaSRC) Surface Reflectance data.

    Args:
        input_dir (str): Directory containing Sentinel-2 (LaSRC) Surface Reflectance folders.

        cloud_dir (str): Directory containing Sentinel-2 folders that contains cloud masks.

        output_dir (str): Directory in which the validation values will be written.

        pairs (Tuple[str,str]): Tuple containing a pair of sceneids that will be evaluated.

        bands (List[str]): name of the bands that will be evaluated.

    """
    comparison_metrics = {}

    for pair in pairs:
        name = pair[0] + '_x_' + pair[1]
        comparison_metrics[pair[0] + '_x_' + pair[1]] = {}
        # Prepare Cloud Mask
        cloud1_ds = rasterio.open(navigate.path_to_s2l2a_cloud(cloud_dir, pair[0]))
        cloud2_ds = rasterio.open(navigate.path_to_s2l2a_cloud(cloud_dir, pair[1]))

        cloud1_ds = validation_funcs.resample_raster(cloud1_ds, 10)
        cloud2_ds = validation_funcs.resample_raster(cloud2_ds, 10)

        cloud1_arr, cloud2_arr = validation_funcs.raster_intersection(cloud1_ds, cloud2_ds)
        mask1 = validation_funcs.mask_pixel_scl(cloud1_arr)
        mask2 = validation_funcs.mask_pixel_scl(cloud2_arr)
        mask = numpy.logical_or(mask1, mask2)  # Combined mask

        for b in bands:
            # Load files
            print(f"Comparing pair {pair} band {b}")
            raster1_path = navigate.path_to_s2srlasrc_band(input_dir, pair[0], b)
            raster2_path = navigate.path_to_s2srlasrc_band(input_dir, pair[1], b)
            raster1_ds = rasterio.open(raster1_path)
            raster2_ds = rasterio.open(raster2_path)

            # Get raster intersection
            raster1_arr, raster2_arr = validation_funcs.raster_intersection(raster1_ds, raster2_ds)

            # Apply Cloud mask
            raster1_arr[mask] = numpy.nan
            raster2_arr[mask] = numpy.nan

            abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr)

            # Store
            add_comparison(comparison_metrics, name, b, abs_dif_mean=abs_dif_mean,
                           rel_abs_perc_mean=relative_abs_perc_mean)

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands, pairs)

    validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics_sr_s2_lasrc.json'))


def validation_nbar_s2_lasrc(input_dir: str, cloud_dir: str, output_dir: str, pairs: Tuple[str, str],
                             bands: List[str]) -> None:
    """Performs validation on Sentinel-2 (LaSRC) NBAR data.

    Args:
        input_dir (str): Directory containing Sentinel-2 (LaSRC) NBAR folders.

        cloud_dir (str): Directory containing Sentinel-2 folders that contains cloud masks.

        output_dir (str): Directory in which the validation values will be written.

        pairs (Tuple[str,str]): Tuple containing a pair of sceneids that will be evaluated.

        bands (List[str]): name of the bands that will be evaluated.

    """
    comparison_metrics = {}

    for pair in pairs:
        name = pair[0] + '_x_' + pair[1]
        comparison_metrics[pair[0] + '_x_' + pair[1]] = {}
        # Prepare Cloud Mask
        cloud1_ds = rasterio.open(navigate.path_to_s2l2a_cloud(cloud_dir, pair[0]))
        cloud2_ds = rasterio.open(navigate.path_to_s2l2a_cloud(cloud_dir, pair[1]))

        cloud1_ds = validation_funcs.resample_raster(cloud1_ds, 10)
        cloud2_ds = validation_funcs.resample_raster(cloud2_ds, 10)

        cloud1_arr, cloud2_arr = validation_funcs.raster_intersection(cloud1_ds, cloud2_ds)
        mask1 = validation_funcs.mask_pixel_scl(cloud1_arr)
        mask2 = validation_funcs.mask_pixel_scl(cloud2_arr)
        mask = numpy.logical_or(mask1, mask2)  # Combined mask

        for b in bands:
            # Load files
            print(f"Comparing pair {pair} band {b}")
            raster1_path = navigate.path_to_s2nbarlasrc_band(input_dir, pair[0], b)
            raster2_path = navigate.path_to_s2nbarlasrc_band(input_dir, pair[1], b)
            raster1_ds = rasterio.open(raster1_path)
            raster2_ds = rasterio.open(raster2_path)

            # Get raster intersection
            raster1_arr, raster2_arr = validation_funcs.raster_intersection(raster1_ds, raster2_ds)

            # Apply Cloud mask
            raster1_arr[mask] = numpy.nan
            raster2_arr[mask] = numpy.nan

            abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr)

            # Store
            add_comparison(comparison_metrics, name, b, abs_dif_mean=abs_dif_mean,
                           rel_abs_perc_mean=relative_abs_perc_mean)

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands, pairs)

    validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics_nbar_s2_lasrc.json'))


def validation_sr_l8_s2_sen2cor(input_dir_l8: str, cloud_dir_l8: str, input_dir_s2: str, cloud_dir_s2: str,
                                output_dir: str, pairs: Tuple[str, str], bands_l8: List[str],
                                bands_s2: List[str]) -> None:
    """Performs validation on both Landsat-8 and Sentinel-2 (Sen2cor) surface reflectance data.

    Args:
        input_dir_l8 (str): Directory containing Landsat-8 surface reflectance folders.

        cloud_dir_l8 (str): Directory containing Landsat-8 folders that contains cloud masks.

        input_dir_s2 (str): Directory containing Sentinel-2 (Sen2cor) surface reflectance folders.

        cloud_dir_s2 (str): Directory containing Sentinel-2 folders that contains cloud masks.

        output_dir (str): Directory in which the validation values will be written.

        pairs (Tuple[str,str]): Tuple containing a pair of sceneids that will be evaluated.

        bands_l8 (List[str]): Landsat-8 bands that will be evaluated.

        bands_s2 (List[str]): Sentinel-2 bands that will be evaluated (Sen2cor syntax).

    """

    comparison_metrics = {}

    for pair in pairs:
        name = pair[0] + '_x_' + pair[1]
        comparison_metrics[pair[0] + '_x_' + pair[1]] = {}
        # Prepare Cloud Mask
        cloud1_path = navigate.path_to_l8cloud(cloud_dir_l8, pair[0])
        cloud2_path = navigate.path_to_s2l2a_cloud(cloud_dir_s2, pair[1])

        cloud1_ds = rasterio.open(cloud1_path)
        cloud2_ds = rasterio.open(cloud2_path)

        cloud1_ds = validation_funcs.resample_raster(cloud1_ds, 10)
        cloud2_ds = validation_funcs.resample_raster(cloud2_ds, 10)

        cloud1_arr, cloud2_arr = validation_funcs.raster_intersection(cloud1_ds, cloud2_ds)
        mask1 = validation_funcs.mask_pixel_bitwise(cloud1_arr.astype(int), nodata=0)
        mask2 = validation_funcs.mask_pixel_scl(cloud2_arr)
        mask = numpy.logical_or(mask1, mask2)  # Combined mask

        for b in range(len(bands_l8)):
            print(f"Comparing pair {pair} band {bands_l8[b]}")

            # Load files
            raster1_ds = rasterio.open(navigate.path_to_l8srband(input_dir_l8, pair[0], bands_l8[b]))
            raster1_ds = validation_funcs.resample_raster(raster1_ds, 10)

            raster2_path, res = navigate.path_to_s2srsen2cor_band(input_dir_s2, pair[1], bands_s2[b])
            raster2_ds = rasterio.open(raster2_path)
            if res != 10:
                raster2_ds = validation_funcs.resample_raster(raster2_ds, 10)

            # Get raster intersection
            raster1_arr, raster2_arr = validation_funcs.raster_intersection(raster1_ds, raster2_ds)

            # Apply Cloud mask
            raster1_arr[mask] = numpy.nan
            raster2_arr[mask] = numpy.nan

            # Rescale
            raster1_arr = ((raster1_arr * 0.275) - 2000)  # Rescale data to 0-10000 -> ((raster1_arr * 0.0000275)-0.2)

            abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr)

            # Store
            add_comparison(comparison_metrics, name, bands_l8[b], abs_dif_mean=abs_dif_mean,
                           rel_abs_perc_mean=relative_abs_perc_mean)

            del raster1_ds, raster2_ds, raster1_arr, raster2_arr, abs_dif_mean, relative_abs_perc_mean
        del cloud1_ds, cloud2_ds, cloud1_arr, cloud2_arr, mask1, mask2, mask

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands_l8, pairs)
    validation_funcs.write_dict(comparison_metrics,
                                os.path.join(output_dir, 'comparison_metrics_sr_l8_s2_sen2cor.json'))


def validation_sr_l8_s2_lasrc(input_dir_l8: str, cloud_dir_l8: str, input_dir_s2: str, cloud_dir_s2: str,
                              output_dir: str, pairs: Tuple[str, str], bands_l8: List[str], bands_s2: List[str]):
    """Performs validation on both Landsat-8 and Sentinel-2 (LaSRC) surface reflectance data.

    Args:
        input_dir_l8 (str): Directory containing Landsat-8 surface reflectance folders.

        cloud_dir_l8 (str): Directory containing Landsat-8 folders that contains cloud masks.

        input_dir_s2 (str): Directory containing Sentinel-2 (LaSRC) surface reflectance folders.

        cloud_dir_s2 (str): Directory containing Sentinel-2 folders that contains cloud masks.

        output_dir (str): Directory in which the validation values will be written.

        pairs (Tuple[str,str]): Tuple containing a pair of sceneids that will be evaluated.

        bands_l8 (List[str]): Landsat-8 bands that will be evaluated.

        bands_s2 (List[str]): Sentinel-2 bands that will be evaluated (LaSRC syntax).

    """

    comparison_metrics = {}

    for pair in pairs:
        name = pair[0] + '_x_' + pair[1]
        comparison_metrics[pair[0] + '_x_' + pair[1]] = {}
        # Prepare Cloud Mask

        cloud1_ds = rasterio.open(navigate.path_to_l8cloud(cloud_dir_l8, pair[0]))
        cloud2_ds = rasterio.open(navigate.path_to_s2l2a_cloud(cloud_dir_s2, pair[1]))

        cloud1_ds = validation_funcs.resample_raster(cloud1_ds, 10)
        cloud2_ds = validation_funcs.resample_raster(cloud2_ds, 10)

        cloud1_arr, cloud2_arr = validation_funcs.raster_intersection(cloud1_ds, cloud2_ds)
        mask1 = validation_funcs.mask_pixel_bitwise(cloud1_arr.astype(int), nodata=0)
        mask2 = validation_funcs.mask_pixel_scl(cloud2_arr)
        mask = numpy.logical_or(mask1, mask2)  # Combined mask

        for b in range(len(bands_l8)):
            # Load files
            print(f"Comparing pair {pair} band {bands_l8[b]}")
            raster1_path = navigate.path_to_l8srband(input_dir_l8, pair[0], bands_l8[b])
            raster2_path = navigate.path_to_s2srlasrc_band(input_dir_s2, pair[1], bands_s2[b])

            with rasterio.open(raster1_path, 'r') as raster1_ds, rasterio.open(raster2_path, 'r') as raster2_ds:
                raster1_resamp_ds = validation_funcs.resample_raster(raster1_ds, 10)
                raster2_resamp_ds = validation_funcs.resample_raster(raster2_ds, 10)

                # Get raster intersection
                raster1_arr, raster2_arr = validation_funcs.raster_intersection(raster1_resamp_ds, raster2_resamp_ds)

                # Close ds
                raster1_resamp_ds.close()
                raster2_resamp_ds.close()

                # Apply Cloud mask
                raster1_arr[mask] = numpy.nan
                raster2_arr[mask] = numpy.nan

                # Rescale
                raster1_arr = (
                        (raster1_arr * 0.275) - 2000)  # Rescale data to 0-10000 -> ((raster1_arr * 0.0000275)-0.2)

                abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr)

                # Store
                add_comparison(comparison_metrics, name, bands_l8[b], abs_dif_mean=abs_dif_mean,
                               rel_abs_perc_mean=relative_abs_perc_mean)

                # Clear Variables
                raster2_arr, raster1_arr = None, None
        cloud1_ds.close()
        cloud2_ds.close()
        cloud1_arr, cloud2_arr, mask1, mask2, mask = None, None, None, None, None

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands_l8, pairs)

    validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics_sr_l8_s2_lasrc.json'))


def validation_nbar_l8_s2_sen2cor(input_dir_l8: str, cloud_dir_l8: str, input_dir_s2: str, cloud_dir_s2: str,
                                  output_dir: str, pairs: Tuple[str, str], bands_l8: List[str],
                                  bands_s2: List[str]) -> None:
    """Performs validation on both Landsat-8 and Sentinel-2 (Sen2cor) NBAR data.

    Args:
        input_dir_l8 (str): Directory containing Landsat-8 NBAR folders.

        cloud_dir_l8 (str): Directory containing Landsat-8 folders that contains cloud masks.

        input_dir_s2 (str): Directory containing Sentinel-2 (Sen2cor) NBAR folders.

        cloud_dir_s2 (str): Directory containing Sentinel-2 folders that contains cloud masks.

        output_dir (str): Directory in which the validation values will be written.

        pairs (Tuple[str,str]): Tuple containing a pair of sceneids that will be evaluated.

        bands_l8 (List[str]): Landsat-8 bands that will be evaluated.

        bands_s2 (List[str]): Sentinel-2 bands that will be evaluated (Sen2cor syntax).

    """

    comparison_metrics = {}

    for pair in pairs:
        name = pair[0] + '_x_' + pair[1]
        comparison_metrics[pair[0] + '_x_' + pair[1]] = {}
        # Prepare Cloud Mask

        l2aname = pair[1].replace('L1C', 'L2A')
        l2aname = l2aname.replace(l2aname.split('_')[3], 'N9999')
        pattern = '_'.join(l2aname.split('_')[:-1])
        l2a_dir = [d for d in os.listdir(cloud_dir_s2) if d.startswith(pattern)][0]
        img_dir = os.path.join(cloud_dir_s2, l2a_dir, 'GRANULE',
                               os.listdir(os.path.join(cloud_dir_s2, l2a_dir, 'GRANULE'))[0], 'IMG_DATA')

        cloud2_file = pair[1].split('_')[5] + '_' + pair[1].split('_')[2] + '_SCL_20m.jp2'
        cloud2_path = os.path.join(img_dir, 'R20m', cloud2_file)

        cloud1_ds = rasterio.open(navigate.path_to_l8cloud(cloud_dir_l8, pair[0]))
        cloud2_ds = rasterio.open(cloud2_path)

        cloud1_ds = validation_funcs.resample_raster(cloud1_ds, 10)
        cloud2_ds = validation_funcs.resample_raster(cloud2_ds, 10)

        cloud1_arr, cloud2_arr = validation_funcs.raster_intersection(cloud1_ds, cloud2_ds)
        mask1 = validation_funcs.mask_pixel_bitwise(cloud1_arr.astype(int), nodata=0)
        mask2 = validation_funcs.mask_pixel_scl(cloud2_arr)
        mask = numpy.logical_or(mask1, mask2)  # Combined mask

        for b in range(len(bands_l8)):
            print(f"Comparing pair {pair} band {bands_l8[b]}")

            # Load files
            raster1_path = navigate.path_to_l8nbarband(input_dir_l8, pair[0], bands_l8[b])
            raster1_ds = rasterio.open(raster1_path)
            raster1_ds = validation_funcs.resample_raster(raster1_ds, 10)

            raster2_path, res = navigate.path_to_s2nbarsen2cor_band(input_dir_s2, pair[1], bands_s2[b])
            raster2_ds = rasterio.open(raster2_path)
            if res != 10:
                raster2_ds = validation_funcs.resample_raster(raster2_ds, 10)

            # Get raster intersection
            raster1_arr, raster2_arr = validation_funcs.raster_intersection(raster1_ds, raster2_ds)

            # Apply Cloud mask
            raster1_arr[mask] = numpy.nan
            raster2_arr[mask] = numpy.nan

            abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr)

            # Store
            add_comparison(comparison_metrics, name, bands_l8[b], abs_dif_mean=abs_dif_mean,
                           rel_abs_perc_mean=relative_abs_perc_mean)

            del raster1_ds, raster2_ds, raster1_arr, raster2_arr, abs_dif_mean, relative_abs_perc_mean
        del cloud1_ds, cloud2_ds, cloud1_arr, cloud2_arr, mask1, mask2, mask

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands_l8, pairs)

    validation_funcs.write_dict(comparison_metrics,
                                os.path.join(output_dir, 'comparison_metrics_nbar_l8_s2_sen2cor.json'))


def validation_nbar_l8_s2_lasrc(input_dir_l8: str, cloud_dir_l8: str, input_dir_s2: str, cloud_dir_s2: str,
                                output_dir: str, pairs: Tuple[str, str], bands_l8: List[str], bands_s2: List[str]):
    """Performs validation on both Landsat-8 and Sentinel-2 (LaSRC) NBAR data.

    Args:
        input_dir_l8 (str): Directory containing Landsat-8 NBAR folders.

        cloud_dir_l8 (str): Directory containing Landsat-8 folders that contains cloud masks.

        input_dir_s2 (str): Directory containing Sentinel-2 (LaSRC) NBAR folders.

        cloud_dir_s2 (str): Directory containing Sentinel-2 folders that contains cloud masks.

        output_dir (str): Directory in which the validation values will be written.

        pairs (Tuple[str,str]): Tuple containing a pair of sceneids that will be evaluated.

        bands_l8 (List[str]): Landsat-8 bands that will be evaluated.

        bands_s2 (List[str]): Sentinel-2 bands that will be evaluated (LaSRC syntax).

    """

    comparison_metrics = {}

    for pair in pairs:
        name = pair[0] + '_x_' + pair[1]
        comparison_metrics[pair[0] + '_x_' + pair[1]] = {}
        # Prepare Cloud Mask

        cloud1_ds = rasterio.open(navigate.path_to_l8cloud(cloud_dir_l8, pair[0]))
        cloud2_ds = rasterio.open(navigate.path_to_s2l2a_cloud(cloud_dir_s2, pair[1]))

        cloud1_ds = validation_funcs.resample_raster(cloud1_ds, 10)
        cloud2_ds = validation_funcs.resample_raster(cloud2_ds, 10)

        cloud1_arr, cloud2_arr = validation_funcs.raster_intersection(cloud1_ds, cloud2_ds)
        mask1 = validation_funcs.mask_pixel_bitwise(cloud1_arr.astype(int), nodata=0)
        mask2 = validation_funcs.mask_pixel_scl(cloud2_arr)
        mask = numpy.logical_or(mask1, mask2)  # Combined mask

        for b in range(len(bands_l8)):
            print(f"Comparing pair {pair} band {bands_l8[b]}")

            # Load files
            raster1_path = navigate.path_to_l8nbarband(input_dir_l8, pair[0], bands_l8[b])
            raster1_ds = rasterio.open(raster1_path)
            raster1_ds = validation_funcs.resample_raster(raster1_ds, 10)

            raster2_path = navigate.path_to_s2nbarlasrc_band(input_dir_s2, pair[1], bands_s2[b])
            raster2_ds = rasterio.open(raster2_path)

            # Get raster intersection
            raster1_arr, raster2_arr = validation_funcs.raster_intersection(raster1_ds, raster2_ds)

            # Apply Cloud mask
            raster1_arr[mask] = numpy.nan
            raster2_arr[mask] = numpy.nan

            abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr)

            # Store
            add_comparison(comparison_metrics, name, bands_l8[b], abs_dif_mean=abs_dif_mean,
                           rel_abs_perc_mean=relative_abs_perc_mean)

            del raster1_ds, raster2_ds, raster1_arr, raster2_arr, abs_dif_mean, relative_abs_perc_mean
        del cloud1_ds, cloud2_ds, cloud1_arr, cloud2_arr, mask1, mask2, mask

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands_l8, pairs)

    validation_funcs.write_dict(comparison_metrics,
                                os.path.join(output_dir, 'comparison_metrics_nbar_l8_s2_lasrc.json'))
