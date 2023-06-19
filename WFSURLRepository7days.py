# This class is created to access to WFS data of odl and precipiation
import datetime
import json
import pandas as pd
import webbrowser
from urllib.request import urlopen

# get wfs data odl with locality code start and end date measurement filters
def getOdl_1h(locality_code,start,end):

    url = "https://entw-imis.lab.bfs.de/ogc/opendata/wfs?typeName=opendata:public_odl_brutto_1h&_dc=1665655122146&service=WFS&version=1.1.0&request=GetFeature&outputFormat=application%2Fjson&srsname=EPSG%3A3857&cql_filter=id%20%3D%20%27"+locality_code+"%27%20AND%20end_measure%3E%27"+start+"T00%3A00%3A00.000Z%27%20AND%20end_measure%3C%27"+end+"T11%3A59%3A00.000Z%27"
        
    response = urlopen(url)       
    data_json = json.loads(response.read())
    
    return data_json

# get wfs data precipitation with locality code start and end date measurement filters
def getPrecipitation_15min(locality_code,start,end):

    url = "https://entw-imis.lab.bfs.de/ogc/opendata/wfs?typeName=opendata:public_precipitation_15min&_dc=1665655122146&service=WFS&version=1.1.0&request=GetFeature&outputFormat=application%2Fjson&srsname=EPSG%3A3857&cql_filter=id%20%3D%20%27"+locality_code+"%27%20AND%20end_measure%3E%27"+start+"T00%3A00%3A00.000Z%27%20AND%20end_measure%3C%27"+end+"T11%3A59%3A00.000Z%27"
        
    response = urlopen(url)       
    data_json = json.loads(response.read())
    
    return data_json