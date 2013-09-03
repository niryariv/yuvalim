#!/usr/bin/python
import json
import requests
import sys
import codecs
import subprocess
from datetime import datetime
from optparse import OptionParser


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-f", dest="output_file", help="output filename (will be stored under the data/ directory)")

    (options, args) = parser.parse_args()

    if not options.output_file:
        print "must include -f <output filename>"
        exit()

    OUTPUT_PATH = 'data/' + options.output_file


    with open("api.json") as f:
        keys = json.loads(f.read())

    server_key = keys["ServerKey"]
    tablename = keys['fusion_table']
    endpoint = 'https://www.googleapis.com/fusiontables/v1/query?sql=SELECT * FROM '
    apicall = "".join([endpoint, tablename, "&key=", server_key])
    
    raw = requests.get(apicall)
    if not raw.ok:
        print("something wrong with the apicall\n would print the requests object for inspection and debugging:")
        print('dir:',dir(raw))
        print('status code:',raw.status_code)
        print('text:', raw.text)
        sys.exit()

    data = raw.json()
    
    geojson = {"type": "FeatureCollection", "features": []}
    for place in data['rows']:
        geojson['features'].append(
                    {
                      "geometry": {
                        "type": "Point",
                        "coordinates": [
                            place[6],
                            place[5]
                            ]
                      },
                      "type": "Feature",
                      "properties": {
                        "city": place[1],
                        "name": place[0],
                        "district":place[2],
                        "subdistrict":place[3],
                        "address":place[4],
                        "operator": place[16],
                        "days": [
                            place[8],
                            place[9],
                            place[10],
                            place[11],
                            place[12],
                            place[13]
                            ],
                        "phones" : place[7],
                        "notes": place[15],
                        "error" : place[17]
                      }
                    }
                )
    
    with codecs.open(OUTPUT_PATH,'wb+', 'utf-8') as f:
        output = "stations=" + json.dumps(geojson, indent=4, ensure_ascii=False)
        f.write(output)
        f.close()

    subprocess.call(['git', 'add', OUTPUT_PATH])
    subprocess.call(['git','commit', OUTPUT_PATH, '-m', 'commiting updated geojson from Fusion table %s' % datetime.now().strftime("%d/%m/%Y %H:%M")])
