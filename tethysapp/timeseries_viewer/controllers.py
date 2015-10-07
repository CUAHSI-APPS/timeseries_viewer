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
from .model import engine, SessionMaker, Base, URL,SessionMaker1,Base1,engine1
from hs_restclient import HydroShare, HydroShareAuthBasic
import dicttoxml
import ast
import zipfile
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
            url_zip = "http://localhost:8000/static/data_cart/waterml/"+request.GET['res_id']
            #filename_zip = file_unzipper(url_zip)
            #print "happy"
        if request.GET['src'] == "cuahsi":
            show_cuahsi = True

        elif request.GET['src'] == "hydroshare":
            show_hydroshare = True

    #zip file test

    # r = requests.get(url_zip)
    # z = zipfile.ZipFile(StringIO.StringIO(r.content))
    # file_list = z.namelist()
    #
    #
    # for  file in file_list[1:]:
    #     counter2 = counter2 +1
    #     joe1 = z.read(file)
    #     graph_original = Original_Checker(joe1)
    #     number_ts.append({'name':graph_original['site_name'],'data':graph_original['for_highchart']})
    #     timeseries_plot = chartPara(graph_original,number_ts)#plots graph data

    #end zip test

    if request.POST and 'hydroshare' in request.POST:
        show_hydroshare = True
    if request.POST and 'water_ml' in request.POST:
        show_waterml = True




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
                session = SessionMaker()
                url1 = URL(url = url_hs_resource)
                session.add(url1)
                session.commit()
                session.close()
            except etree.XMLSyntaxError as e: #checks to see if data is an xml
                print "Error:Not XML"
                #quit("not valid xml")
            except ValueError, e: #checks to see if Url is valid
                print "Error:invalid Url"
            except TypeError, e: #checks to see if xml is formatted correctly
                print "Error:string indices must be integers not str"
         #adding data through cuashi or from a water ml url
        if request.POST.get('url_name') != None or show_cuahsi == True:
            try:
                # if url_zip != None:
                #     print "zip"
                #     response = urllib2.urlopen(url_zip)

                if show_cuahsi:
                    cuahsi_url = 'http://appsdev.hydroshare.org/static/data_cart/waterml/' + request.GET['res_id']
                    response = urllib2.urlopen(cuahsi_url)
                    url1 = URL(url=cuahsi_url)

                else:
                    response = urllib2.urlopen(request.POST['url_name'])
                    url1 = URL(url = request.POST['url_name'])
                # zip file name
                html = response.read()
                graph_original = Original_Checker(html)
                url_data_validation.append(graph_original['site_name'])
                session = SessionMaker()
                session.add(url1)
                session.commit()
                session.close()
            except etree.XMLSyntaxError as e: #checks to see if data is an xml
                print "Error:Not XML"
            except ValueError, e: #checks to see if Url is valid
                print "Error:invalid Url"
            except TypeError, e: #checks to see if xml is formatted correctly
                print "Error:string indices must be integers not str"



    session = SessionMaker()
    urls = session.query(URL).all()
    for url in urls:#creates a list of timeseries data and displays the results in the legend
            url_list.append(url.url)
            response = urllib2.urlopen(url.url)
            html = response.read()
            graph_original1 = Original_Checker(html)
            legend.append(graph_original1['site_name'])
    session.close()


    if request.POST and "clear_all_ts" in request.POST:
        session = SessionMaker()
        urls = session.query(URL).all()
        for url in urls:
             session.delete(url)
             session.commit()
        session.close()
        legend = None
        url_list =[]


    if len(url_list) ==0:
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