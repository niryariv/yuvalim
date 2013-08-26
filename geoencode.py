# coding=utf-8

import requests
import json
import codecs

def locate(addr):
	# url = "http://nominatim.openstreetmap.org/search?" + urllib.urlencode({"q" : addr.encode('utf8'), "format": "json"})
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
		trouble_locs[addr]="No street address data"
		loc = locate(item['Yeshuv'])
		if loc is False:
			trouble_locs[addr]="No data at all"
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
	if ctr > 1: 
		break	


f = codecs.open('all_stations.geojson', 'w', 'utf-8')
f.write(json.dumps(geojson, indent=4))
f.close()

	