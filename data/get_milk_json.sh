
if [ -e milk.geojson ]
then
	echo "milk.geojson found, now removing old copy and updating"
	rm milk.geojson
fi

echo "downloading milk.geojson"

curl -o milk.geojson https://raw.github.com/segalle/milkscrapper/master/src/milk.geojson 

