from django.shortcuts import render
from utilities import *
from tethys_gizmos.gizmo_options import *
from owslib.wps import WebProcessingService
from owslib.wps import printInputOutput
from owslib.wps import monitorExecution
from owslib.wps import WPSExecution
from tethys_apps.sdk import list_wps_service_engines
import xml.etree.ElementTree as ET
import sys
import requests
import csv
from datetime import datetime
import urllib2
from .model import engine, SessionMaker, Base, URL,rscript,SessionMaker1,Base1,engine1
from hs_restclient import HydroShare, HydroShareAuthBasic
import dicttoxml
import ast

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
    return render(request, 'ts_converter/home.html', context)
#Normal Get or Post Request
#http://dev.hydroshare.org/hsapi/resource/72b1d67d415b4d949293b1e46d02367d/files/referencetimeseries-2_23_2015-wml_2_0.wml/
def View_R_Code(request):
    context = View_R()
    return render(request, 'ts_converter/View_R_Code.html', context)

def home(request):
    url_wml=None
    name = None
    show_time = False
    no_url = False
    output_converter = None
    number_ts = []#stores highcharts info of each time series
    Base.metadata.create_all(engine)
    url_list = []
    plot = None
    counter = 0
    r_script = None
    script_test =[]
    legend = []
    download_bool = False
    string_download = None
    url_data_validation=[]
    Current_r = "Select an R script"
    show_hydroshare = False
    show_waterml = False

    if request.POST and 'hydroshare' in request.POST:
        show_hydroshare = True
    if request.POST and 'water_ml' in request.POST:
        show_waterml = True


    #test for downloading hydroshare
    # hs = HydroShare()
    # name =hs.getResourceFile("b29ac5ce06914752aaac74685ba0f682","DemoReferencedTimeSeries-wml_1.xml")
    # jim =[]
    # for thing in name:
    #     jim.append(thing)
    # xml = ''.join(jim)

    # response = urllib2.urlopen("https://www.hydroshare.org/resource/b29ac5ce06914752aaac74685ba0f682/data/contents/DemoReferencedTimeSeries-wml_2_0.xml")
    # html = response.read()
    # graph_original = Original_Checker(html)# this is the common element between hydroshare resource and water ml url
    # number_ts.append({'name':graph_original['site_name'],'data':graph_original['for_highchart']})
    # plot = chartPara(graph_original,number_ts)#plots graph data


















    if request.POST:
        Current_r = request.POST['select_r_script']

    if request.POST and "hydroshare_resource" in request.POST and "hydroshare_file" in request.POST:
        resouce = request.POST['hydroshare_resource']
        file = request.POST['hydroshare_file']

    if request.POST and "add_ts" in request.POST:
        Current_r = request.POST['select_r_script']
        if request.POST.get('hydroshare_resource') != None and request.POST.get('hydroshare_file')!= None:
            try:
                hs = HydroShare()
                hs_resource = request.POST['hydroshare_resource']
                hs_file = request.POST['hydroshare_file']

                #hs_text =hs.getResourceFile("b29ac5ce06914752aaac74685ba0f682","DemoReferencedTimeSeries-wml_1.xml")
                hs_text =hs.getResourceFile(hs_resource,hs_file)
                # hs_lst =[] This was an old methond to extract the data from the resource. Probably obsolete
                # for line in hs_text:
                #     hs_lst.append(line)
                # xml = ''.join(hs_lst)
                url_hs_resource = "https://www.hydroshare.org/resource/"+hs_resource+"/data/contents/"+hs_file
                #graph_original = Original_Checker(xml)
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
        if request.POST.get('url_name') != None:
            try:
                response = urllib2.urlopen(request.POST['url_name'])
                html = response.read()
                graph_original = Original_Checker(html)
                url_data_validation.append(graph_original['site_name'])
                session = SessionMaker()
                #url1 = URL(url = str(graph_original)) changed before trip
                url1 = URL(url = request.POST['url_name'])
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

    session = SessionMaker()
    urls = session.query(URL).all()
    for url in urls:#creates a list of timeseries data and displays the results in the legend
            url_list.append(url.url)
            response = urllib2.urlopen(url.url)
            html = response.read()
            #graph_original = url.url
            #graph_original1 = ast.literal_eval(graph_original)#this displays the whole document
            graph_original1 = Original_Checker(html)
            legend.append(graph_original1['site_name'])
            #yay = "ii"
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
        Current_r = request.POST['select_r_script']

    if len(url_list) ==0:
        print "empty"
    else:
        for x in url_list:
            counter = counter +1#counter for testing
            #graphs the original time series
            response = urllib2.urlopen(x)
            html = response.read()
            graph_original = Original_Checker(html)
            number_ts.append({'name':graph_original['site_name'],'data':graph_original['for_highchart']})
        plot = chartPara(graph_original,number_ts)#plots graph data

    # if request.POST and "graph" in request.POST:
    #     for x in url_list:
    #         counter = counter +1#counter for testing
    #         #graphs the original time series
    #         url_wml = x
    #         response = urllib2.urlopen(url_wml)
    #         html = response.read()
    #         graph_original = Original_Checker(html)
    #         number_ts.append({'name':graph_original['site_name'],'data':graph_original['for_highchart']})
    #     plot = chartPara(graph_original,number_ts)#plots graph data
    #     Current_r = request.POST['select_r_script']

    if request.POST and "select_r" in request.POST:
        session = SessionMaker1()
        script1 = session.query(rscript).all()
        for script in script1:
            session.delete(script)
            session.commit()
        script = rscript(rscript = request.POST['select_r_script'])
        session.add(script)
        session.commit()
        session.close()
        r = View_R()
        r1 = r['r_code']
        #code to locate the inputs of the r script
        test1 = "wps.in"
        Current_r = request.POST['select_r_script']
        for m in re.finditer(test1,r1):
            print m
            counter = counter+1


    if request.POST and "run" in request.POST:
        download_bool = True
        display_r=[]

        session = SessionMaker1()
        script1 = session.query(rscript).all()
        for script in script1:
            display_r.append(script.rscript)
        Current_r = display_r[0]
        #this is the default chart if no values are given
        if url_list is None:
            filename = 'KiWIS-WML2-Example.wml'
            url_wml='http://hydrodata.info/chmi-h/cuahsi_1_1.asmx/GetValuesObject?location=CHMI-H:140&variable=CHMI-H:TEPLOTA&startDate=2015-07-01&endDate=2015-07-10&authToken='
            no_url = True
            response = urllib2.urlopen(url_wml)
            html = response.read()
            graph_info = Original_Checker(html)
            number_ts1 = [{'name':"timeseries1", 'data':graph_info['for_highchart']}]
            plot = chartPara(graph_info,number_ts1)
        # Plotting the altered time series
        else:
            for x in url_list:
                counter = counter +1#counter for testing
                #graphs the original time series
                response = urllib2.urlopen(x)
                html = response.read()
                graph_original = Original_Checker(html)
                #number_ts.append({'name':graph_original['site_name'],'data':graph_original['for_highchart']})
                url_user = str(x)
                url_user = url_user.replace('=', '!')
                url_user = url_user.replace('&', '~')
                if Current_r == "Time Series Converter":
                    interval = str(request.POST['select_interval'])
                    stat = str(request.POST['select_stat'])
                    process_id = 'org.n52.wps.server.r.timeSeriesConverter2'
                    input = [("url",url_user),("interval",interval),("stat",stat)]
                    output = "output"
                    #process_input = '<?xml+version="1.0"+encoding="UTF-8"+standalone="yes"?><wps:Execute+service="WPS"+version="1.0.0"++xmlns:wps="http://www.opengis.net/wps/1.0.0"+xmlns:ows="http://www.opengis.net/ows/1.1"++xmlns:xlink="http://www.w3.org/1999/xlink"+xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"++xsi:schemaLocation="http://www.opengis.net/wps/1.0.0++http://schemas.opengis.net/wps/1.0.0/wpsExecute_request.xsd">++<ows:Identifier>org.n52.wps.server.r.convert-time-series</ows:Identifier>++<wps:DataInputs>++++<wps:Input>++++++<ows:Identifier>url</ows:Identifier>++++++<wps:Data>++++++++<wps:LiteralData>'+url_user+'</wps:LiteralData>++++++</wps:Data>++++</wps:Input>++++<wps:Input>++++++<ows:Identifier>interval</ows:Identifier>++++++<wps:Data>++++++++<wps:LiteralData>'+interval+'</wps:LiteralData>++++++</wps:Data>++++</wps:Input>++++<wps:Input>++++++<ows:Identifier>stat</ows:Identifier>++++++<wps:Data>++++++++<wps:LiteralData>'+stat+'</wps:LiteralData>++++++</wps:Data>++++</wps:Input>++</wps:DataInputs>++<wps:ResponseForm>++++<wps:ResponseDocument+storeExecuteResponse="false">++++++<wps:Output+asReference="false">++++++++<ows:Identifier>output</ows:Identifier>++++++</wps:Output>++++</wps:ResponseDocument>++</wps:ResponseForm></wps:Execute>'
                elif Current_r =="Gap Filler":
                   process_id = 'org.n52.wps.server.r.timeSeriesGapFiller'
                   input = [("url",url_user)]
                   output = "output"
                   #process_input = '<?xml+version="1.0"+encoding="UTF-8"+standalone="yes"?><wps:Execute+service="WPS"+version="1.0.0"++xmlns:wps="http://www.opengis.net/wps/1.0.0"+xmlns:ows="http://www.opengis.net/ows/1.1"++xmlns:xlink="http://www.w3.org/1999/xlink"+xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"++xsi:schemaLocation="http://www.opengis.net/wps/1.0.0++http://schemas.opengis.net/wps/1.0.0/wpsExecute_request.xsd">++<ows:Identifier>org.n52.wps.server.r.timeSeriesGapFiller</ows:Identifier>++<wps:DataInputs>++++<wps:Input>++++++<ows:Identifier>url</ows:Identifier>++++++<wps:Data>++++++++<wps:LiteralData>'+url_user+'</wps:LiteralData>++++++</wps:Data>++++</wps:Input>++</wps:DataInputs>++<wps:ResponseForm>++++<wps:ResponseDocument+storeExecuteResponse="false">++++++<wps:Output+asReference="false">++++++++<ows:Identifier>output</ows:Identifier>++++++</wps:Output>++++</wps:ResponseDocument>++</wps:ResponseForm></wps:Execute>'
                #graphs the new time series
                #wps_request = urllib2.Request(url_wps,process_input)
                #wps_open = urllib2.urlopen(wps_request)
                #wps_read = wps_open.read()
                #graph_info =TimeSeriesConverter(wps_read)#prepares data for graphing
                test_run = run_wps(process_id,input,output)
                download_link = test_run[1]
                string_download = ''.join(download_link)
                upload_hs = string_download
                graph_info =TimeSeriesConverter(test_run[0])#prepares data for graphing
                number_ts.append({'name':graph_original['site_name']+' Convertered','data':graph_info['for_highchart']})
                legend.append(graph_original['site_name']+' Convertered')
            plot = chartPara(graph_original,number_ts)#plots graph data


    text_input_options = TextInput(display_text='Enter URL of Water ML data and click "Add a Time Series"',
                                   name='url_name',
                                    )
    hydroshare_resource = TextInput(display_text='Enter Hydroshare Resouce ID',
                                   name='hydroshare_resource',
                                    )
    hydroshare_file = TextInput(display_text='Enter file name of Hydroshare Resource',
                                   name='hydroshare_file',
                                    )
    select_interval = SelectInput(display_text='Select a new time frame',
                            name='select_interval',
                            multiple=False,
                            options=[('Select a new interval', 'default'),('Daily', 'daily'),('Weekly','weekly'), ('Monthly', 'monthly'), ('Yearly','yearly')],
                            original=['Two'])
    select_stat = SelectInput(display_text='Select a statistics function',
                            name='select_stat',
                            multiple=False,
                            options=[('Select a statistics function', 'no_select'),('Mean', 'mean'), ('Median','median')],
                            original=['Two'])
    select_r_script = SelectInput(display_text='Select a R Script',
                            name='select_r_script',
                            multiple=False,
                            options=[("Select an R script", "Select an R script"),('Time Series Converter', 'Time Series Converter'), ('Gap Filler','Gap Filler')],
                            original=['Two'])
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
    run = Button(display_text='Run Script',
                       name='run',
                       submit=True)
    download = Button(display_text='Download CSV',
                       name='download',
                       submit=True)
    graph = Button(display_text='Graph Oringal Time Series',
                       name='graph',
                       submit=True)
    select_r = Button(display_text='Select R Script',
                       name='select_r',
                       submit=True)

    upload_hs = Button(display_text='Upload data to HydroShare',
                       name='upload_hs',
                       submit=True)
    context = {
'plot':plot,
'text_input_options':text_input_options,
'name':name,
'select_interval': select_interval,
'select_stat':select_stat,
'select_r_script':select_r_script,
'show_time':show_time,
'no_url':no_url,
'output_converter':output_converter,
'add_ts':add_ts,
'run':run,
'clear_all_ts':clear_all_ts,
'graph':graph,
'legend':legend,
'select_r':select_r,
'string_download':string_download,
'download_bool':download_bool,
'Current_r': Current_r,
'hydroshare':hydroshare,
'show_hydroshare':show_hydroshare,
'hydroshare_file':hydroshare_file,
'hydroshare_resource':hydroshare_resource,
'water_ml':water_ml,
'show_waterml':show_waterml,
'upload_hs':upload_hs



}
    
    return render(request, 'ts_converter/home.html', context)

