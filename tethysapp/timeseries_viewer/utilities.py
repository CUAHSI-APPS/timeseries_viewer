# coding=utf-8
#
# Created by Matthew Bayles, 2016
from lxml import etree
import numpy
import urllib2
import urllib
from .app import TimeSeriesViewer
import StringIO
import time
import zipfile
import os
import controllers
import collections
import json
from suds.transport import TransportError
from suds.client import Client
from xml.sax._exceptions import SAXParseException
import requests
import sqlite3
import uuid
import ciso8601
from hs_restclient import HydroShare, HydroShareAuthOAuth2, \
    HydroShareNotAuthorized, HydroShareNotFound
import hs_restclient as hs_r
from django.conf import settings
from time import gmtime, strftime
from time import mktime as mktime
from tethys_services.backends.hs_restclient_helper import get_oauth_hs

def get_workspace():
    """Get path to Tethys Workspace"""

    return TimeSeriesViewer.get_app_workspace().path


def get_version(root):
    """
    Get version of waterml file

    Parameters
    __________
    root: lxml object
        The contents of an xml file that have been parsed using the etree
        method in the lxml library
    Returns
    _______
    string
        A string representation of the waterml version
    """
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


def parse_1_0_and_1_1(root):
    """
    Get version of waterml file

    Parameters
    __________
    root: lxml object
        The contents of an xml file that have been parsed using the etree
        method in the lxml library
    Returns
    _______
    site_name
    variable_name
    units
    meta_dic
    organization'
    quality
    method
    status
    datatype
    valuetype
    samplemedium
    timeunit
    sourcedescription
    timesupport
    master_counter
    master_values
    master_times
    master_boxplot
    master_stat'
    master_data_values
    """
    print type(root)
    print '!!!!!!!!!!!!'
    # print 'begin parse'
    # print time.ctime()
    root_tag = root.tag.lower()
    boxplot = []
    master_values = collections.OrderedDict()
    master_times = collections.OrderedDict()
    master_boxplot = collections.OrderedDict()
    master_stat = collections.OrderedDict()
    master_data_values = collections.OrderedDict()
    meth_qual = []  # List of all the quality, method, and source combinations
    for_canvas = []
    meta_dic = {'method': {}, 'quality': {}, 'source': {}, 'organization': {},
                'quality_code': {}}
    m_des = None
    m_code = None
    m_org = None
    x_value = []
    y_value = []
    master_counter = True
    nodata = "-9999"  # default NoData value. The actual NoData value is read from the XML noDataValue tag
    timeunit = None
    sourcedescription = None
    timesupport = None
    units, site_name, variable_name, quality, method, organization = None, None, None, None, None, None
    unit_is_set = False
    datatype = None
    valuetype = None
    samplemedium = None
    try:
        if 'timeseriesresponse' in root_tag or 'timeseries' in root_tag or "envelope" in root_tag or 'timeSeriesResponse' in root_tag:

            # lists to store the time-series data

            # iterate through xml document and read all values
            for element in root.iter():

                bracket_lock = -1
                if '}' in element.tag:
                    # print element.tag
                    bracket_lock = element.tag.index(
                        '}')  # The namespace in the tag is enclosed in {}.
                    tag = element.tag[
                          bracket_lock + 1:]  # Takes only actual tag, no namespace

                    if 'value' != tag:
                        # in the xml there is a unit for the value, then for time. just take the first
                        # print tag
                        if 'unitName' == tag or 'units' == tag or 'UnitName' == tag or 'unitCode' == tag:
                            if not unit_is_set:
                                units = element.text

                                unit_is_set = True
                        # print units
                        if 'noDataValue' == tag:
                            nodata = float(element.text)
                        if 'siteName' == tag:
                            site_name = element.text
                        if 'variableName' == tag:
                            variable_name = element.text
                        if 'organization' == tag or 'Organization' == tag or 'siteCode' == tag:
                            try:
                                organization = element.attrib['agencyCode']
                            except:
                                organization = element.text
                        if 'definition' == tag or 'qualifierDescription' == tag:
                            quality = element.text
                        if 'methodDescription' == tag or 'MethodDescription' == tag:
                            # print element.attrib['methodID']
                            method = element.text
                        if 'dataType' == tag:
                            datatype = element.text
                        if 'valueType' == tag:
                            valuetype = element.text
                        if "sampleMedium" == tag:
                            samplemedium = element.text
                        if "timeSupport" == tag or "timeInterval" == tag:
                            timesupport = element.text
                        if "unitName" == tag or "UnitName" == tag:
                            timeunit = element.text
                        if "sourceDescription" == tag or "SourceDescription" == tag:
                            sourcedescription = element.text
                        if "method" == tag.lower():
                            try:
                                mid = element.attrib['methodID']
                            except:
                                mid = None
                                m_code = ''
                            for subele in element:
                                if 'methodcode' in subele.tag.lower() and m_code == '':
                                    m_code = subele.text
                                    m_code = m_code.replace(" ", "")

                                if mid != None:
                                    m_code = element.attrib['methodID']
                                    m_code = m_code.replace(" ", "")
                                if 'methoddescription' in subele.tag.lower():
                                    m_des = subele.text

                            meta_dic['method'].update({m_code: m_des})
                        if "source" == tag.lower():

                            try:
                                sid = element.attrib['sourceID']
                            except:
                                sid = None
                                m_code = ''

                            for subele in element:
                                if 'sourcecode' in subele.tag.lower() and m_code == '':
                                    m_code = subele.text
                                    m_code = m_code.replace(" ", "")
                                if sid != None:
                                    m_code = element.attrib['sourceID']
                                    m_code = m_code.replace(" ", "")
                                if 'sourcedescription' in subele.tag.lower():
                                    m_des = subele.text
                                if 'organization' in subele.tag.lower():
                                    m_org = subele.text
                            meta_dic['source'].update({m_code: m_des})
                            meta_dic['organization'].update({m_code: m_org})
                        if "qualitycontrollevel" == tag.lower():
                            try:
                                qlc = element.attrib['qualityControlLevelID']
                            except:
                                qlc = None
                                m_code = ''
                            for subele in element:
                                if qlc != None:
                                    m_code = element.attrib[
                                        'qualityControlLevelID']
                                    m_code = m_code.replace(" ", "")
                                if 'qualitycontrollevelcode' in subele.tag.lower():
                                    m_code1 = subele.text
                                    m_code1 = m_code1.replace(" ", "")
                                if 'qualitycontrollevelcode' in subele.tag.lower() and m_code == '':
                                    m_code = subele.text
                                    m_code = m_code1.replace(" ", "")
                                if 'definition' in subele.tag.lower():
                                    m_des = subele.text
                            meta_dic['quality'].update({m_code: m_des})
                            meta_dic['quality_code'].update({m_code1: m_code})
                            # print meta_dic
                    elif 'value' == tag:
                        # try:
                        #     n = element.attrib['dateTimeUTC']
                        # except:
                        #     n =element.attrib['dateTime']
                        n = element.attrib['dateTime']
                        # print n
                        n = ciso8601.parse_datetime(n)
                        n=n.timetuple()
                        n = time.mktime(n)
                        # print n
                        # print type(n)
                        # print ts
                        # if 'Z' in n:
                        #     n = n.replace('Z','')
                        #     print "there is a z"
                        #     print n
                        try:
                            quality = element.attrib['qualityControlLevelCode']
                        except:
                            quality = ''
                        try:
                            quality1 = element.attrib['qualityControlLevel']
                        except:
                            quality1 = ''
                        if quality == '' and quality1 != '':
                            quality = quality1
                        try:
                            method = element.attrib['methodCode']
                        except:
                            method = ''
                        try:
                            method1 = element.attrib['methodID']
                        except:
                            method1 = ''
                        if method == '' and method1 != '':
                            method = method1
                        try:
                            source = element.attrib['sourceCode']
                        except:
                            source = ''
                        try:
                            source1 = element.attrib['sourceID']
                        except:
                            source1 = ''
                        if source == '' and source1 != '':
                            source = source1
                        dic = quality + 'aa' + method + 'aa' + source
                        dic = dic.replace(" ", "")
                        if dic not in meth_qual:
                            meth_qual.append(dic)
                            master_values.update({dic: []})
                            master_times.update({dic: []})
                            master_boxplot.update({dic: []})
                            master_stat.update({dic: []})
                            master_data_values.update({dic: []})

                        v = element.text
                        if float(v) == nodata:
                            value = None
                            # x_value.append(n)
                            # y_value.append(value)
                            v = None

                        else:
                            v = float(element.text)
                            # x_value.append(n)
                            # y_value.append(v)
                            # records only none null values for running statistics
                            master_data_values[dic].append(v)
                        master_values[dic].append(v)
                        master_times[dic].append(n)

            for item in master_data_values:
                if len(master_data_values[item]) == 0:
                    mean = None
                    median = None
                    quar1 = None
                    quar3 = None
                    min1 = None
                    max1 = None
                else:
                    mean = numpy.mean(master_data_values[item])
                    mean = float(format(mean, '.2f'))
                    median = float(
                        format(numpy.median(master_data_values[item]), '.2f'))
                    quar1 = float(
                        format(numpy.percentile(master_data_values[item], 25),
                               '.2f'))
                    quar3 = float(
                        format(numpy.percentile(master_data_values[item], 75),
                               '.2f'))
                    min1 = float(format(min(master_data_values[item]), '.2f'))
                    max1 = float(format(max(master_data_values[item]), '.2f'))
                master_stat[item].append(mean)
                master_stat[item].append(median)
                master_stat[item].append(max1)
                master_stat[item].append(min1)
                master_boxplot[item].append(1)
                master_boxplot[item].append(
                    min1)  # adding data for the boxplot
                master_boxplot[item].append(quar1)
                master_boxplot[item].append(median)
                master_boxplot[item].append(quar3)
                master_boxplot[item].append(max1)
                # print 'end parse'
                # print time.ctime()
                error =''
            return [{
                'site_name': site_name,
                'variable_name': variable_name,
                'units': units,
                'meta_dic': meta_dic,
                # 'organization': organization,
                # 'quality': quality,
                # 'method': method,
                'status': 'success',
                'datatype': datatype,
                'valuetype': valuetype,
                'samplemedium': samplemedium,
                'timeunit': timeunit,
                'sourcedescription': sourcedescription,
                'timesupport': timesupport,
                # 'master_counter': master_counter,
                'master_values': master_values,
                'master_times': master_times,
                'master_boxplot': master_boxplot,
                'master_stat': master_stat,
                # 'master_data_values': master_data_values
            },
                    error]
        else:
            parse_error = "Parsing error: The WaterML document doesn't appear to be a WaterML 1.0/1.1 time series"
            # error_report(
            #     "Parsing error: The WaterML document doesn't appear to be a WaterML 1.0/1.1 time series")
            print parse_error
            return [None,parse_error]
    except Exception, e:
        data_error = "Parsing error: The Data in the Url, or in the request, was not correctly formatted for water ml 1."
        # error_report(
        #     "Parsing error: The Data in the Url, or in the request, was not correctly formatted.")
        print data_error
        print e
        return [None,data_error]


