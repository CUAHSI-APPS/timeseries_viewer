from lxml import etree
from datetime import datetime
from datetime import timedelta
from dateutil import parser
from django.http import HttpResponse
from .app import TsConverter as app
import csv
import zipfile
import StringIO
import requests
from tethys_sdk.gizmos import TimeSeries
import xml.etree.ElementTree as ET
import time
import numpy
import zipfile
import os


def get_app_base_uri(request):
    base_url = request.build_absolute_uri()
    if "?" in base_url:
        base_url = base_url.split("?")[0]
    return base_url


def get_workspace():
    return app.get_app_workspace().path


def get_version(root):
    wml_version = None
    for element in root.iter():
        if '{http://www.opengis.net/waterml/2.0}Collection' in element.tag:
            wml_version = '2.0'
            break
        if '{http://www.cuahsi.org/waterML/1.1/}timeSeriesResponse' \
        or '{http://www.cuahsi.org/waterML/1.0/}timeSeriesResponse' in element.tag:
            wml_version = '1'
            break
    return wml_version

#drew 20150401 convert date string into datetime obj
def time_str_to_datetime(t):
    try:
        t_datetime=parser.parse(t)
        return t_datetime
    except ValueError:
        print "time_str_to_datetime error: "+ t
        raise Exception("time_str_to_datetime error: "+ t)
        return datetime.now()


#drew 20150401 convert datetime obj into decimal second (epoch second)
def time_to_int(t):
    try:
        d=parser.parse(t)
        t_sec_str=d.strftime('%s')
        return int(t_sec_str)
    except ValueError:
        print ("time_to_int error: "+ t)
        raise Exception('time_to_int error: ' + t)


def parse_1_0_and_1_1(root):
    print "running parse_1_0_and_1_1"
    root_tag = root.tag.lower()
    print "root tag: " + root_tag
    try:
        if 'timeseriesresponse' in root_tag or 'timeseries' in root_tag or "envelope" in root_tag:

            # lists to store the time-series data
            for_graph = []
            for_highchart = []
            my_times = []
            my_values = []

            t0 = time.time()

            # metadata items
            units, site_name, variable_name = None, None, None
            unit_is_set = False

            # iterate through xml document and read all values
            for element in root.iter():
                brack_lock = -1
                if '}' in element.tag:
                    brack_lock = element.tag.index('}')  #The namespace in the tag is enclosed in {}.
                    tag = element.tag[brack_lock+1:]     #Takes only actual tag, no namespace

                if 'value' == tag:
                    my_times.append(element.attrib['dateTime'])
                    my_values.append(element.text)
                else:
                    if 'unitName' == tag:  # in the xml there is a unit for the value, then for time. just take the first
                        if not unit_is_set:
                            units = element.text
                            unit_is_set = True

                    if 'noDataValue' == tag:
                        nodata = element.text
                    if 'siteName' == tag:
                        site_name = element.text
                    if 'variableName' == tag:
                        variable_name = element.text
                    if 'organization'==tag:
                        organization = element.text

            print "root.iter time: " + str(time.time() - t0)

            t0 = time.time()

            for i in range(0, len(my_times)):
                t= datetime.strptime(my_times[i], '%Y-%m-%dT%H:%M:%S')

                #check to see if there are null values in the time series
                if my_values[i] == nodata:
                    for_highchart.append([t, None])
                else:
                    for_highchart.append([t, float(my_values[i])])
                    for_graph.append(float(my_values[i]))

            smallest_time = for_highchart[0][0]
            value_count = len(for_highchart)
            largest_time = for_highchart[value_count - 1][0]

            print "convert time time: " + str(time.time() - t0)

            mean = numpy.mean(for_graph)
            mean = float(format(mean, '.2f'))
            median = numpy.median(for_graph)
            stdev = numpy.std(for_graph)

            print mean
            print median
            print stdev

            return {
                    'site_name': site_name,
                    'start_date': str(smallest_time),
                    'end_date':str(largest_time),
                    'variable_name': variable_name,
                    'units': units,
                    'for_graph': for_graph,
                    'wml_version': '1',
                    'for_highchart':for_highchart,
                    'mean': mean,
                    'median': median,
                    'stdev': stdev,
                    'count': value_count,
                    'organization': organization
            }
        else:
            print "Parsing error: The waterml document doesn't appear to be a WaterML 1.0/1.1 time series"
            return "Parsing error: The waterml document doesn't appear to be a WaterML 1.0/1.1 time series"
    except Exception, e:
        print e
        return "Parsing error: The Data in the Url, or in the request, was not correctly formatted for water ml 1."


def getResourceIDs(page_request):
    cuahsi_data = page_request.GET['res_id']#retrieves ids from url
    cuahsi_split = cuahsi_data.split(',')#splits ideas by commma
    return cuahsi_split


def findZippedUrl(page_request, res_id):
    base_url = page_request.build_absolute_uri()
    if "?" in base_url:
        base_url = base_url.split("?")[0]
        zipped_url = base_url + "temp_waterml/" + res_id + ".xml"
        return zipped_url


# Prepare for Chart Parameters
def chartPara(ts_original,for_highcharts,legend1):

    timeseries_plot = TimeSeries(
        height='600px',
        width='600px',
        engine='highcharts',
        title= ts_original ['site_name']+" "+ts_original['start_date']+" - "+ts_original['end_date'],
        y_axis_title=ts_original['variable_name'],
        y_axis_units=ts_original['units'],

        legend= legend1,
        series= for_highcharts
    )
    return timeseries_plot