def run_wps(process_id,input,output):

    #choose the first wps engine
    my_engine = WebProcessingService('http://appsdev.hydroshare.org:8282/wps/WebProcessingService', verbose=False, skip_caps=True)
    my_engine.getcapabilities()

    #wps_engines = list_wps_service_engines()
    #my_engine = wps_engines[0]

    #choose the r.time-series-converter

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


    #now we must use our own method to send the request1


    #we need to use the request



    #this code is for the normal wps which is not working right now
    # monitorExecution(execution)
    # output_data = execution.processOutputs
    # final_output_url = output_data[0].reference
    # final_data = read_final_data(final_output_url)

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

def View_R():
    display_r =[]

    session = SessionMaker1()
    script1 = session.query(rscript).all()
    for script in script1:
        display_r.append(script.rscript)
    if display_r[0] == "Time Series Converter":
        my_url = "http://appsdev.hydroshare.org:8282/wps/R/scripts/timeSeriesConverter.R"
    elif display_r[0] =="Gap Filler":
        my_url = 'http://appsdev.hydroshare.org:8282/wps/R/scripts/timeSeriesGapFiller.R'
    r = urllib2.urlopen(my_url)
    r_html = r.read()
    r_code = r_html

    return  {'r_code':r_code,'my_url':my_url}
def upload_to_hs(id,file):
    auth = HydroShareAuthBasic(username='mbayles2', password='lego2695')
    hs = HydroShare(auth=auth)
    fpath = '/path/to/somefile.txt'
    resource_id = hs.addResourceFile('id', file)