def parse_2_0(root):  # waterml 2 has not been implemented in the viewer at this time
    print "running parse_2"
    root_tag = root.tag.lower()
    boxplot = []
    master_values = collections.OrderedDict()
    master_times = collections.OrderedDict()
    master_boxplot = collections.OrderedDict()
    master_stat = collections.OrderedDict()
    master_data_values = collections.OrderedDict()
    meth_qual = []  # List of all the quality, method, and source combinations
    for_canvas = []
    meta_dic = {'method': {}, 'quality': {}, 'source': {}, 'organization': {},
                'quality_code': {}}
    m_des = None
    m_code = None
    m_org = None
    x_value = []
    y_value = []
    master_counter = True
    nodata = "-9999"  # default NoData value. The actual NoData value is read from the XML noDataValue tag
    timeunit = None
    sourcedescription = None
    timesupport = None
    # metadata items
    units, site_name, variable_name, quality, method, organization = None, None, None, None, None, None
    unit_is_set = False
    datatype = None
    valuetype = None
    samplemedium = None
    # we only display the first 50000 values
    threshold = 50000000

    try:
        if 'Collection' in root.tag:
            # ts = etree.tostring(root)
            # keys = []
            # vals = []
            # for_graph = []
            # for_highchart=[]
            # units, site_name, variable_name, latitude, longitude, method = None, None, None, None, None, None
            # name_is_set = False
            # variable_name = root[1].text
            # organization = None
            # quality = None
            # method =None
            # datatype = None
            # valuetype = None
            # samplemedium = None
            # timeunit=None
            # sourcedescription = None
            # timesupport =None
            # smallest_value = 0
            for element in root.iter():
                if 'MeasurementTVP' in element.tag:
                    for e in element:
                        try:
                            n = element.attrib['dateTimeUTC']
                        except:
                            n = element.attrib['dateTime']
                        try:
                            quality = element.attrib['qualityControlLevelCode']
                        except:
                            quality1 = ''
                        try:
                            method = element.attrib['methodCode']
                        except:
                            method = ''
                        try:
                            source = element.attrib['sourceCode']
                        except:
                            source = ''
                        dic = quality + 'aa' + method + 'aa' + source
                        if dic not in meth_qual:
                            meth_qual.append(dic)
                            master_values.update({dic: []})
                            master_times.update({dic: []})
                            master_boxplot.update({dic: []})
                            master_stat.update({dic: []})
                            master_data_values.update({dic: []})

                        v = element.text
                        if v == nodata:
                            value = None
                            x_value.append(n)
                            y_value.append(value)
                            v = None

                        else:
                            v = float(element.text)
                            x_value.append(n)
                            y_value.append(v)
                            master_data_values[dic].append(
                                v)  # records only none null values for running statistics
                        master_values[dic].append(v)
                        master_times[dic].append(n)


                        # if 'time' in e.tag:
                        #     keys.append(e.text)
                        # if 'value' in e.tag:
                        #     vals.append(e.text)
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
                                    method = e.attrib[a]
                print element.tag
                if 'organization' in element.tag:
                    organization = element.text
                if 'definition' in element.tag:
                    quality = element.text
                if 'methodDescription' in element.tag:
                    method = element.text
                if 'dataType' in element.tag:
                    datatype = element.text
                if 'valueType' in element.tag:
                    valuetype = element.text
                if "sampleMedium" in element.tag:
                    samplemedium = element.text
                if "timeSupport" in element.text:
                    timesupport = element.text
                if "unitName" in element.text:
                    timeunit = element.text
                if "sourceDescription" in element.text:
                    sourcedescription = element.text

            for i in range(0, len(keys)):
                time_str = keys[i]
                time_obj = time_str_to_datetime(time_str)

                if vals[i] == "-9999.0" or vals[i] == "-9999":
                    val_obj = None
                else:
                    val_obj = float(vals[i])

                item = [time_obj, val_obj]
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
                if t > largest_time:
                    largest_time = t
            for v in list(values.vals()):
                if v < smallest_value:
                    smallest_value = t

            return {'time_series': ts,
                    'site_name': site_name,
                    'start_date': smallest_time,
                    'end_date': largest_time,
                    'variable_name': variable_name,
                    'units': units,
                    'values': values,
                    'wml_version': '2.0',
                    'latitude': latitude,
                    'longitude': longitude,
                    'for_highchart': for_highchart,
                    'organization': organization,
                    'quality': quality,
                    'method': method,
                    'status': 'success',
                    'datatype': datatype,
                    'valuetype': valuetype,
                    'samplemedium': samplemedium,
                    'smallest_value': smallest_value,
                    'timeunit': timeunit,
                    'sourcedescription': sourcedescription,
                    'timesupport': timesupport,
                    'values': vals
                    }
        else:
            print "Parsing error: The waterml document doesn't appear to be a WaterML 2.0 time series"
            # error_report(
            #     "Parsing error: The waterml document doesn't appear to be a WaterML 2.0 time series")
            return "Parsing error: The waterml document doesn't appear to be a WaterML 2.0 time series"
    except:
        print "Parsing error: The Data in the Url, or in the request, was not correctly formatted."
        # error_report(
        #     "Parsing error: The Data in the Url, or in the request, was not correctly formatted.")
        return "Parsing error: The Data in the Url, or in the request, was not correctly formatted."


