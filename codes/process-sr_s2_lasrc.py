import os

sceneids = [] # define an empty list
with open('input/s2-sceneids.txt', 'r') as filehandle: # open file and read the content in a list
    for line in filehandle:
        currentPlace = line[:-1] # remove linebreak which is the last character of the string
        sceneids.append(currentPlace) # add item to the list

input_dir = '/dados/Rennan/harmonization/work/s2_toa'
output_dir = '/dados/Rennan/harmonization/work/s2_sr_lasrc'
aux_dir = '/tower/atmcor_aux/lasrc/L8'

for sceneid in sceneids:
    print(f'docker run --rm -v {input_dir}:/mnt/input-dir:rw -v {output_dir}:/mnt/output-dir:rw -v {aux_dir}:/mnt/lasrc-aux:ro -t lasrc {sceneid}')
