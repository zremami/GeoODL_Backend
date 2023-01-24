from flask import Flask
from owslib.fes import *
import datetime
import xml.dom.minidom # WFS returns GML - this library is used to parse it
import json
import pandas as pd
from IPython.display import display
from owslib.wfs import WebFeatureService
import webbrowser



#https://www.imis.bfs.de/ogc/opendata/ows
#https://entw-imis.lab.bfs.de/ogc/opendata/wfs
wfs11 = WebFeatureService(url='https://www.imis.bfs.de/ogc/opendata/ows', version='1.1.0')

def getOdl_1h(locality_code):
    
    filter = PropertyIsLike(propertyname='id', literal=locality_code,wildCard='*')

    filterxml = etree.tostring(filter.toXML()).decode("utf-8")

    #odlinfo_timeseries_precipitation_15min

    response = wfs11.getfeature(typename='odlinfo_timeseries_odl_1h',filter = filterxml,outputFormat='application/json')
 
    # convert IO-byte to bytes
    bytesD=bytes(response.read())
    # convert to json
    data = json.loads(bytesD)
    return data

def getPrecipitation_15min(locality_code):

    filter = PropertyIsLike(propertyname='id', literal=locality_code,wildCard='*')
    #filters3= PropertyIsLike(propertyname='local_authority', literal='Ulm',wildCard='*')

    filterxml = etree.tostring(filter.toXML()).decode("utf-8")

    response = wfs11.getfeature(typename='odlinfo_timeseries_precipitation_15min',filter = filterxml,outputFormat='application/json')
    # convert IO-byte to bytes
    bytesD=bytes(response.read())
    # convert to json
    data = json.loads(bytesD)
    return data