def Original_Checker(xml_file):
    try:
        tree = etree.parse(xml_file)
        root = tree.getroot()
        wml_version = get_version(root)

        if wml_version == '1':

            return parse_1_0_and_1_1(root)

        elif wml_version == '2.0':
            return parse_2_0(root)
    except ValueError, e:
        print e

        return read_error_file(xml_file)
    except Exception as e:
        print e

        return read_error_file(xml_file)


def read_error_file(xml_file):
    try:
        f = open(xml_file)
        return f.readline()
    except:

        return [None,'invalid WaterML file']


def unzip_waterml(request, res_id, src):
    file_number = 0
    temp_dir = get_workspace()
    file_type = None
    error = ''
    file_path = ''
    # if not os.path.exists(temp_dir+"/id"):
    #     os.makedirs(temp_dir+"/id")
    if 'hydroshare' in src:
        # Get file location of python scripts
        cwd = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        # if controllers.use_hs_client_helper:
        #     print 'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG'
        #     hs = controllers.get_oauth_hs(request)
        # else:

        if controllers.use_hs_client_helper:
            hs = controllers.get_oauth_hs(request)
        else:
            hs = getOAuthHS(request)
            # hs = get_oauth_hs(request)
        # hs = getOAuthHS(request)
        # file_path_id = get_workspace() + '/id'
        file_path_id = get_workspace()
        status = 'running'
        delay = 0
        while (status == 'running' or delay < 10):

            if (delay > 15):
                error = 'Request timed out. ' + error
                break
            elif (status == 'done'):
                error = ''
                break
            else:
                try:
                    hs.getResource(res_id, destination=file_path_id,
                                   unzip=True)
                    status = 'done'
                except HydroShareNotAuthorized as e:
                    print "Not authorized"
                    error = 'Current user does not have permission to view this resource'
                    # error = str(e)
                    break
                except HydroShareNotFound as e:
                    print "Resource not found"
                    error = 'Resource was not found. Please try again in a few moments'
                    # error = str(e)
                    time.sleep(2)
                    delay = delay + 1

                except Exception as e:
                    print e
                    print type(e).__name__
                    print e.__class__.__name__
                    error = str(e)
                    status = 'running'
                    time.sleep(2)
                    delay = delay + 1

        # hs.getResource(res_id, destination=file_path_id, unzip=True)
        if error == '':
            try:
                root_dir = file_path_id + '/' + res_id
                data_dir = root_dir + '/' + res_id + '/data/contents/'
                for subdir, dirs, files in os.walk(root_dir):
                    for file in files:
                        path = data_dir + file
                        if 'wml_1_' in file:
                            file_type = 'waterml'
                            with open(path, 'r') as f:
                                file_data = f.read()
                                f.close()
                                # file_path = temp_dir + '/id/' + res_id + '.xml'
                                file_path = temp_dir + res_id + '.xml'
                                file_temp = open(file_path, 'wb')
                                file_temp.write(file_data)
                                file_temp.close()
                        elif '.refts.json' in file:
                            file_type = '.json.refts'
                            file_number = parse_ts_layer(path)
                        elif '.sqlite' in file:
                            file_path = path
                            file_type = 'sqlite'
                if file_type == None:
                    error = "No supported file type found. This app supports resource types HIS " \
                            "Referenced Time Series, Time Series, and Generic with file extension .json.refts"
            except Exception as e:
                error = str(e)
    # Data from USGS and AHPS Gaugeviewer WML
    elif "xmlrest" in src:
        file_type = 'waterml'
        res_id = request.POST.get('url_xml')
        # Creates a unique id for the time series
        xml_id = str(uuid.uuid4())
        res = urllib.unquote(res_id).decode()
        r = requests.get(res, verify=False)
        file_data = r.content
        # file_path = temp_dir + '/id/'+xml_id+'.xml'
        file_path = temp_dir + '/' + xml_id + '.xml'
        file_temp = open(file_path, 'wb')
        file_temp.write(file_data)
        file_temp.close()
    elif src == 'cuahsi':
        # get the URL of the remote zipped WaterML resource
        file_type = 'waterml'
        app_host =request.META['HTTP_HOST']
        if 'appsdev.hydroshare' in app_host:
        # if '127.0.0' in app_host:
        # url_zip = 'http://qa-webclient-solr.azurewebsites.net/CUAHSI/HydroClient/WaterOneFlowArchive/' + res_id + '/zip'
            url_zip = 'http://qa-hiswebclient.azurewebsites.net/CUAHSI/HydroClient/WaterOneFlowArchive/' + res_id + '/zip'
        else:
            url_zip = 'http://data.cuahsi.org/CUAHSI/HydroClient/WaterOneFlowArchive/' + res_id + '/zip'
        try:
            r = requests.get(url_zip, verify=False)
            z = zipfile.ZipFile(StringIO.StringIO(r.content))
            file_list = z.namelist()
            try:
                for file in file_list:
                    file_data = z.read(file)
                    # file_path = temp_dir + '/id/' + res_id + '.xml'
                    file_path = temp_dir + '/' +res_id + '.xml'
                    # file_temp = open(file_temp_name, 'wb')
                    with open(file_path, 'wb') as f:
                        f.write(file_data)
                        # file_temp.close()
            # error handling
            # checks to see if data is an xml
            except etree.XMLSyntaxError as e:
                print "Error:Not XML"
                error = "Error:Not XML"
            # checks to see if Url is valid
            except ValueError, e:
                print "Error:invalid Url"
                error = "Error:invalid Url"
            # checks to see if xml is formatted correctly
            except TypeError, e:
                error = "Error:string indices must be integers not str"
                print "Error:string indices must be integers not str"
        # check if the zip file is valid
        except zipfile.BadZipfile as e:
            error = "Bad Zip File"
            print error

        except Exception as e:
            print error
            error = str(e)

    data_for_chart = []
    # if we don't have the xml file, download and unzip it
    # file_number = int(file_meta['file_number'])
    # file_path = file_meta['file_path']
    # file_type = file_meta['file_type']
    # error = file_meta['error']

    if error == '':
        if file_type == 'waterml':
            # file_path = utilities.waterml_file_path(res_id,xml_id)
            data_for_chart.append(Original_Checker(file_path)[0])
            error = Original_Checker(file_path)[1]
        elif file_type == '.json.refts':
            for i in range(0, file_number):
                # file_path = temp_dir+'/id/timeserieslayer'+str(i)+'.xml'
                file_path = temp_dir+'/timeserieslayer'+str(i)+'.xml'
                data_for_chart.append(Original_Checker(file_path)[0])
                error = Original_Checker(file_path)[1]
        elif file_type == 'sqlite':

            conn = sqlite3.connect(file_path)
            c = conn.cursor()
            c.execute('SELECT Results.ResultID FROM Results')
            num_series = c.fetchall()
            conn.close()
            for series in num_series:
                str_series = str(series[0])
                data_for_chart.append(parse_odm2(file_path, str_series))

        if isinstance(data_for_chart[0],basestring)==True:
            error = data_for_chart[0]
    if error is not '':
        error_report(error, res_id)
    return {'data': data_for_chart, 'error': error}
    # return {'file_number': file_number, "file_type": file_type,
    # 'error': error,
    #         'file_path': file_path}


