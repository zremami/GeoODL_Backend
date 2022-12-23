from flask import Flask
from owslib.fes import *
from datetime import datetime
import xml.dom.minidom # WFS returns GML - this library is used to parse it
import json
import pandas as pd
from IPython.display import display
from owslib.wfs import WebFeatureService

#https://www.imis.bfs.de/ogc/opendata/ows
#https://entw-imis.lab.bfs.de/ogc/opendata/wfs
wfs11 = WebFeatureService(url='https://entw-imis.lab.bfs.de/ogc/opendata/wfs', version='1.1.0')
currdate = datetime.date.today()-datetime.timedelta(1)

def getOdl_1h():
    #filter1 = PropertyIsGreaterThanOrEqualTo(propertyname='start', literal='2022-01-01')
    filter1 = PropertyIsBetween(propertyname='start', lower='2022-01-01' ,upper= currdate)
    #filter1 = PropertyIsBetween(propertyname='start_measure', lower='2022-11-01',upper='2022-11-02')
    filter2 = PropertyIsLike(propertyname='id', literal='DEZ0402',wildCard='*')
    #filter3 = PropertyIsLike(propertyname='network', literal='BfS',wildCard='*')
    #filters3= PropertyIsLike(propertyname='local_authority', literal='Ulm',wildCard='*')
    filters=[filter1,filter2]

    filterxml = etree.tostring(And(operations=filters).toXML()).decode("utf-8")

    #odlinfo_timeseries_precipitation_15min
    #odlinfo_timeseries_odl_1h
    #opendata:public_odl_brutto_1h
    #opendata:odl_brutto_1h
    response = wfs11.getfeature(typename='opendata:public_odl_brutto_1h',filter = filterxml,outputFormat='application/json')
    # convert IO-byte to bytes
    bytesD=bytes(response.read())
    # convert to json
    data1 = json.loads(bytesD)
    return data1

def getPrecipitation_15min():

    #filter1 = PropertyIsGreaterThanOrEqualTo(propertyname='start_measure', literal='2022-01-01')
    filter1 = PropertyIsBetween(propertyname='start_measure', lower='2022-01-01', upper='2022.12.23 07:00:00')
    #filter1 = PropertyIsBetween(propertyname='start_measure', lower='2022-11-01',upper='2022-11-02')
    filter2 = PropertyIsLike(propertyname='id', literal='DEZ0402',wildCard='*')
    #filters3= PropertyIsLike(propertyname='local_authority', literal='Ulm',wildCard='*')
    filters=[filter1,filter2]

    filterxml = etree.tostring(And(operations=filters).toXML()).decode("utf-8")

    #odlinfo_timeseries_precipitation_15min
    #odlinfo_timeseries_odl_1h
    response = wfs11.getfeature(typename='opendata:public_precipitation_15min',filter = filterxml,outputFormat='application/json')
    # convert IO-byte to bytes
    bytesD=bytes(response.read())
    # convert to json
    data2 = json.loads(bytesD)
    return data2    

"""for index in range(len(datanorm)):
kenn=datanorm['properties.kenn'][index], 
value=datanorm['properties.value'][index],
start_measure=datanorm['properties.start_measure'][index],
end_measure=datanorm['properties.end_measure'][index]
print(index ,':' , value,kenn,start_measure,end_measure)"""

"""for i in datanorm:
value = datanorm['properties.kenn']
print(value)"""