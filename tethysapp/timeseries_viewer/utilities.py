from lxml import etree
import numpy
import requests
import time
from datetime import timedelta
from dateutil import parser
from django.http import HttpResponse
import urllib2
import urllib
from .app import TimeSeriesViewer
import csv
import zipfile
import StringIO
import time
import zipfile
import os
import dateutil.parser
from datetime import datetime
import pandas as pd
from hs_restclient import HydroShare
import controllers
import operator
import collections
import json
from suds.transport import TransportError
from suds.client import Client
from xml.sax._exceptions import SAXParseException
import requests
import codecs

def get_app_base_uri(request):
    base_url = request.build_absolute_uri()
    if "?" in base_url:
        base_url = base_url.split("?")[0]
    return base_url

def get_workspace():
    return TimeSeriesViewer.get_app_workspace().path

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

def parse_1_0_and_1_1(root,id_qms):
    root_tag = root.tag.lower()
    boxplot = []
    master_values=collections.OrderedDict()
    master_times = collections.OrderedDict()
    master_boxplot = collections.OrderedDict()
    master_stat = collections.OrderedDict()
    master_data_values = collections.OrderedDict()
    meth_qual = [] # List of all the quality, method, and source combinations
    for_canvas = []
    meta_dic ={'method':{},'quality':{},'source':{},'organization':{},'quality_code':{}}
    m_des = None
    m_code = None
    m_org =None
    x_value = []
    y_value = []
    master_counter =True
    nodata = "-9999"  # default NoData value. The actual NoData value is read from the XML noDataValue tag
    timeunit=None
    sourcedescription = None
    timesupport =None
    units, site_name, variable_name,quality,method,organization = None, None, None, None, None, None
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
                    bracket_lock = element.tag.index('}')  # The namespace in the tag is enclosed in {}.
                    tag = element.tag[bracket_lock+1:]     # Takes only actual tag, no namespace

                    if 'value'!= tag:
                        # in the xml there is a unit for the value, then for time. just take the first
                        if 'unitName' == tag or 'units' ==tag or 'UnitName'==tag or 'unitCode'==tag:
                            if not unit_is_set:
                                units = element.text
                                unit_is_set = True
                        if 'noDataValue' == tag:
                            nodata = element.text
                        if 'siteName' == tag:
                            site_name = element.text
                        if 'variableName' == tag:
                            variable_name = element.text
                        if 'organization'==tag or 'Organization'==tag or'siteCode'==tag:
                            try:
                                organization = element.attrib['agencyCode']
                            except:
                                organization = element.text
                        if 'definition' == tag or 'qualifierDescription'==tag:
                            quality = element.text
                        if 'methodDescription' == tag or 'MethodDescription'==tag:
                            # print element.attrib['methodID']
                            method = element.text
                        if 'dataType' == tag :
                            datatype = element.text
                        if 'valueType' == tag:
                            valuetype = element.text
                        if "sampleMedium" == tag:
                            samplemedium = element.text
                        if "timeSupport"== tag or"timeInterval" ==tag:
                            timesupport =element.text
                        if"unitName"== tag or "UnitName"==tag:
                            timeunit =element.text
                        if"sourceDescription"== tag or "SourceDescription"==tag:
                            sourcedescription =element.text
                        if "method" ==tag.lower():
                            try:
                                mid = element.attrib['methodID']
                            except:
                                mid =None
                                m_code =''
                            for subele in element:
                                if 'methodcode' in subele.tag.lower() and m_code=='':
                                    m_code = subele.text
                                    m_code = m_code.replace(" ","")

                                if mid != None:
                                    m_code = element.attrib['methodID']
                                    m_code = m_code.replace(" ","")
                                if 'methoddescription' in subele.tag.lower():
                                    m_des = subele.text

                            meta_dic['method'].update({m_code:m_des})
                        if "source" ==tag.lower():

                            try:
                                sid = element.attrib['sourceID']
                            except:
                                sid = None
                                m_code =''

                            for subele in element:
                                if 'sourcecode' in subele.tag.lower() and m_code =='':
                                    m_code = subele.text
                                    m_code = m_code.replace(" ","")
                                if sid!= None:
                                    m_code = element.attrib['sourceID']
                                    m_code = m_code.replace(" ","")
                                if 'sourcedescription' in subele.tag.lower():
                                    m_des = subele.text
                                if 'organization' in subele.tag.lower():
                                    m_org = subele.text
                            meta_dic['source'].update({m_code:m_des})
                            meta_dic['organization'].update({m_code:m_org})
                        if "qualitycontrollevel" ==tag.lower():
                            try:
                                qlc= element.attrib['qualityControlLevelID']
                            except:
                                qlc =None
                                m_code =''
                            for subele in element:
                                if  qlc !=None:
                                    m_code =element.attrib['qualityControlLevelID']
                                    m_code = m_code.replace(" ","")
                                if 'qualitycontrollevelcode' in subele.tag.lower():
                                    m_code1 = subele.text
                                    m_code1 = m_code1.replace(" ","")
                                if 'qualitycontrollevelcode' in subele.tag.lower() and m_code =='':
                                    m_code = subele.text
                                    m_code = m_code1.replace(" ","")
                                if 'definition' in subele.tag.lower():
                                    m_des = subele.text
                            meta_dic['quality'].update({m_code:m_des})
                            meta_dic['quality_code'].update({m_code1:m_code})
                        # print meta_dic
                    elif 'value' == tag:
                        try:
                            n = element.attrib['dateTimeUTC']
                        except:
                            n =element.attrib['dateTime']
                        try:
                            quality= element.attrib['qualityControlLevelCode']
                        except:
                            quality =''
                        try:
                            quality1 = element.attrib['qualityControlLevel']
                        except:
                            quality1 =''
                        if quality =='' and quality1 != '':
                            quality = quality1
                        try:
                            method = element.attrib['methodCode']
                        except:
                            method=''
                        try:
                            method1 = element.attrib['methodID']
                        except:
                            method1=''
                        if method =='' and method1 != '':
                                method = method1
                        try:
                            source = element.attrib['sourceCode']
                        except:
                            source=''
                        try:
                            source1 = element.attrib['sourceID']
                        except:
                            source1=''
                        if source =='' and source1 != '':
                            source = source1
                        dic = quality +'aa'+method+'aa'+source
                        dic = dic.replace(" ","")


                        if dic not in meth_qual:

                            meth_qual.append(dic)
                            master_values.update({dic:[]})
                            master_times.update({dic:[]})
                            master_boxplot.update({dic:[]})
                            master_stat.update({dic:[]})
                            master_data_values.update({dic:[]})

                        v = element.text
                        if v == nodata:
                            value = None
                            x_value.append(n)
                            y_value.append(value)
                            v =None

                        else:
                            v = float(element.text)
                            x_value.append(n)
                            y_value.append(v)
                            master_data_values[dic].append(v) #records only none null values for running statistics
                        master_values[dic].append(v)
                        master_times[dic].append(n)
            for item in master_data_values:
                if len(master_data_values[item]) ==0:
                    mean = None
                    median =None
                    quar1 = None
                    quar3 = None
                    min1 = None
                    max1=None
                else:
                    mean = numpy.mean(master_data_values[item])
                    mean = float(format(mean, '.2f'))
                    median = float(format(numpy.median(master_data_values[item]), '.2f'))
                    quar1 = float(format(numpy.percentile(master_data_values[item],25), '.2f'))
                    quar3 = float(format(numpy.percentile(master_data_values[item],75), '.2f'))
                    min1 = float(format(min(master_data_values[item]), '.2f'))
                    max1 = float(format(max(master_data_values[item]), '.2f'))
                master_stat[item].append(mean)
                master_stat[item].append(median)
                master_stat[item].append(max1)
                master_stat[item].append(min1)
                master_boxplot[item].append(1)
                master_boxplot[item].append(min1)#adding data for the boxplot
                master_boxplot[item].append(quar1)
                master_boxplot[item].append(median)
                master_boxplot[item].append(quar3)
                master_boxplot[item].append(max1)
            return {
                'site_name': site_name,
                'variable_name': variable_name,
                'units': units,
                'meta_dic':meta_dic,
                'for_canvas':for_canvas,
                'organization': organization,
                'quality': quality,
                'method': method,
                'status': 'success',
                'datatype' :datatype,
                'valuetype' :valuetype,
                'samplemedium':samplemedium,
                'timeunit':timeunit,
                'sourcedescription' :sourcedescription,
                'timesupport' : timesupport,
                'master_counter':master_counter,
                'boxplot':boxplot,
                'master_values':master_values,
                'master_times':master_times,
                'master_boxplot':master_boxplot,
                'master_stat':master_stat
            }
        else:
            parse_error = "Parsing error: The WaterML document doesn't appear to be a WaterML 1.0/1.1 time series"
            error_report("Parsing error: The WaterML document doesn't appear to be a WaterML 1.0/1.1 time series")
            print parse_error
            return {
                'status': parse_error
            }
    except Exception, e:
        data_error = "Parsing error: The Data in the Url, or in the request, was not correctly formatted for water ml 1."
        error_report("Parsing error: The Data in the Url, or in the request, was not correctly formatted.")
        print data_error
        print e
        return {
            'status': data_error
        }