def waterml_file_path(res_id, xml_id):
    base_path = get_workspace()

    # file_path = base_path + "/id/"+xml_id #+ res_id
    file_path = base_path + xml_id  # + res_id

    if not file_path.endswith('.xml'):
        file_path += '.xml'
    return file_path


def error_report(text, res_id):
    temp_dir = get_workspace()
    file_temp_name = temp_dir + '/timeseries_viewer_error_report.txt'
    if not os.path.exists(file_temp_name):
        file_temp = open(file_temp_name, 'a')
        file_temp.write('Error Reports: ')
        file_temp.close()
    with  open(file_temp_name, 'a') as file_temp:
        # time = datetime.now()
        time2 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        data = dict(Date_Time_UTC=time2, Error_text=text, Resource_ID=res_id)
        json.dump(data, file_temp)
        file_temp.write(',')


def view_counter(request):
    temp_dir = get_workspace()
    file_temp_name = temp_dir + '/timeseries_viewer_view_counter.txt'
    if not os.path.exists(file_temp_name):
        file_temp = open(file_temp_name, 'w')
        file_temp.write('0')
        file_temp.close()
    with open(file_temp_name, 'r+') as file_temp:
        if 'mbayles' not in str(request.user):
            # file_temp_name = temp_dir + '/timeseries_viewer_view_counter.txt'
            if not os.path.exists(temp_dir + "/timeseries_viewer_view_counter.txt"):
                # file_temp = open(file_temp_name, 'a')
                first = '1'
                file_temp.write(first)
                # file_temp.close()
            else:
                # file_temp = open(file_temp_name, 'r+')
                content = file_temp.read()
                number = int(content)
                number = number + 1
                number = str(number)
                file_temp.seek(0)
                file_temp.write(number)
                # file_temp.close()


