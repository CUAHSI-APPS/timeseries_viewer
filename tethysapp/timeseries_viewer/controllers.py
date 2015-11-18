from django.shortcuts import render
from utilities import *
from tethys_gizmos.gizmo_options import *
from django.core.servers.basehttp import FileWrapper
from owslib.wps import WebProcessingService
import requests
import csv
import urllib2
from hs_restclient import HydroShare, HydroShareAuthBasic

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


def temp_waterml(request, id):
    base_path = get_workspace()
    file_path = base_path + "/" +id
    response = HttpResponse(FileWrapper(open(file_path)), content_type='application/xml')
    return response


def home(request):
    name = None
    no_url = False
    number_ts = []#stores highcharts info of each time series
    url_list = []
    legend = []
    show_hydroshare = False
    show_waterml = False
    show_cuahsi = False
    timeseries_plot =None
    outside_input = False
    stat_data2 = []
    meta_data = []
    use_wps = False
    show_add_clear_ts = False

    if request.GET and 'res_id' in request.GET and 'src' in request.GET:
        outside_input = True

    if request.GET and 'res_id' in request.GET and 'src' in request.GET:
        outside_input = True
        if request.GET['src'] == "hydroshare":
            show_hydroshare = True
        elif request.GET['src']=='cuahsi':
            show_cuahsi =True
            outside_input = True
            cuahsi_resources = getResourceIDs(request)
            for id in cuahsi_resources:
                unzip_waterml(request, id, src='cuahsi')
        elif request.GET['src'] == 'test':
            show_cuahsi = True
            test_resources = getResourceIDs(request)
            for id in test_resources:
                unzip_waterml(request, id, src='test')

    if request.POST and 'hydroshare' in request.POST:
        show_hydroshare = True
    if request.POST and 'water_ml' in request.POST:
        show_waterml = True



    # this block of code will add a time series from hydroshare
    if (request.POST and "add_ts" in request.POST) or outside_input:
        if not outside_input:
            print "not using outside_input"

        if request.POST.get('hydroshare_resource') != None and request.POST.get('hydroshare_file')!= None:
            try:
                #adding a hydroshare resource
                hs = HydroShare()
                hs_resource = request.POST['hydroshare_resource']
                hs_file = request.POST['hydroshare_file']
                url_hs_resource = "https://www.hydroshare.org/resource/"+hs_resource+"/data/contents/"+hs_file
            except etree.XMLSyntaxError as e: #checks to see if data is an xml
                print "Error:Not XML"
                #quit("not valid xml")
            except ValueError, e: #checks to see if Url is valid
                print "Error:invalid Url"
            except TypeError, e: #checks to see if xml is formatted correctly
                print "Error:string indices must be integers not str"


        #adding data through cuashi or from a water ml url
        if show_cuahsi == True:

            cuahsi_resources = getResourceIDs(request)
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
                    stat_data2.append({'site_name': graph_original['site_name'],
                               'mean': '%.4f'% graph_original['mean'],
                               'median': '%.4f'% graph_original['median'],
                               'stdev': '%.4f'% graph_original['stdev'],
                               'count': '%d'% graph_original['count']})

                    meta_data.append({'site_name':graph_original['site_name'],
                                      'variable_name':graph_original['variable_name'],
                                      'units':graph_original['units'],
                                      'organization':graph_original['organization']})
                    legend ={'layout': 'vertical','align': 'right','verticalAlign': 'top','borderWidth': 0,'floating':"false",'backgroundColor': 'FCFFC5'}
                    graph_type = 'spline'
                    units_space = ' '+graph_original['units']+'test'
                    tooltip_units = {'valueSuffix': units_space}
                    ts_name = graph_original['site_name'] + ' '+graph_original['variable_name'] +': '+graph_original['organization']
                    number_ts.append({'name':ts_name,'data':graph_original['for_highchart'],'type':graph_type,'lineWidth': 3, 'tooltip':tooltip_units})



                except etree.XMLSyntaxError as e: #checks to see if data is an xml
                    print "Error:Not XML"
                except ValueError, e: #checks to see if Url is valid
                    print "Error:invalid Url"
                except TypeError, e: #checks to see if xml is formatted correctly
                    print "Error:string indices must be integers not str"

            #finally plot the charts
            timeseries_plot = chartPara(graph_original,number_ts,legend)






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
    stat_table = TableView(column_names=('Name', 'Mean', 'Median', 'Standard Deviation'),
                           rows = stat_data2,
                           hover =True,
                           striped = False,
                           bordered = True,
                           condensed = True
                           )
    context = {
        'timeseries_plot':timeseries_plot,
        'text_input_options':text_input_options,
        'name':name,
        'stat_data':stat_data2,
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
        'choices':choices,
        'show_add_clear_ts':show_add_clear_ts,

        'meta_data':meta_data
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

    return [wps_read1, split]


def read_final_data(url):
    r = requests.get(url)
    data = r.text
    reader = csv.reader(data.splitlines(), delimiter='\t')
    rows = []
    for row in reader:
        rows.append(row)
    return rows