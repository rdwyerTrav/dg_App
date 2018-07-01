# Simple Spatial Ops REST app with flask
used python 2.7  
dependencies - installed these python mods in a virtual env  
	flask  
	pandas  
	geopandas  
	geojsonio  

## Input
used geojson.io online to generate 2 geoJSON polys  
combined those into one JSON structure and used Postman to submit as HTTP POST  
example of this JSON is 2obinput.txt  
format is:  
	{ "poly1" : {geoJSON}, "poly2" : {geoJSON} }  
home page assumes the States geoJSON txt file - please stage and point to it  
	
## Running
```
python /<path to dgSpatialOps.py file>/dgSpatialOps.py
```
home is local host  
choosing operation is via URL  
<localhost>/ops/union  
<localhost>/ops/intersection  

## Testing
```
python /<path to dgSpatialOps.py file>/dgSOtests.py
```