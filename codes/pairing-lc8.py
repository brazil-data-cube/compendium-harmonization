from datetime import datetime
from operator import itemgetter

sceneids = [] # define an empty list
with open('input/l8-sceneids.txt', 'r') as filehandle: # open file and read the content in a list
    for line in filehandle:
        currentPlace = line[:-1] # remove linebreak which is the last character of the string
        sceneids.append(currentPlace) # add item to the list

l8_sceneids = []
for sceneid in sceneids:
    splited_sceneid = sceneid.split('_')
    sensing_date = datetime.strptime(splited_sceneid[3], '%Y%m%d')
    orbit = int(splited_sceneid[2])
    l8_sceneids.append([sceneid, sensing_date, orbit])

# Order by sensing_date
l8_sceneids = sorted(l8_sceneids, key=itemgetter(1))

day_diff = 10
pairs = []
uniques = set()
for i in range(0, len(l8_sceneids)-1):
    # Select with day difference
    if abs((l8_sceneids[i][1] - l8_sceneids[i+1][1]).days) < day_diff:
        # Select from other orbit
        if l8_sceneids[i][2] != l8_sceneids[i+1][2]:
            pairs.append((l8_sceneids[i][0], l8_sceneids[i+1][0]))
            uniques.add(l8_sceneids[i][0])
            uniques.add(l8_sceneids[i+1][0])

print(f'Total pairs: {len(pairs)}')
print(f'Total uniques: {len(uniques)}')

for pair in pairs:
    print(pair)
# for unique in uniques:
#     print(unique)
