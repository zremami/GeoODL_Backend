from flask import Flask
from owslib.fes import *
import datetime
import xml.dom.minidom # WFS returns GML - this library is used to parse it
import json
import pandas as pd
from IPython.display import display
from owslib.wfs import WebFeatureService
import webbrowser
from urllib.request import urlopen


def getOdl_1h(locality_code):

    
    url = "https://www.imis.bfs.de/ogc/opendata/wfs?typeName=opendata:odlinfo_timeseries_odl_1h&_dc=1665655122146&service=WFS&version=1.1.0&request=GetFeature&outputFormat=application%2Fjson&srsname=EPSG%3A3857&cql_filter=id%20%3D%20%27"+locality_code+"%27%20"
        
    # store the response of URL
    response = urlopen(url)       
    # storing the JSON response 
    # from url in data
    data_json = json.loads(response.read())
    
    return data_json

def getPrecipitation_15min(locality_code):

    url = "https://www.imis.bfs.de/ogc/opendata/wfs?typeName=opendata:odlinfo_timeseries_precipitation_15min&_dc=1665655122146&service=WFS&version=1.1.0&request=GetFeature&outputFormat=application%2Fjson&srsname=EPSG%3A3857&cql_filter=id%20%3D%20%27"+locality_code+"%27%20"
        
    # store the response of URL
    response = urlopen(url)       
    # storing the JSON response 
    # from url in data
    data_json = json.loads(response.read())
    
    return data_json