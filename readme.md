#### This code powers [tipa.li](http://tipa.li/), a simple mobile-friendly site for location Polio vaccination clinics in Israel ([background](http://niryariv.wordpress.com/2013/09/03/tipa-li-a-tool-for-easily-finding-polio-vaccination-clinics/))

### Frontend

The front end consists of index.html, hosted on GitHub pages

### Data

Data is kept in geoJSON format in data/clinics.js and read by index.html. 

### Scraping & Geoencodign

Geoencoding was done by geoencode.py, running against all_stations.json. Currently geoencode.py isn't used, instead we're using data from the [Milkscrapper project](https://github.com/segalle/milkscrapper) stored in data/milkscrapper.geojson

### Editing

Data from milkscrapper.geojson is exported to a [Google Fusion table](https://www.google.com/fusiontables/DataSource?docid=1zpsJz8BGY5uSWbQC6CLgXQka1vhHyHqtrUMHas8) to be proofread and edited by volunteers. 

Occasionally, the data in the Fusion table is imported back via the import_fusion.py script via:
```python import_fusion.py -f clinics.js```

### Contributing

**YOU can help!:** Help us verify, clean and optimize the information. 

We use a google fusion [table](https://www.google.com/fusiontables/DataSource?docid=1zpsJz8BGY5uSWbQC6CLgXQka1vhHyHqtrUMHas8) with the data.
ping us in the issues section or by email to grant an editing permission.
