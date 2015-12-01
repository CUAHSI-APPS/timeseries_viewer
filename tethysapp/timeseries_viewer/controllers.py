from django.shortcuts import render
from django.http import JsonResponse
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


# formats the time series for highcharts
def chart_data(request, res_id):
    base_path = get_workspace()
    file_path = base_path + "/" + res_id
    if not file_path.endswith('.xml'):
        file_path += '.xml'

    if not os.path.exists(file_path):
        unzip_waterml(request, res_id)

    data_for_chart = Original_Checker(file_path, time_format='highcharts')
    return JsonResponse(data_for_chart)


# home page controller
def home(request):
    name = None
    no_url = False
    number_ts = []
    url_list = []
    legend = []
    show_waterml = False
    timeseries_plot =None
    outside_input = False
    stat_data2 = []
    meta_data = []
    use_wps = False
    show_add_clear_ts = False

    print"starting"
    if request.GET:

        return render(request, 'timeseries_viewer/home.html', {})
    else:
        if 'res_id' in request.GET and 'src' in request.GET:
            resources = getResourceIDs(request)
            for id in resources:
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
                    legend ={'layout': 'vertical','align': 'left','verticalAlign': 'top','borderWidth': 0,'floating':"false",'backgroundColor': 'FCFFC5'}
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
    print meta_data

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
        'name': name,
        'stat_data': stat_data2,
        'stat_table': stat_table,
        'no_url': no_url,
        'add_ts': add_ts,
        'clear_all_ts': clear_all_ts,
        'graph': graph,
        'legend': legend,
        'hydroshare_resource': hydroshare_resource,
        'water_ml': water_ml,
        'show_waterml': show_waterml,
        'upload_hs': upload_hs,
        'choices': choices,
        'show_add_clear_ts': show_add_clear_ts,
        'meta_data':meta_data
    }
    return render(request, 'timeseries_viewer/home.html', context)