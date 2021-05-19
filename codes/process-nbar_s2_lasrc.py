sceneids = [] # define an empty list
with open('input/s2-sceneids.txt', 'r') as filehandle: # open file and read the content in a list
    for line in filehandle:
        currentPlace = line[:-1] # remove linebreak which is the last character of the string
        sceneids.append(currentPlace) # add item to the list

input_dir = '/dados/Rennan/harmonization/work/s2_sr_lasrc'
output_dir = '/dados/Rennan/harmonization/work/s2_nbar_lasrc'

sceneids = ["S2B_MSIL1C_20180418T133219_N0206_R081_T22JBM_20180418T150306.SAFE","S2A_MSIL1C_20180403T133221_N0206_R081_T22JBM_20180403T183251.SAFE","S2B_MSIL1C_20200417T133219_N0209_R081_T22JBM_20200417T164717.SAFE","S2A_MSIL1C_20191204T133221_N0208_R081_T22JBM_20191204T150916.SAFE","S2B_MSIL1C_20200410T134209_N0209_R124_T22JBM_20200410T165935.SAFE","S2A_MSIL1C_20180406T134211_N0206_R124_T22JBM_20180406T152102.SAFE","S2A_MSIL1C_20190408T133231_N0207_R081_T22JBM_20190408T151102.SAFE","S2A_MSIL1C_20180304T133221_N0206_R081_T22JBM_20180304T151552.SAFE","S2B_MSIL1C_20200420T134209_N0209_R124_T22JBM_20200420T165908.SAFE","S2A_MSIL1C_20190411T134211_N0207_R124_T22JBM_20190411T165738.SAFE","S2A_MSIL1C_20200422T133231_N0209_R081_T22JBM_20200422T195221.SAFE","S2B_MSIL1C_20181104T133219_N0206_R081_T22JBM_20181104T151242.SAFE","S2B_MSIL1C_20200430T134209_N0209_R124_T22JBM_20200430T165419.SAFE","S2A_MSIL1C_20200425T134211_N0209_R124_T22JBM_20200425T152459.SAFE","S2B_MSIL1C_20200407T133219_N0209_R081_T22JBM_20200407T150234.SAFE","S2B_MSIL1C_20180408T133219_N0206_R081_T22JBM_20180408T151430.SAFE","S2A_MSIL1C_20200412T133221_N0209_R081_T22JBM_20200412T151311.SAFE","S2B_MSIL1C_20181204T133219_N0207_R081_T22JBM_20181204T150957.SAFE","S2A_MSIL1C_20180416T134211_N0206_R124_T22JBM_20180416T165957.SAFE","S2A_MSIL1C_20200405T134211_N0209_R124_T22JBM_20200405T152340.SAFE","S2B_MSIL1C_20190804T134219_N0208_R124_T22JBM_20190804T165447.SAFE","S2A_MSIL1C_20200415T134211_N0209_R124_T22JBM_20200415T165901.SAFE"]
for sceneid in sceneids:
    print(f'docker run --rm -v {input_dir}:/mnt/input-dir:rw -v {output_dir}:/mnt/output-dir nbar {sceneid[:-5]}')
