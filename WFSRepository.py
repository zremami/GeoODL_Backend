from flask import Flask
from owslib.fes import *
from datetime import datetime
import xml.dom.minidom # WFS returns GML - this library is used to parse it
import json
import pandas as pd
from IPython.display import display

def getWFSData():
    from owslib.wfs import WebFeatureService

    wfs11 = WebFeatureService(url='https://www.imis.bfs.de/ogc/opendata/ows', version='1.1.0')

    filter1 = PropertyIsGreaterThanOrEqualTo(propertyname='start_measure', literal='2022-12-01')
    #filter1 = PropertyIsBetween(propertyname='start_measure', lower='2022-11-01',upper='2022-11-02')
    filter2 = PropertyIsLike(propertyname='kenn', literal='141772901',wildCard='*')
    #filters3= PropertyIsLike(propertyname='local_authority', literal='Ulm',wildCard='*')
    filters=[filter1,filter2]

    filterxml = etree.tostring(And(operations=filters).toXML()).decode("utf-8")

    #odlinfo_timeseries_precipitation_15min
    #odlinfo_timeseries_odl_1h
    response = wfs11.getfeature(typename='odlinfo_timeseries_precipitation_15min',filter = filterxml,outputFormat='application/json',maxfeatures=900)
    # convert IO-byte to bytes
    bytesD=bytes(response.read())
    # convert to json
    data = json.loads(bytesD)
    return data   

"""for index in range(len(datanorm)):
kenn=datanorm['properties.kenn'][index], 
value=datanorm['properties.value'][index],
start_measure=datanorm['properties.start_measure'][index],
end_measure=datanorm['properties.end_measure'][index]
print(index ,':' , value,kenn,start_measure,end_measure)"""

"""for i in datanorm:
value = datanorm['properties.kenn']
print(value)"""