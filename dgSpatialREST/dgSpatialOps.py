import sys, os
import geopandas as gpd
import geojsonio
import json

from flask import Flask, request, Response
app = Flask(__name__)

#geoJSON test file
statesGeoJSON = r'/Users/regandwyer/dev/eclipseWS/dg_App/StatesGeoJSON.txt'
#########################################################################################
##when reading geoJSON from a file - gpd.read_file() method automagically returns a gdf (fionna package)
##generating gdf (for spatial overlay set ops) from response data is trickier - need from_features() method
#file_data1 = r'/Users/regandwyer/dev/eclipseWS/dg_App/obj1.txt' 
#file_data2 = r'/Users/regandwyer/dev/eclipseWS/dg_App/obj2.txt'

#unicode handling - unicode comes back in Flask response
#probably a better way to do this, some formatting/encoding property?
def processing_hook(pairs):
    new_pairs = []
    for key, value in pairs:
        if isinstance(value, unicode):
            value = value.encode('utf-8')         
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        new_pairs.append((key, value))
    return dict(new_pairs)

@app.route('/')
def simpleSpatialHome():
    gdf_states = gpd.read_file(statesGeoJSON).to_json()
    geojsonio.display(gdf_states)
    return 'display States geoJSON file'

@app.route('/ops/<op_type>', methods = ['POST'])
def simpleSpatialOps(op_type):
    respValues = {}
    req_data = request.get_json() #this is type 'dict'  
    #need string obj for loads, use dumps() to create a JSON formatted string
    strObj_rdata = json.dumps(req_data)
    #need dict to collect separate features, and remove unicode
    fDict = json.loads(strObj_rdata, object_pairs_hook=processing_hook)
    feature1 = (fDict["poly1"])
    feature2 = (fDict["poly2"])
    #GeoDataFrame.from_features() accepts dict
    gdf_F1 = gpd.GeoDataFrame.from_features(feature1)
    gdf_F2 = gpd.GeoDataFrame.from_features(feature2)   
    if op_type=='union':
        respValues["operation"] = op_type
        unionGDF = gpd.overlay(gdf_F1 , gdf_F2, how='union')
        displayResult = unionGDF.to_json()
        respValues["geoJSON"] = displayResult
        geojsonio.display(displayResult)
        #return op_type + "\n" + str(displayResult) 
    elif op_type=='intersection':
        respValues["operation"] = op_type
        intersectGDF = gpd.overlay(gdf_F1, gdf_F2, how='intersection')
        displayResult = intersectGDF.to_json()
        geojsonio.display(displayResult)
        respValues["geoJSON"] = displayResult
        #return op_type + "\n" + str(displayResult)
    else:
        return "operation not specified"
    responseJSON = json.dumps(respValues)
    ##TODO - this is a string object which isn't JSON format
    ##can successfully return as op_type + "\n" + str(displayResult) and have valid JSON 
        ####but wanted to have it coming back in valid JSON in Response object 
    resp = Response(responseJSON, status=200, mimetype='application/json')
    return resp    
    
if __name__ == '__main__':
    app.run()
######################