def parse_2_0(root):#waterml 2 has not been implemented in the viewer at this time
    print "running parse_2"
    root_tag = root.tag.lower()
    boxplot = []
    master_values=collections.OrderedDict()
    master_times = collections.OrderedDict()
    master_boxplot = collections.OrderedDict()
    master_stat = collections.OrderedDict()
    master_data_values = collections.OrderedDict()
    meth_qual = [] # List of all the quality, method, and source combinations
    for_canvas = []
    meta_dic ={'method':{},'quality':{},'source':{},'organization':{},'quality_code':{}}
    m_des = None
    m_code = None
    m_org =None
    x_value = []
    y_value = []
    master_counter =True
    nodata = "-9999"  # default NoData value. The actual NoData value is read from the XML noDataValue tag
    timeunit=None
    sourcedescription = None
    timesupport =None
    # metadata items
    units, site_name, variable_name,quality,method, organization = None, None, None, None, None, None
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
                                n =element.attrib['dateTime']
                            try:
                                quality= element.attrib['qualityControlLevelCode']
                            except:
                                quality1 =''
                            try:
                                method = element.attrib['methodCode']
                            except:
                                method=''
                            try:
                                source = element.attrib['sourceCode']
                            except:
                                source=''
                            dic = quality +'aa'+method+'aa'+source
                            if dic not in meth_qual:
                                meth_qual.append(dic)
                                master_values.update({dic:[]})
                                master_times.update({dic:[]})
                                master_boxplot.update({dic:[]})
                                master_stat.update({dic:[]})
                                master_data_values.update({dic:[]})

                            v = element.text
                            if v == nodata:
                                value = None
                                x_value.append(n)
                                y_value.append(value)
                                v =None

                            else:
                                v = float(element.text)
                                x_value.append(n)
                                y_value.append(v)
                                master_data_values[dic].append(v) #records only none null values for running statistics
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
                                    method=e.attrib[a]

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
                if"timeSupport"in element.text:
                    timesupport =element.text
                if"unitName"in element.text:
                    timeunit =element.text
                if"sourceDescription"in element.text:
                    sourcedescription =element.text

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
            for v in list(values.vals()):
                if v < smallest_value:
                    smallest_value = t




            return {'time_series': ts,
                    'site_name': site_name,
                    'start_date': smallest_time,
                    'end_date':largest_time,
                    'variable_name': variable_name,
                    'units': units,
                    'values': values,
                    'wml_version': '2.0',
                    'latitude': latitude,
                    'longitude': longitude,
                    'for_highchart': for_highchart,
                    'organization':organization,
                    'quality':quality,
                    'method':method,
                    'status': 'success',
                    'datatype' :datatype,
                    'valuetype' :valuetype,
                    'samplemedium':samplemedium,
                    'smallest_value':smallest_value,
                    'timeunit':timeunit,
                    'sourcedescription' :sourcedescription,
                    'timesupport' : timesupport,
                    'values':vals
                    }
        else:
            print "Parsing error: The waterml document doesn't appear to be a WaterML 2.0 time series"
            error_report("Parsing error: The waterml document doesn't appear to be a WaterML 2.0 time series")
            return "Parsing error: The waterml document doesn't appear to be a WaterML 2.0 time series"
    except:
        print "Parsing error: The Data in the Url, or in the request, was not correctly formatted."
        error_report("Parsing error: The Data in the Url, or in the request, was not correctly formatted.")
        return "Parsing error: The Data in the Url, or in the request, was not correctly formatted."



