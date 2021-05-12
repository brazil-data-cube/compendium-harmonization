sceneids = [] # define an empty list
with open('input/l8-sceneids.txt', 'r') as filehandle: # open file and read the content in a list
    for line in filehandle:
        currentPlace = line[:-1] # remove linebreak which is the last character of the string
        sceneids.append(currentPlace) # add item to the list

base_dir = '/dados/Rennan/harmonization/south/l8'

for sceneid in sceneids:
    # print(sceneid)
    print(f'docker run --rm -v {base_dir}:/mnt/input-dir:rw l8angs {sceneid}')