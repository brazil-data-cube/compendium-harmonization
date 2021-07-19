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

from cfactor.validation import navigate, validation_funcs


def validation(raster1_arr, raster2_arr):
    """
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


def add_comparison(obj, name, band, **kwargs):
    if not obj.get(name):
        obj[name] = {}
    obj[name][band]= kwargs


def validation_nbar_l8(input_dir, cloud_dir, output_dir, bands, pairs):
    """
    """

    comparison_metrics = {}

    for pair in pairs:
        name = pair[0] + '_x_' + pair[1]
        # Prepare Cloud Mask
        cloud1_ds = rasterio.open(navigate.path_to_l8cloud(cloud_dir, pair[0]))
        cloud2_ds = rasterio.open(navigate.path_to_l8cloud(cloud_dir, pair[1]))
        cloud1_arr, cloud2_arr = validation_funcs.raster_intersection(cloud1_ds, cloud2_ds)
        mask1 = validation_funcs.mask_pixel_bitwise(cloud1_arr, nodata=0)
        mask2 = validation_funcs.mask_pixel_bitwise(cloud2_arr, nodata=0)
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

            abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr, mask)

            # Store
            add_comparison(comparison_metrics, name, b, abs_dif_mean=abs_dif_mean, rel_abs_perc_mean=relative_abs_perc_mean)

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands, pairs)
    validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics.json'))


def validation_nbar_s2_sen2cor(input_dir: str, cloud_dir, output_dir, pairs, bands10m, bands20m):
    """"""

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

            abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr, mask)

            # Store
            add_comparison(comparison_metrics, name, b, abs_dif_mean=abs_dif_mean, rel_abs_perc_mean=relative_abs_perc_mean)

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands, pairs)

    validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics.json'))


def validation_nbar_s2_lasrc(input_dir, cloud_dir, output_dir, pairs, bands):
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

            abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr, mask)

            # Store
            add_comparison(comparison_metrics, name, b, abs_dif_mean=abs_dif_mean, rel_abs_perc_mean=relative_abs_perc_mean)

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands, pairs)

    validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics.json'))


def validation_sr_l8_s2_sen2cor(input_dir_l8, cloud_dir_l8, input_dir_s2, cloud_dir_s2, output_dir, pairs, bands_l8,
                                bands_s2):
    """"""

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
        mask1 = validation_funcs.mask_pixel_bitwise(cloud1_arr, nodata=0)
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

            abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr, mask)

            # Store
            add_comparison(comparison_metrics, name, bands_l8[b], abs_dif_mean=abs_dif_mean, rel_abs_perc_mean=relative_abs_perc_mean)

            del raster1_ds, raster2_ds, raster1_arr, raster2_arr, abs_dif_mean, relative_abs_perc_mean
        del cloud1_ds, cloud2_ds, cloud1_arr, cloud2_arr, mask1, mask2, mask

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands_l8, pairs)
    validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics.json'))


def validation_sr_l8_s2_lasrc(input_dir_l8, cloud_dir_l8, input_dir_s2, cloud_dir_s2, output_dir, pairs, bands_l8,
                              bands_s2):
    """"""

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
        mask1 = validation_funcs.mask_pixel_bitwise(cloud1_arr, nodata=0)
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
                        (raster1_arr * 0.275) - 2000) # Rescale data to 0-10000 -> ((raster1_arr * 0.0000275)-0.2)

                abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr, mask)

                # Store
                add_comparison(comparison_metrics, name, bands_l8[b], abs_dif_mean=abs_dif_mean, rel_abs_perc_mean=relative_abs_perc_mean)

                # Clear Variables
                raster2_arr, raster1_arr = None, None
        cloud1_ds.close()
        cloud2_ds.close()
        cloud1_arr, cloud2_arr, mask1, mask2, mask = None, None, None, None, None

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands_l8, pairs)

    validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics.json'))


def validation_nbar_l8_s2_sen2cor(input_dir_l8, cloud_dir_l8, input_dir_s2, cloud_dir_s2, output_dir, pairs, bands_l8,
                                  bands_s2):
    """"""

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
        mask1 = validation_funcs.mask_pixel_bitwise(cloud1_arr, nodata=0)
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

            abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr, mask)

            # Store
            add_comparison(comparison_metrics, name, bands_l8[b], abs_dif_mean=abs_dif_mean, rel_abs_perc_mean=relative_abs_perc_mean)

            del raster1_ds, raster2_ds, raster1_arr, raster2_arr, abs_dif_mean, relative_abs_perc_mean
        del cloud1_ds, cloud2_ds, cloud1_arr, cloud2_arr, mask1, mask2, mask

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands_l8, pairs)

    validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics.json'))


def validation_nbar_l8_s2_lasrc(input_dir_l8, cloud_dir_l8, input_dir_s2, cloud_dir_s2, output_dir, pairs, bands_l8,
                                bands_s2):
    """"""

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
        mask1 = validation_funcs.mask_pixel_bitwise(cloud1_arr, nodata=0)
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

            abs_dif_mean, relative_abs_perc_mean = validation(raster1_arr, raster2_arr, mask)

            # Store
            add_comparison(comparison_metrics, name, bands_l8[b], abs_dif_mean=abs_dif_mean, rel_abs_perc_mean=relative_abs_perc_mean)

            del raster1_ds, raster2_ds, raster1_arr, raster2_arr, abs_dif_mean, relative_abs_perc_mean
        del cloud1_ds, cloud2_ds, cloud1_arr, cloud2_arr, mask1, mask2, mask

    comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands_l8, pairs)

    validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics.json'))
