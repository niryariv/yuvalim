# coding=utf-8

import requests
import json
import codecs

OUTPUT_FILE = 'all_stations.geojson'
ERROR_FILE = 'errors.txt'

def locate(addr):
	payload={"q" : addr, "format": "json"} 

	r = requests.get("http://nominatim.openstreetmap.org/search", params=payload)

	print r.url
	j = r.json

	if not j:
		return False

	lon = float(j[0]['lon'])
	lat = float(j[0]['lat'])

	return [lon,lat]


def reverse_str(s):
	try:
		rev = s.split()
		rev.reverse()
		return u' '.join(rev)
	except:
		return s

json_data = open('milkdrop.json')
data = json.load(json_data, encoding="utf-8")

geojson = {"type": "FeatureCollection", "features" : []}
trouble_locs = {}

ctr = 0
for i in data:
	item = data[i]
	if item['Yeshuv'] is None: 
		continue
	# print i, item
	
	addr = item['Yeshuv'] + " " + item['Addr']
	
	loc = locate(addr)
	if loc is False:
		trouble_locs[i]="No street address data for " + addr
		loc = locate(item['Yeshuv'])
		if loc is False:
			trouble_locs[i]="No data at all"
			continue

	lon, lat = loc
	print addr, locate(addr) #.encode('utf-8').decode('unicode-escape'))

	geojson['features'].append(
		{
	      "type": "Feature",
	      "geometry": {
	        "type": "Point",
	        "coordinates": [ lon, lat ]
	      },
	      "properties": {
	        "marker-symbol": "water",
	        "שם תחנה": item['ThanaName'],
	        "כתובת": addr,
	        "ארחיות": item['Aharait']
	      }
	    }
	)
	
	ctr += 1
	# if ctr > 1: break	


f = codecs.open(OUTPUT_FILE, 'w', 'utf-8')
f.write(json.dumps(geojson, indent=4))
f.close()

f = codecs.open(ERROR_FILE, 'w', 'utf-8')
f.write(str(trouble_locs))
f.close()

	