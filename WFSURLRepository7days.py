from flask import Flask
from owslib.fes import *
import datetime
import xml.dom.minidom # WFS returns GML - this library is used to parse it
import json
import pandas as pd
from IPython.display import display
import webbrowser
from urllib.request import urlopen

def getOdl_1h(locality_code,start,end):

    #url = "https://entw-imis.lab.bfs.de/ogc/opendata/wfs?typeName="+typeName1+"&_dc=1665655122146&service=WFS&version=1.1.0&request=GetFeature&outputFormat=application%2Fjson&srsname=EPSG%3A3857&cql_filter=id%20%3D%20%27"+locality_code+"%27%20AND%20end_measure%3E%272023-02-25T00%3A00%3A00.000Z%27%20AND%20end_measure%3C%272023-03-03T00%3A00%3A00.000Z%27"
    url = "https://entw-imis.lab.bfs.de/ogc/opendata/wfs?typeName=opendata:public_odl_brutto_1h&_dc=1665655122146&service=WFS&version=1.1.0&request=GetFeature&outputFormat=application%2Fjson&srsname=EPSG%3A3857&cql_filter=id%20%3D%20%27"+locality_code+"%27%20AND%20end_measure%3E%27"+start+"T00%3A00%3A00.000Z%27%20AND%20end_measure%3C%27"+end+"T00%3A00%3A00.000Z%27"
        
    # store the response of URL
    response = urlopen(url)       
    # storing the JSON response 
    # from url in data
    data_json = json.loads(response.read())
    
    return data_json

def getPrecipitation_15min(locality_code,start,end):

    url = "https://entw-imis.lab.bfs.de/ogc/opendata/wfs?typeName=opendata:public_precipitation_15min&_dc=1665655122146&service=WFS&version=1.1.0&request=GetFeature&outputFormat=application%2Fjson&srsname=EPSG%3A3857&cql_filter=id%20%3D%20%27"+locality_code+"%27%20AND%20end_measure%3E%27"+start+"T00%3A00%3A00.000Z%27%20AND%20end_measure%3C%27"+end+"T00%3A00%3A00.000Z%27"
        
    # store the response of URL
    response = urlopen(url)       
    # storing the JSON response 
    # from url in data
    data_json = json.loads(response.read())
    
    return data_json