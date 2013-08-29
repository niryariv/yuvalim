#!/user/bin/python
# -*- coding = utf-8 -*-

import requests
import json
import codecs

OUTPUT_FILENAME = 'data/all_stations'


with open('data/milkdrop.json') as json_data:
    data = json.load(json_data, encoding="utf-8")

geojson = {"type": "FeatureCollection", "features": []}


def locate_with_google(addr):
    """
    Gets address and returns lat,lon location vs googleapis geocode
    """

    payload = {"address": addr, "sensor": "true"}

    r = requests.get("http://maps.googleapis.com/maps/api/geocode/json", params=payload)

    print r.url
    print r.text
    j = r.json()

    if j['status'] != 'OK':
        print "bad status"
        return False

    res = j['results'][0]
    country = res['address_components'].pop()
    country_options = ["Israel", "israel", "Palestine", "palestine", "Palestinian Authority", "Palestinian National Authority"]

    # turns out that places like Kiryat Arba just don't have a country address (ie neither Israel/Palestine)
    # so if the location doesn't have a country assume it's in the west bank
    if 'country' in country['types'] and country['long_name'] not in country_options:
        return False

    return res['geometry']['location']


if __name__ == "__main__":

# here we go

    ctr = 0
    for i in data:
        item = data[i]

        if item['Yeshuv'] is None:
            continue

        addr = item['Yeshuv'] + " " + item['Addr']

        loc = locate_with_google(addr)
        print addr, loc

        error = not loc

        if loc is False:
            loc = {'lng': 0, 'lat': 0}

        geojson['features'].append(
            {
              "type": "Feature",
              "geometry": {
                "type": "Point",
                "coordinates": [ loc['lng'], loc['lat'] ]
              },
              "properties": {
                "item_id": i,
                "name": item['ThanaName'],
                "address": unicode(addr),
                "operator": item['Aharait'],
                "phone" : item['tel1'],
                "error" : error
              }
            }
        )

        ctr += 1
        # if ctr > 1: break

    output = json.dumps(geojson, indent=4, ensure_ascii=False)

    # clean geoJSON
    f = codecs.open(OUTPUT_FILENAME + '.geojson', 'wb', 'utf-8')
    f.write(output)
    f.close()


    # make it JS so it can be included in index.html
    output = "var stations=" + output
    f = codecs.open(OUTPUT_FILENAME + '.js', 'wb', 'utf-8')
    f.write(output)
    f.close()

