#!/user/bin/python
# -*- coding = utf-8 -*-

import csv
import json
from geoencode import OUTPUT_FILENAME

input_file = "".join([OUTPUT_FILENAME,".geojson"])

with open(input_file) as file:

    data = json.loads(file.read())['features']
    
with open('data/milk.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile )
    writer.writerow(['name', 'address', 'lat', 'lon', 'phone','error', 'operator'])
    for row in data:
        writer.writerow(
            [row['properties']['name'].encode('utf-8'),
             row['properties']['address'].encode('utf-8'),
             row['geometry']['coordinates'][1],
             row['geometry']['coordinates'][0],
             row['properties']['phone'],
             row['properties']['error'],
             row['properties']['operator'].encode('utf-8'),])

