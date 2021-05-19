import os
import re
from pathlib import Path

# 3rd party
import numpy
import rasterio


import validation_funcs
import navigate

# local
# input_dir = '/home/marujo/Downloads/validation/s2_nbar_sen2cor'
# cloud_s2_dir = '/home/marujo/Downloads/validation/s2_sr_sen2cor'
# output_dir = '/tower/git_hub/marujore/c-factor-article/validation/s2_nbar_sen2cor/'
# pairs = validation_funcs.search_pairs_s2('/tower/git_hub/marujore/c-factor-article/input/s2-sceneids.txt')
# pairs = [("S2A_MSIL1C_20200803T134221_N0209_R124_T22JBM_20200803T152907.SAFE", "S2B_MSIL1C_20200805T133229_N0209_R081_T22JBM_20200805T151504.SAFE")]

# datacube
input_dir = '/dados/Rennan/harmonization/work/s2_nbar_sen2cor/'
cloud_s2_dir = '/dados/Rennan/harmonization/work/s2_sr_sen2cor/'
output_dir = '/dados/Rennan/harmonization/validation/s2_nbar_sen2cor/'
pairs = validation_funcs.search_pairs_s2('/dados/Rennan/harmonization/input/s2-sceneids.txt')


bands10m = ['B02', 'B03', 'B04', 'B08']
bands20m = ['B8A', 'B11', 'B12']
bands = bands10m+bands20m
comparison_metrics = {}

for pair in pairs:
    comparison_metrics[pair[0]+'_x_'+pair[1]] = {}
    # Prepare Cloud Mask
    cloud1_path = navigate.path_to_s2l2a_cloud(cloud_s2_dir, pair[0])
    cloud2_path = navigate.path_to_s2l2a_cloud(cloud_s2_dir, pair[1])

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
        mask = numpy.logical_or(mask1, mask2) # Combined mask

        #Load files
        raster1_ds = rasterio.open(navigate.path_to_s2nbarsen2cor_band(input_dir, pair[0], b)[0])
        raster2_ds = rasterio.open(navigate.path_to_s2nbarsen2cor_band(input_dir, pair[1], b)[0])

        # Get raster intersection
        raster1_arr, raster2_arr = validation_funcs.raster_intersection(raster1_ds, raster2_ds)
        raster1_arr = raster1_arr.astype(float)
        raster2_arr = raster2_arr.astype(float)

        #Apply Cloud mask
        raster1_arr[mask] = numpy.nan
        raster2_arr[mask] = numpy.nan

        # Compare
        abs_dif = abs(raster1_arr - raster2_arr)
        abs_dif_mean = numpy.nanmean(abs_dif)
        abs_sum = abs(raster1_arr + raster2_arr)
        relative_abs_perc = numpy.divide((2*abs_dif), abs_sum, out=numpy.zeros_like(2*abs_dif), where=abs_sum!=0)
        relative_abs_perc_mean = numpy.nanmean(relative_abs_perc)*100

        # Store
        comparison_metrics[pair[0]+'_x_'+pair[1]][b] = {}
        comparison_metrics[pair[0]+'_x_'+pair[1]][b]['abs_dif_mean'] = abs_dif_mean
        comparison_metrics[pair[0]+'_x_'+pair[1]][b]['relative_abs_perc_mean'] = relative_abs_perc_mean

comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, bands, pairs)

validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics.json'))