def parse_ts_layer(path):
    
    counter = 0
    error = ''
    response = None
    with open(path, 'r') as f:
        data = f.read()
    data = data.encode(encoding='UTF-8')
    data = data.replace("'", '"')
    json_data = json.loads(data)
    
    json_data = json_data["timeSeriesReferenceFile"]
    layer = json_data['referencedTimeSeries']
   
    for sub in layer:
       
        ref_type = sub['requestInfo']['refType']
        service_type = sub['requestInfo']['serviceType']
        url = sub['requestInfo']['url']
        site_code = sub['site']['siteCode']
        variable_code = sub['variable']['variableCode']
        start_date = sub['beginDate']
        end_date = sub['endDate']
        auth_token = ''
        print ref_type
        print "!!!!!!!!!!!!!!!!!!!"
        if ref_type == 'WOF':
            print 'wof'
            if service_type == 'SOAP':
                print 'soap'
                if 'nasa' in url:
                    
                    headers = {'content-type': 'text/xml'}
                    body = """<?xml version="1.0" encoding="utf-8"?>
                        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                          <soap:Body>
                            <GetValuesObject xmlns="http://www.cuahsi.org/his/1.0/ws/">
                              <location>""" + site_code + """</location>
                              <variable>""" + variable_code + """</variable>
                              <startDate>""" + start_date + """</startDate>
                              <endDate>""" + end_date + """</endDate>
                              <authToken></authToken>
                            </GetValuesObject>
                          </soap:Body>
                        </soap:Envelope>"""
                    body = body.encode('utf-8')
                    response = requests.post(url, data=body, headers=headers)
                    response = response.content
                else:
                    print 'connecting to soap'
                    client = connect_wsdl_url(url)
                    try:
                        response = client.service.GetValues(site_code,
                                                                  variable_code,
                                                                  start_date,
                                                                  end_date,
                                                                  auth_token)
                    except:
                        error = "unable to connect to HydroSever"
                        print error
                temp_dir = get_workspace()
                file_path = temp_dir + '/timeserieslayer' + str(counter) + '.xml'
                try:
                    response = response.encode('utf-8')
                except:
                    response = response
                with open(file_path, 'w') as outfile:
                    outfile.write(response)
            if (service_type == 'REST'):
                waterml_url = url + '/GetValueObject'
                response = urllib2.urlopen(waterml_url)
                html = response.read()
            counter = counter + 1
    return counter