def Original_Checker(xml_file,id_qms):

    print xml_file
    try:
        tree = etree.parse(xml_file)
        root = tree.getroot()
        wml_version = get_version(root)

        if wml_version == '1':

            return parse_1_0_and_1_1(root,id_qms)

        elif wml_version == '2.0':
            return parse_2_0(root)
    except ValueError, e:
        error_report("xml parse error")
        return read_error_file(xml_file)
    except:
        error_report("xml parse error")
        return read_error_file(xml_file)

def read_error_file(xml_file):
    try:
        f = open(xml_file)
        return {'status': f.readline()}
    except:
        error_report('invalid WaterML file')
        return {'status': 'invalid WaterML file'}

def unzip_waterml(request, res_id,src,res_id2,xml_id):
        print src
        file_number=0
        temp_dir = get_workspace()
        file_data =None
        # get the URL of the remote zipped WaterML resource
        if not os.path.exists(temp_dir+"/id"):
            os.makedirs(temp_dir+"/id")
        if 'cuahsi'in src :
            url_zip = 'http://qa-webclient-solr.azurewebsites.net/CUAHSI/HydroClient/WaterOneFlowArchive/'+res_id+'/zip'
        elif 'hydroshare' in src:
            if controllers.use_hs_client_helper:
                hs = controllers.get_oauth_hs(request)
            else:
                hs = controllers.getOAuthHS(request)
            file_path = get_workspace() + '/id'
            hs.getResource(res_id, destination=file_path, unzip=True)
            root_dir = file_path + '/' + res_id
            data_dir = root_dir + '/' + res_id + '/data/contents/'
            for subdir, dirs, files in os.walk(data_dir):
                for file in files:
                    if  'wml_1_' in file:
                        data_file = data_dir + file
                        with open(data_file, 'r') as f:
                            # print f.read()
                            file_data = f.read()
                            f.close()
                            file_temp_name = temp_dir + '/id/' + res_id + '.xml'
                            file_temp = open(file_temp_name, 'wb')
                            file_temp.write(file_data)
                            file_temp.close()
                    if '.json.refts' in file:
                        data_file = data_dir +file
                        with open(data_file, 'r') as f:
                            file_data = f.read()

                            file_number = parse_ts_layer(file_data)
        elif "xmlrest" in src:

            url_zip = res_id2
            res = urllib.unquote(res_id2).decode()
            r = requests.get(res, verify=False)

            file_data = r.content
            print file_data
            file_temp_name = temp_dir + '/id/'+xml_id+'.xml'
            file_temp = open(file_temp_name, 'wb')
            file_temp.write(file_data)
            file_temp.close()
        else:
            url_zip = 'http://' + request.META['HTTP_HOST'] + '/apps/data-cart/showfile/'+res_id


        if src != 'hydroshare_generic' and src != 'xmlrest' and src !='hydroshare':
            try:
                r = requests.get(url_zip, verify=False)
                z = zipfile.ZipFile(StringIO.StringIO(r.content))
                file_list = z.namelist()
                try:
                    for file in file_list:
                        if 'hydroshare' in src:
                            if 'wml_1_' in file:
                                file_data = z.read(file)
                                file_temp_name = temp_dir + '/id/' + res_id + '.xml'
                                file_temp = open(file_temp_name, 'wb')
                                file_temp.write(file_data)
                                file_temp.close()
                        else:
                            file_data = z.read(file)
                            file_temp_name = temp_dir + '/id/' + res_id + '.xml'
                            file_temp = open(file_temp_name, 'wb')
                            file_temp.write(file_data)
                            file_temp.close()
                # error handling

                # checks to see if data is an xml
                except etree.XMLSyntaxError as e:
                    print "Error:Not XML"
                    error_report("Error:Not XML")
                    return False

                # checks to see if Url is valid
                except ValueError, e:
                    error_report("Error:invalid Url")
                    print "Error:invalid Url"
                    return False

                # checks to see if xml is formatted correctly
                except TypeError, e:
                    error_report("Error:string indices must be integers not str")
                    print "Error:string indices must be integers not str"
                    return False

            # check if the zip file is valid
            except zipfile.BadZipfile as e:
                    error_message = "Bad Zip File"
                    error_report(error_message)
                    print "Bad Zip file"
        return file_number
