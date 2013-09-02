#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import json
OUTPUT_FILENAME = "data/milk"

input_file = "".join([OUTPUT_FILENAME,".geojson"])

if __name__ == "__main__":
    with open(input_file) as file:
    
        data = json.loads(file.read())['features']
        
    with open('data/milk.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile )
        writer.writerow(['name', 'city', 'district','subdistrict','address', 'lat', 'lon', 'phone','Sunday','Monday','Tuesday','Wednesady','Thursday','Friday','Saturday','notes','owner'])
        for row in data:
            prop = row['properties']
            row_to_write =[
                 prop['name'].encode('utf-8'),
                 prop['city'].encode('utf-8'),
                 prop['district'].encode('utf-8'),
                 prop['subdistrict'].encode('utf-8'),
                 prop['address'].encode('utf-8'),
                 row['geometry']['coordinates'][1],
                 row['geometry']['coordinates'][0],
                 prop['phones']]
            try:
                for day in prop['days']:
                    row_to_write.append(day.encode('utf-8'))
                if len(prop['days']) < 7:
                        for day in range(7 -len(prop['days'])):
                            row_to_write.append(u'סגור'.encode('utf-8'))
            except IndexError:
                pass
            row_to_write.extend([prop['notes'].encode('utf-8'),
                 prop['owner'].encode('utf-8'),])
            if prop.has_key('error'):
                e = prop['error']
            else:
                e = 'false'
            row_to_write.append(e)
            writer.writerow(row_to_write)
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            print(now)
            subprocess.call(['git','commit','data/milk.csv','-m','commiting csv file to upload to fusion %s' % now])        
