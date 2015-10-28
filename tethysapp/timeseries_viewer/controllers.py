from django.shortcuts import render
from utilities import *
from tethys_gizmos.gizmo_options import *
from owslib.wps import WebProcessingService
from owslib.wps import printInputOutput
from owslib.wps import monitorExecution
from owslib.wps import WPSExecution
#from tethys_apps.sdk import list_wps_service_engines
import xml.etree.ElementTree as ET
import sys
import requests
import csv
from datetime import datetime
import urllib2
from .model import engine, Base, URL
from hs_restclient import HydroShare, HydroShareAuthBasic
import dicttoxml
import ast
import zipfile
import tempfile
import StringIO

import urllib
import json
# -- coding: utf-8--

#Base_Url_HydroShare REST API
url_base='http://{0}.hydroshare.org/hsapi/resource/{1}/files/{2}'
##Call in Rest style
def restcall(request,branch,res_id,filename):
    print "restcall",branch,res_id,filename
    url_wml= url_base.format(branch,res_id,filename)
    response = urllib2.urlopen(url_wml)
    html = response.read()
    timeseries_plot = chartPara(html,filename)
    context = {"timeseries_plot":timeseries_plot}
    return render(request, 'timeseries_viewer/home.html', context)
#Normal Get or Post Request
#http://dev.hydroshare.org/hsapi/resource/72b1d67d415b4d949293b1e46d02367d/files/referencetimeseries-2_23_2015-wml_2_0.wml/