def connect_wsdl_url(wsdl_url):
    try:
        client = Client(wsdl_url)
    except TransportError:
        raise Exception('Url not found')
    except ValueError:
        raise Exception(
            'Invalid url')  # ought to be a 400, but no page implemented for that
    except SAXParseException:
        raise Exception("The correct url format ends in '.asmx?WSDL'.")
    except:
        raise Exception("Unexpected error")
    return client


def parse_odm2(file_path, result_num):
    master_times = []
    master_values = collections.OrderedDict()
    master_times = collections.OrderedDict()
    site_name = None
    variable_name = None
    units = None
    meta_dic = None
    for_canvas = None
    organization = None
    quality = None
    method = None
    source = None
    datatype = None
    valuetype = None
    samplemedium = None
    timeunit = None
    sourcedescription = None
    timesupport = None
    master_counter = True
    boxplot = None
    master_boxplot = collections.OrderedDict()
    master_stat = collections.OrderedDict()
    master_data_values = collections.OrderedDict()
    meta_dic = {'method': {}, 'quality': {}, 'source': {}, 'organization': {},
                'quality_code': {}}
    meth_qual = []  # List of all the quality, method, and source combinations
    nodatavalue = None
    conn = sqlite3.connect(file_path)
    c = conn.cursor()
    c.execute(
        'SELECT Variables.VariableNameCV,Units.UnitsName,'
        'Results.SampledMediumCV,Variables.NoDataValue '
        'FROM Results,Variables,Units '
        'WHERE Results.ResultID=' + result_num + ' '
                                                 'AND Results.UnitsID = Units.UnitsID AND Results.VariableID = Variables.VariableID')
    var_unit = c.fetchall()
    for unit in var_unit:
        variable_name = unit[0]
        units = unit[1]
        samplemedium = unit[2]
        nodatavalue = unit[3]
    c.execute(
        'SELECT  TimeSeriesResults.IntendedTimeSpacing, Units.UnitsName,TimeSeriesResults.AggregationStatisticCV '
        'FROM TimeSeriesResults, Units '
        'WHERE TimeSeriesResults.ResultID =' + result_num + ' '
                                                            'AND TimeSeriesResults.IntendedTimeSpacingUnitsID = Units.UnitsID')
    time_support = c.fetchall()
    for time in time_support:
        timeunit = time[1]

        timesupport = time[0]
        datatype = time[2]
    c.execute(
        'SELECT Results.ResultID,Methods.MethodID,Methods.MethodName, SamplingFeatures.SamplingFeatureName,Actions.ActionTypeCV '
        'FROM Results,FeatureActions,Actions,Methods, SamplingFeatures ' +
        'WHERE Results.ResultID=' + result_num + ' '
                                                 'AND Results.FeatureActionID=FeatureActions.FeatureActionID ' +
        'AND ((FeatureActions.ActionID=Actions.ActionID '
        'AND Actions.MethodID=Methods.MethodID) OR(FeatureActions.SamplingFeatureID = SamplingFeatures.SamplingFeatureID)) ')
    methods = c.fetchall()  # Returns Result id method id and method description for each result
    # Quality Control
    c.execute(
        'SELECT ProcessingLevels.ProcessingLevelCode, ProcessingLevels.Explanation '
        'FROM Results, ProcessingLevels ' +
        'WHERE Results.ResultID=' + result_num + ' '
                                                 'AND Results.ProcessingLevelID = ProcessingLevels.ProcessingLevelID')
    qualityControl = c.fetchall()
    c.execute(
        'SELECT Organizations.OrganizationID,Organizations.OrganizationName,Organizations.OrganizationName '
        'FROM Organizations,Affiliations,ActionBy,Actions,FeatureActions,Results ' +
        'WHERE Results.ResultID=' + result_num + ' '
                                                 'AND Results.FeatureActionID=FeatureActions.FeatureActionID ' +
        'AND FeatureActions.ActionID=Actions.ActionID ' +
        'AND Actions.ActionID=ActionBy.ActionID ' +
        'AND ActionBy.AffiliationID = Affiliations.AffiliationID ' +
        'AND Affiliations.OrganizationID = Organizations.OrganizationID ')
    # c.execute('Select *')
    organizations = c.fetchall()
    for meth, qual, org in zip(methods, qualityControl, organizations):

        result_id = str(meth[0])
        m_code = meth[1]
        m_des = meth[2]
        site_name = meth[3]
        valuetype = meth[4]

        q_code = qual[0]
        q_des = qual[1]

        s_code = org[0]
        o_org = org[1]
        s_des = org[2]
        meta_dic['method'].update({m_code: m_des})

        meta_dic['quality_code'].update({q_code: q_code})
        meta_dic['quality'].update({q_code: q_des})

        meta_dic['source'].update({s_code: s_des})
        meta_dic['organization'].update({s_code: o_org})

        dic = str(q_code) + 'aa' + str(m_code) + 'aa' + str(s_code)
        # dic = dic.replace(" ","")
        if dic not in meth_qual:
            # meth_qual.append(dic)
            master_values.update({dic: []})
            master_times.update({dic: []})
            master_boxplot.update({dic: []})
            master_stat.update({dic: []})
            master_data_values.update({dic: []})

    c.execute(
        'SELECT ResultID,ValueDateTime,DataValue FROM TimeSeriesResultValues')
    data = c.fetchall()

    for ele in data:
        res_id = ele[0]
        if int(result_num) == res_id:
            v = ele[2]
            n = ele[1]
            n = ciso8601.parse_datetime(str(n))
            n = n.timetuple()
            n = mktime(n)
            # if v == nodata:
            if v == nodatavalue:
                v = None
            else:
                v = float(v)
                # records only none null values for running statistics
                master_data_values[dic].append(v)
            master_values[dic].append(v)
            master_times[dic].append(n)

    for item in master_data_values:
        if len(master_data_values[item]) == 0:
            mean = None
            median = None
            quar1 = None
            quar3 = None
            min1 = None
            max1 = None
        else:

            mean = numpy.mean(master_data_values[item])
            mean = float(format(mean, '.2f'))
            median = float(
                format(numpy.median(master_data_values[item]), '.2f'))
            quar1 = float(
                format(numpy.percentile(master_data_values[item], 25), '.2f'))
            quar3 = float(
                format(numpy.percentile(master_data_values[item], 75), '.2f'))
            min1 = float(format(min(master_data_values[item]), '.2f'))
            max1 = float(format(max(master_data_values[item]), '.2f'))

        master_stat[item].append(mean)
        master_stat[item].append(median)
        master_stat[item].append(max1)
        master_stat[item].append(min1)
        master_boxplot[item].append(1)
        master_boxplot[item].append(min1)  # adding data for the boxplot
        master_boxplot[item].append(quar1)
        master_boxplot[item].append(median)
        master_boxplot[item].append(quar3)
        master_boxplot[item].append(max1)

    conn.close()
    return {
        'site_name': site_name,
        'variable_name': variable_name,
        'units': units,
        'meta_dic': meta_dic,
        'organization': organization,
        'quality': quality,
        'method': method,
        'status': 'success',
        'datatype': datatype,
        'valuetype': valuetype,
        'samplemedium': samplemedium,
        'timeunit': timeunit,
        'sourcedescription': sourcedescription,
        'timesupport': timesupport,
        'master_counter': master_counter,
        'master_values': master_values,
        'master_times': master_times,
        'master_boxplot': master_boxplot,
        'master_stat': master_stat,
        'master_data_values': master_data_values
    }


def getOAuthHS(request):
    # hs_instance_name = "www"
    hs_instance_name = "beta"
    client_id = getattr(settings, "SOCIAL_AUTH_HYDROSHARE_KEY", None)
    client_secret = getattr(settings, "SOCIAL_AUTH_HYDROSHARE_SECRET", None)
    # this line will throw out from django.core.exceptions.ObjectDoesNotExist if current user is not signed in via HydroShare OAuth
    token = request.user.social_auth.get(provider='hydroshare').extra_data[
        'token_dict']
    hs_hostname = "{0}.hydroshare.org".format(hs_instance_name)
    auth = HydroShareAuthOAuth2(client_id, client_secret, token=token)
    hs = HydroShare(auth=auth, hostname=hs_hostname)
    return hs