# finds the waterML file path in the workspace folder
def waterml_file_path(res_id,xml_rest,xml_id):
    base_path = get_workspace()
    if xml_rest == True:
        file_path = base_path + "/id/"+xml_id #+ res_id
    else:
        file_path = base_path + "/id/"+ res_id
    if not file_path.endswith('.xml'):
        file_path += '.xml'
    return file_path

def error_report(text):
    temp_dir = get_workspace()
    temp_dir = temp_dir[:-24]
    file_temp_name = temp_dir + '/error_report.txt'
    file_temp = open(file_temp_name, 'a')
    time = datetime.now()
    time2 = time.strftime('%Y-%m-%d %H:%M')
    file_temp.write(time2+": "+text+"\n")
    file_temp.close()
def viewer_counter(request):
    temp_dir = get_workspace()
    try:


        if controllers.use_hs_client_helper:
            hs = controllers.get_oauth_hs(request)
        else:
            hs = controllers.getOAuthHS(request)

        user =  hs.getUserInfo()
        user1 = user['username']
    except:
        user1 =""
    if user1 != 'mbayles2':
        temp_dir = temp_dir[:-24]
        file_temp_name = temp_dir + '/view_counter.txt'
        if not os.path.exists(temp_dir+"/view_counter.txt"):
            file_temp = open(file_temp_name, 'a')
            first = '1'
            file_temp.write(first)
            file_temp.close()
        else:
            file_temp = open(file_temp_name, 'r+')
            content = file_temp.read()
            number = int(content)
            number  = number +1
            number  = str(number)
            file_temp.seek(0)
            file_temp.write(number)
            file_temp.close()
    else:
        user1=''