def parse_2_0(root):

    try:
        if 'Collection' in root.tag:
            ts = etree.tostring(root)
            keys = []
            vals = []
            for_graph = []
            for_highchart=[]
            units, site_name, variable_name, latitude, longitude, method = None, None, None, None, None, None
            name_is_set = False
            variable_name = root[1].text
            organization = None
            for element in root.iter():
                if 'MeasurementTVP' in element.tag:
                        for e in element:
                            if 'time' in e.tag:
                                keys.append(e.text)
                            if 'value' in e.tag:
                                vals.append(e.text)
                if 'uom' in element.tag:
                    units = element.text
                if 'MonitoringPoint' in element.tag:
                    for e in element.iter():
                        if 'name' in e.tag and not name_is_set:
                            site_name = e.text
                            name_is_set = True
                        if 'pos' in e.tag:
                            lat_long = e.text
                            lat_long = lat_long.split(' ')
                            latitude = lat_long[0]
                            longitude = lat_long[1]
                if 'observedProperty' in element.tag:
                    for a in element.attrib:
                        if 'title' in a:
                            variable_name = element.attrib[a]
                if 'ObservationProcess' in element.tag:
                    for e in element.iter():
                        if 'processType' in e.tag:
                            for a in e.attrib:
                                if 'title' in a:
                                    method=e.attrib[a]

                if 'organization' in element.tag:
                    organization = element.text
            for i in range(0,len(keys)):
                time_str=keys[i]
                time_obj=time_str_to_datetime(time_str)

                if vals[i] == "-9999.0"or vals[i]=="-9999":
                    val_obj = None
                else:
                    val_obj=float(vals[i])

                item=[time_obj,val_obj]
                for_highchart.append(item)
            values = dict(zip(keys, vals))

            for k, v in values.items():
                t = time_to_int(k)
                for_graph.append({'x': t, 'y': float(v)})
            smallest_time = list(values.keys())[0]
            largest_time = list(values.keys())[0]
            for t in list(values.keys()):
                if t < smallest_time:
                    smallest_time = t
                if t> largest_time:
                    largest_time = t

            return {'time_series': ts,
                    'site_name': site_name,
                    'start_date': smallest_time,
                    'end_date':largest_time,
                    'variable_name': variable_name,
                    'units': units,
                    'values': values,
                    'for_graph': for_graph,
                    'wml_version': '2.0',
                    'latitude': latitude,
                    'longitude': longitude,
                    'for_highchart': for_highchart,
		            'test': test,
                    'organization':organization
                    }
        else:
            print "Parsing error: The waterml document doesn't appear to be a WaterML 2.0 time series"
            return "Parsing error: The waterml document doesn't appear to be a WaterML 2.0 time series"
    except:
        print "Parsing error: The Data in the Url, or in the request, was not correctly formatted."
        return "Parsing error: The Data in the Url, or in the request, was not correctly formatted."



def Original_Checker(html):
    root = etree.XML(html)

    wml_version = get_version(root)
    if wml_version == '1':
        return parse_1_0_and_1_1(root)
    elif wml_version == '2.0':
        return parse_2_0(root)


def unzip_waterml(request, id, src='cuahsi'):
    temp_dir = get_workspace()

    if src == 'cuahsi':
        url_zip = 'http://bcc-hiswebclient.azurewebsites.net/CUAHSI/HydroClient/WaterOneFlowArchive/'+id+'/zip'
    elif src == 'test':
        url_zip = 'http://' + request.META['HTTP_HOST'] + '/apps/data-cart/showfile/'+id
    r = requests.get(url_zip, verify=False)
    try:
        z = zipfile.ZipFile(StringIO.StringIO(r.content))
        file_list = z.namelist()

        try:
            for file in file_list:
                file_data = z.read(file)
                file_temp_name = temp_dir + '/' + id + '.xml'
                print "unzipping file " + file_temp_name

                file_temp = open(file_temp_name, 'wb')
                file_temp.write(file_data)
                file_temp.close()

                print "unzipped file " + file_temp_name

                #getting the URL of the zip file
                base_url = request.build_absolute_uri()
                if "?" in base_url:
                    base_url = base_url.split("?")[0]

                zipped_url = base_url + "temp_waterml/cuahsi/" + id + '.xml'
                print zipped_url

                print "WaterML file unzipped successfully."
        except etree.XMLSyntaxError as e: #checks to see if data is an xml
            print "Error:Not XML"
            #quit("not valid xml")
        except ValueError, e: #checks to see if Url is valid
            print "Error:invalid Url"
        except TypeError, e: #checks to see if xml is formatted correctly
            print "Error:string indices must be integers not str"
    except  zipfile.BadZipfile as e:
            error_message = "Bad Zip File"
            print "Bad Zip file"
    return zipped_url



def file_unzipper(url_cuashi):
    #this function is for unzipping files
    r = requests.get(url_cuashi)
    z = zipfile.ZipFile(StringIO.StringIO(r.content))

    file_list = z.namelist()
    for  file in file_list:
        z.read(file)
    return file_list



def csv_reader(file):
    #this was designed to read the cuashi data which is in csv format, however, this likely change to waterml format
    for_highchart=[]
    z_object = file.open("nwisuv-salt_creek_at_nephi,_ut-gage_height,_feet.csv")
    csv_cuashi = csv.reader(z_object)

    for row in csv_cuashi:
        #row   associate time_obj and val_obj with row values
        time_obj = row[0]
        val_obj = row[3]
        item=[time_obj,val_obj]
        for_highchart.append(item)

    return for_highchart