def home(request):
    name = None
    no_url = False
    number_ts = []#stores highcharts info of each time series
    Base.metadata.create_all(engine)
    url_list = []
    legend = []
    url_data_validation=[]
    show_hydroshare = False
    show_waterml = False
    show_cuahsi = False
    zip_bool = False
    timeseries_plot =None
    outside_input = False
    stat_data = OrderedDict()
    stat_data1 = []

    if request.GET and 'res_id' in request.GET and 'src' in request.GET:
        zip_string = ".zip"
        outside_input = True

        #unfinished support for zipped files
        if zip_string.find(request.GET['res_id']) != 0:
            zip_bool = True
            #url_zip = "http://localhost:8000/static/data_cart/waterml/"+request.GET['res_id']
            #filename_zip = file_unzipper(url_zip)
            #print "happy"
        if request.GET['src'] == "cuahsi":
            show_cuahsi = True
            zip_bool = True

        elif request.GET['src'] == "hydroshare":
            show_hydroshare = True

    if request.GET and 'res_id' in request.GET and 'src' in request.GET:
        outside_input = True
        if request.GET['src'] == "hydroshare":
            show_hydroshare = True
        elif request.GET['src']=='cuahsi':
            show_cuahsi =True
            outside_input = True
            zip_bool = True
            #Make a dictionary to hold the ids passed by CUAHSI
            cuahsi_resources = getCuahsiResourceIDs(request)

    if request.POST and 'hydroshare' in request.POST:
        show_hydroshare = True
    if request.POST and 'water_ml' in request.POST:
        show_waterml = True

    #new code for zip file
    if zip_bool == True:

        #fetch the zip file urls
        urls1 = []

        if urls1 != []:
            x=2
        else:
            # make temp directory for the zip files
            base_temp_dir = tempfile.tempdir
            temp_dir = os.path.join(base_temp_dir, "cuahsi")
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            for id in cuahsi_resources:
                url_zip = "http://bcc-hiswebclient.azurewebsites.net/CUAHSI/HydroClient/WaterOneFlowArchive/"+id+'/zip'
                r = requests.get(url_zip)
                try:
                    z = zipfile.ZipFile(StringIO.StringIO(r.content))
                    file_list = z.namelist()

                    try:
                        for file in file_list:

                            joe1 = z.read(file)

                            file_temp_name = temp_dir + '/' + id + '.xml'
                            print "unzipping file " + file_temp_name

                            file_temp = open(file_temp_name, 'wb')
                            file_temp.write(joe1)
                            file_temp.close()

                            print "unzipped file " + file_temp_name

                            #getting the URL of the zip file
                            base_url = request.build_absolute_uri()
                            if "?" in base_url:
                                base_url = base_url.split("?")[0]

                            zipped_url = base_url + "temp_waterml/cuahsi/" + id + '.xml'
                            print zipped_url

                            url2 = URL(url = zipped_url)

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


    # this block of code will add a time series to the legend and graph the result
    if (request.POST and "add_ts" in request.POST) or outside_input:
        if not outside_input:
            print "not"

        if request.POST.get('hydroshare_resource') != None and request.POST.get('hydroshare_file')!= None:
            try:
                #adding a hydroshare resource
                hs = HydroShare()
                hs_resource = request.POST['hydroshare_resource']
                hs_file = request.POST['hydroshare_file']
                url_hs_resource = "https://www.hydroshare.org/resource/"+hs_resource+"/data/contents/"+hs_file

                url1 = URL(url = url_hs_resource)

            except etree.XMLSyntaxError as e: #checks to see if data is an xml
                print "Error:Not XML"
                #quit("not valid xml")
            except ValueError, e: #checks to see if Url is valid
                print "Error:invalid Url"
            except TypeError, e: #checks to see if xml is formatted correctly
                print "Error:string indices must be integers not str"


        #adding data through cuashi or from a water ml url
        if show_cuahsi == True:

            cuahsi_resources = getCuahsiResourceIDs(request)
            for id in cuahsi_resources:

                try:
                    cuahsi_url = findZippedUrl(request, id)
                    print "opening " + cuahsi_url + "..."

                    response = urllib2.urlopen(cuahsi_url)

                    # zip file name
                    html = response.read()
                    graph_original = Original_Checker(html)
                    print 'original_checker completed!'

                    # get the statistics...
                    stat_function =  [graph_original['site_name'],"Mean", "Median", "Standard Deviation"]

                    stat_data1.append({'site_name': graph_original['site_name']})
                    stat_data1.append({'Mean': graph_original['mean']})
                    stat_data1.append({'Median': graph_original['median']})
                    stat_data1.append({'Standard Deviation': graph_original['stdev']})

                    for d in stat_data1:
                        stat_data.update(d)

                    number_ts.append({'name':graph_original['site_name'],'data':graph_original['for_highchart']})
                    legend.append(graph_original['site_name'])


                except etree.XMLSyntaxError as e: #checks to see if data is an xml
                    print "Error:Not XML"
                except ValueError, e: #checks to see if Url is valid
                    print "Error:invalid Url"
                except TypeError, e: #checks to see if xml is formatted correctly
                    print "Error:string indices must be integers not str"

            #finally plot the charts
            timeseries_plot = chartPara(graph_original,number_ts)


    if len(url_list) < 2:
        print "empty"
    else:
        for x in url_list:

            #graphs the original time series
            response = urllib2.urlopen(x)
            html = response.read()
            url_user = str(x)
            url_user = url_user.replace('=', '!')
            url_user = url_user.replace('&', '~')
            process_id = 'org.n52.wps.server.r.timeseries_viewer_stat'
            input = [("url",url_user)]
            output = "output"
            test_run = run_wps(process_id,input,output)

            graph_original = Original_Checker(html)

            download_link = test_run[1]
            string_download = ''.join(download_link)
            upload_hs = string_download
            #Takes the data fromt he time series and computes common statistics
            stat = test_run[0]
            split_stat = stat.split()
            split_stat1 = split_stat[1::2]
            split_stat1.insert(0,"")
            stat_function =  [graph_original['site_name'],"Mean", "Median", "Standard Deviation"]

            for i in range(0, len(stat_function)):
                stat_val = split_stat1[i]
                stat_fun = stat_function[i]
                stat_data1.append({stat_fun:stat_val})

            for d in stat_data1:
                stat_data.update(d)

            number_ts.append({'name':graph_original['site_name'],'data':graph_original['for_highchart']})
        timeseries_plot = chartPara(graph_original,number_ts)#plots graph data

    choices = {'joe1':'val1', 'key2':'val2'}
    text_input_options = TextInput(display_text='Enter URL of Water ML data and click "Add a Time Series"',
                                   name='url_name',
                                    )
    hydroshare_resource = TextInput(display_text='Enter Hydroshare Resouce ID',
                                   name='hydroshare_resource',
                                    )
    hydroshare_file = TextInput(display_text='Enter file name of Hydroshare Resource',
                                   name='hydroshare_file',
                                    )
    hydroshare = Button(display_text ="Upload Hydroshare Resource",
                        name ='hydroshare',
                        submit = True)
    water_ml = Button(display_text ="Upload water ml url",
                        name ='water_ml',
                        submit = True)
    add_ts = Button(display_text='Add a Time Series',
                       name='add_ts',
                       submit=True)
    clear_all_ts = Button(display_text='Clear all Time Series',
                       name='clear_all_ts',
                       submit=True)
    graph = Button(display_text='Graph Oringal Time Series',
                       name='graph',
                       submit=True)
    upload_hs = Button(display_text='Upload data to HydroShare',
                       name='upload_hs',
                       submit=True)
    stat_table = TableView(column_names=("Function","Value"),
                           rows = stat_data,
                           hover =True,
                           striped = False,
                           bordered = True,
                           condensed = True
                           )
    context = {
'timeseries_plot':timeseries_plot,
'text_input_options':text_input_options,
'name':name,
'stat_data':stat_data,
'stat_table':stat_table,
'no_url':no_url,
'add_ts':add_ts,
'clear_all_ts':clear_all_ts,
'graph':graph,
'legend':legend,
'hydroshare':hydroshare,
'show_hydroshare':show_hydroshare,
'hydroshare_file':hydroshare_file,
'hydroshare_resource':hydroshare_resource,
'water_ml':water_ml,
'show_waterml':show_waterml,
'upload_hs':upload_hs,
        "choices":choices
}
    
    return render(request, 'timeseries_viewer/home.html', context)