def parse_ts_layer(data):
    counter = 0
    print type(data)
    data = data.encode(encoding ='UTF-8')
    json_data = json.loads(data)
    print type(json_data)
    # print json_data
    json_data = json.loads(json_data['timeSeriesLayerResource'])
    layer = json_data['REFTS']
    for sub in layer:
        ref_type= sub['refType']
        service_type = sub['serviceType']
        url =sub['url']
        site_code = sub['siteCode']
        variable_code = sub['variableCode']
        start_date = sub['beginDate']
        end_date = sub['endDate']

        if ref_type =='WOF':
            if service_type =='SOAP':
                print url
                print site_code
                print variable_code
                print start_date
                print end_date
                # print client
                # site_code = 'NWISUV:10164500'
                # variable_code = 'NWISUV:00060'
                # start_date ='2016-06-03T00:00:00+00:00'
                # end_date = '2016-10-26T00:00:00+00:00'
                auth_token = ''
                client = connect_wsdl_url(url)
                # response1 = client.service.GetSiteInfo('NWISDV:10147100')
                response1 = client.service.GetValues(site_code, variable_code, start_date, end_date)

                temp_dir = get_workspace()
                file_path = temp_dir + '/id/' + 'timeserieslayer'+str(counter) + '.xml'
                response1 = response1.encode('utf-8')
                # response1 = unicode(response1.strip(codecs.BOM_UTF8), 'utf-8')
                with open(file_path, 'w') as outfile:
                    outfile.write(response1)

                # print client.service
                print "done"
            if(service_type=='REST'):
                waterml_url = url+'/GetValueObject'
                response = urllib2.urlopen(waterml_url)
                html = response.read()
            counter = counter +1

    return counter
def connect_wsdl_url(wsdl_url):
    try:
        client = Client(wsdl_url)
    except TransportError:
        raise Exception('Url not found')
    except ValueError:
        raise Exception('Invalid url')  # ought to be a 400, but no page implemented for that
    except SAXParseException:
        raise Exception("The correct url format ends in '.asmx?WSDL'.")
    except:
        raise Exception("Unexpected error")
    return client