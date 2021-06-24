import os

# 3rd party
import numpy
import rasterio

import validation_funcs
import navigate

# Local
# input_dir_l8 = '/home/marujo/Downloads/validation/l8_nbar'
# cloud_l8_dir = '/home/marujo/Downloads/validation/l8_sr'
# input_dir_s2 = '/home/marujo/Downloads/validation/s2_nbar_lasrc'
# cloud_s2_dir = '/home/marujo/Downloads/validation/s2_sr_sen2cor'
# output_dir = '/tower/git_hub/marujore/c-factor-article/validation/l8-s2-lasrc_nbar/'
# pairs = validation_funcs.search_pairs_l8_s2('/tower/git_hub/marujore/c-factor-article/input/l8-sceneids.txt', '/tower/git_hub/marujore/c-factor-article/input/s2-sceneids.txt', 1)
# pairs = [('LC08_L2SP_222081_20200723_20200910_02_T1', 'S2B_MSIL1C_20200726T133229_N0209_R081_T22JBM_20200726T152123.SAFE')]

# Datacube
input_dir_l8 = '/dados/Rennan/harmonization/work/l8_nbar/'
cloud_l8_dir = '/dados/Rennan/harmonization/work/l8_sr/'
input_dir_s2 = '/dados/Rennan/harmonization/work/s2_nbar_lasrc'
cloud_s2_dir = '/dados/Rennan/harmonization/work/s2_sr_sen2cor'
output_dir = '/dados/Rennan/harmonization/validation/l8-s2-lasrc_nbar/'
pairs = validation_funcs.search_pairs_l8_s2('/dados/Rennan/harmonization/input/l8-sceneids.txt', '/dados/Rennan/harmonization/input/s2-sceneids.txt', 5)

l8bands = ['B2',       'B3',       'B4',       'B5',       'B5',        'B6',        'B7']
s2bands = ['sr_band2', 'sr_band3', 'sr_band4', 'sr_band8', 'sr_band8a', 'sr_band11', 'sr_band12']
comparison_metrics = {}

for pair in pairs:
    comparison_metrics[pair[0]+'_x_'+pair[1]] = {}
    # Prepare Cloud Mask

    cloud1_ds = rasterio.open(navigate.path_to_l8cloud(cloud_l8_dir, pair[0]))
    cloud2_ds = rasterio.open(navigate.path_to_s2l2a_cloud(cloud_s2_dir, pair[1]))

    cloud1_ds = validation_funcs.resample_raster(cloud1_ds, 10)
    cloud2_ds = validation_funcs.resample_raster(cloud2_ds, 10)


    cloud1_arr, cloud2_arr = validation_funcs.raster_intersection(cloud1_ds, cloud2_ds)
    mask1 = validation_funcs.mask_pixel_bitwise(cloud1_arr, nodata=0)
    mask2 = validation_funcs.mask_pixel_scl(cloud2_arr)
    mask = numpy.logical_or(mask1, mask2) # Combined mask

    for b in range(len(l8bands)):
        print(f"Comparing pair {pair} band {l8bands[b]}")

        #Load files
        raster1_path = navigate.path_to_l8nbarband(input_dir_l8, pair[0], l8bands[b])
        raster1_ds = rasterio.open(raster1_path)
        raster1_ds = validation_funcs.resample_raster(raster1_ds, 10)


        raster2_path = navigate.path_to_s2nbarlasrc_band(input_dir_s2, pair[1], s2bands[b])
        raster2_ds = rasterio.open(raster2_path)

        # Get raster intersection
        raster1_arr, raster2_arr = validation_funcs.raster_intersection(raster1_ds, raster2_ds)
        raster1_arr = raster1_arr.astype(float)
        raster2_arr = raster2_arr.astype(float)

        #Apply Cloud mask
        raster1_arr[mask] = numpy.nan
        raster2_arr[mask] = numpy.nan

        raster1_arr, raster2_arr = validation_funcs.remove_negative_vals(raster1_arr, raster2_arr)

        # Compare
        abs_dif = abs(raster1_arr - raster2_arr)
        abs_dif_mean = numpy.nanmean(abs_dif)
        abs_sum = abs(raster1_arr + raster2_arr)
        relative_abs_perc = numpy.divide((2*abs_dif), abs_sum, out=numpy.zeros_like(2*abs_dif), where=abs_sum!=0)
        relative_abs_perc_mean = numpy.nanmean(relative_abs_perc)*100

        # Store
        comparison_metrics[pair[0]+'_x_'+pair[1]][l8bands[b]] = {}
        comparison_metrics[pair[0]+'_x_'+pair[1]][l8bands[b]]['abs_dif_mean'] = abs_dif_mean
        comparison_metrics[pair[0]+'_x_'+pair[1]][l8bands[b]]['relative_abs_perc_mean'] = relative_abs_perc_mean

        del raster1_ds, raster2_ds, raster1_arr, raster2_arr, abs_sum, abs_dif, abs_dif_mean, relative_abs_perc, relative_abs_perc_mean
    del cloud1_ds, cloud2_ds, cloud1_arr, cloud2_arr, mask1, mask2, mask

comparison_metrics = validation_funcs.calc_all_pairs(comparison_metrics, l8bands, pairs)

validation_funcs.write_dict(comparison_metrics, os.path.join(output_dir, 'comparison_metrics.json'))
