from flask import Flask
from datetime import datetime
from owslib.wfs import WebFeatureService
from owslib.fes import *
import xml.dom.minidom # WFS returns GML - this library is used to parse it
import json

wfs11 = WebFeatureService(url='https://www.imis.bfs.de/ogc/opendata/ows', version='1.1.0')
wTitle= wfs11.identification.title

filter1= PropertyIsLike(propertyname='kenn', literal='096781381',wildCard='*')
filter2 = PropertyIsGreaterThanOrEqualTo(propertyname='end_measure', literal='2022-10-31')
filters=[filter1,filter2]

filterxml = etree.tostring(And(operations=filters).toXML()).decode("utf-8")

response = wfs11.getfeature(typename='opendata:odlinfo_timeseries_precipitation_15min',filter=filterxml,bbox=(7.800293,47.709762,13.579102,54.033586), srsname='EPSG:4326', maxfeatures=100,outputFormat='application/json')
bytesD=bytes(response.read())
# convert to json
data = json.loads(bytesD)