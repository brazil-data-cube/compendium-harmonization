import os
import shutil
from pathlib import Path

sceneids = [] # define an empty list
with open('input/s2-sceneids.txt', 'r') as filehandle: # open file and read the content in a list
    for line in filehandle:
        currentPlace = line[:-1] # remove linebreak which is the last character of the string
        sceneids.append(currentPlace) # add item to the list

input_dir = '/dados/Rennan/harmonization/work/s2_toa'
output_dir = '/dados/Rennan/harmonization/work/s2_sr_lasrc'

for sceneid in sceneids:
    print(sceneid)
    p_in = Path(Path(input_dir).joinpath(sceneid).joinpath('GRANULE'))
    p_in = p_in.joinpath(os.listdir(str(p_in))[0]).joinpath('ANG_DATA')
    p_out = Path(output_dir).joinpath(sceneid.replace('.SAFE','')).joinpath('ANG_DATA')
    shutil.copytree(str(p_in), str(p_out))
