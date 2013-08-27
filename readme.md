
#### The current results of this code can be seen [here](https://github.com/alonisser/tiptipa/blob/master/data/all_stations.geojson)

#### How this works (so far)


The main challenge is to get the geolocations for all the Tipat Halav stations. The list of stations themselves can be scraped - or, for now, I used milkdrop.json file compiled by @SharonMoravi.

The goal is to get from [milkdrop.json](https://github.com/niryariv/tiptipa/blob/master/data/milkdrop.json) to something that looks like [stations.geojson](https://github.com/niryariv/tiptipa/blob/master/data/stations_demo.geojson).

[geoencode.py](https://github.com/niryariv/tiptipa/blob/master/geoencode.py) tries to acheive this by taking the address/city info and feeding it to [Nominatim](http://nominatim.openstreetmap.org/) - an Open Street Map project for translating addresses to geolocations.

Nominatim returns the lon/lat which are then entered into the geojson file, with the rest of the station data entered to the features dictionary of each point. 

As it turns out, some of the addresses aren't recognized by Nominatim. In that case, geoencode.py tries to get the city only without the city address. The address gets entered into a trouble_locs dict which is then written into [errors.txt](https://github.com/niryariv/tiptipa/blob/master/data/errors.txt) so it can be manually checked later.

Then geoencode.py tries the lat,lng against the [google maps api](http://maps.googleapis.com/maps/api/geocode/json?) and screen out results not in Israel. those results also are appended to [errors.txt](https://github.com/niryariv/tiptipa/blob/master/data/errors.txt).  Just found out that a side effect of the cleaning is that only "In the green line Israel" is shown, googlemaps api doesn't recognize Yehuda & Shomron. No political insult meant.