def run_wps(process_id,input,output):
    #choose the first wps engine
    my_engine = WebProcessingService('http://appsdev.hydroshare.org:8282/wps/WebProcessingService', verbose=False, skip_caps=True)
    my_engine.getcapabilities()
    my_process = my_engine.describeprocess(process_id)
    my_inputs = my_process.dataInputs
    input_names = [] #getting list of input
    for input1 in my_inputs:
        input_names.append(input1)
    #executing the process..
    execution = my_engine.execute(process_id, input, output)
    request = execution.request
    #set store executeresponse to false
    request = request.replace('storeExecuteResponse="true"', 'storeExecuteResponse="false"')
    url_wps = 'http://appsdev.hydroshare.org:8282/wps/WebProcessingService'
    wps_request = urllib2.Request(url_wps,request)
    wps_open = urllib2.urlopen(wps_request)
    wps_read = wps_open.read()
    if 'href' in wps_read:
        tag = 'href="'
        location = wps_read.find(tag)
        new= wps_read[location+len(tag):len(wps_read)]
        tag2 = '"/>\n    </wps:Output>\n  </wps:ProcessOutputs>\n</wps:'
        location2 = new.find(tag2)
        final = new[0:location2]
        split = final.split()
        wps_request1 = urllib2.Request(split[0])
        wps_open1 = urllib2.urlopen(wps_request1)
        wps_read1 = wps_open1.read()

    #return [final_output_url, final_data]
    return [wps_read1, split]


def read_final_data(url):
    r = requests.get(url)
    data = r.text
    reader = csv.reader(data.splitlines(), delimiter='\t')
    rows = []
    for row in reader:
        rows.append(row)
    return rows