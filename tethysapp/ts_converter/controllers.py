from django.shortcuts import render
from utilities import *
from tethys_apps.sdk.gizmos import Button
from tethys_gizmos.gizmo_options import *
from owslib.wps import WebProcessingService
from owslib.wps import printInputOutput
from tethys_apps.sdk import get_wps_service_engine
from owslib.wps import monitorExecution
from owslib.wps import WPSExecution
from datetime import datetime
import urllib2
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


def home(request):

    filename=None
    res_id=None
    url_wml=None
    branch=None
    name = None
    show_time = False
    no_url = False
    output_converter = None

    text_input_options = TextInput(display_text='Enter URL of Water ML data',
                                   name='url_name')

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


    #if request.POST and request.POST['select_interval']=='default' or request.POST['select_stat'] == 'no_select':
        #url_wml = None

    #plotting the unaltered time seres
    if request.POST and 'url_name' in request.POST:
	       url_wml = request.POST['url_name']
	       filename = 'Current Time Series'
	       response = urllib2.urlopen(url_wml)
    	       html = response.read()
    	       timeseries_plot = chartPara(html,filename)


    show_time = True
    #this is the default chart if no values are given
    if url_wml is None:
        filename = 'KiWIS-WML2-Example.wml'
        url_wml='http://www.waterml2.org/KiWIS-WML2-Example.wml'
        no_url = True
        response = urllib2.urlopen(url_wml)
     	html = response.read()
     	timeseries_plot = chartPara(html,filename)
        plot = chartPara(html,filename)

    else:
        url_wps = 'http://localhost:8282/wps/WebProcessingService'
        url_user = url_wml
        interval = request.POST['select_interval']
        #interval = "daily"
        stat = request.POST['select_stat']
        #stat = "mean"
        #replace "=" with "!" and "&" with "|"
        #url_user = 'http://worldwater.byu.edu/app/index.php/byu_test_justin/services/cuahsi_1_1.asmx/GetValuesObject?location!byu_test_justin:B-Lw~variable!byu_test_justin:WATER~startDate!~endDate!'
        url_user = url_user.replace('=', '!')
        url_user = url_user.replace('&', '~')

        process_input = '<?xml+version="1.0"+encoding="UTF-8"+standalone="yes"?><wps:Execute+service="WPS"+version="1.0.0"++xmlns:wps="http://www.opengis.net/wps/1.0.0"+xmlns:ows="http://www.opengis.net/ows/1.1"++xmlns:xlink="http://www.w3.org/1999/xlink"+xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"++xsi:schemaLocation="http://www.opengis.net/wps/1.0.0++http://schemas.opengis.net/wps/1.0.0/wpsExecute_request.xsd">++<ows:Identifier>org.n52.wps.server.r.timeSeriesConverter</ows:Identifier>++<wps:DataInputs>++++<wps:Input>++++++<ows:Identifier>url</ows:Identifier>++++++<wps:Data>++++++++<wps:LiteralData>'+url_user+'</wps:LiteralData>++++++</wps:Data>++++</wps:Input>++++<wps:Input>++++++<ows:Identifier>interval</ows:Identifier>++++++<wps:Data>++++++++<wps:LiteralData>'+interval+'</wps:LiteralData>++++++</wps:Data>++++</wps:Input>++++<wps:Input>++++++<ows:Identifier>stat</ows:Identifier>++++++<wps:Data>++++++++<wps:LiteralData>'+stat+'</wps:LiteralData>++++++</wps:Data>++++</wps:Input>++</wps:DataInputs>++<wps:ResponseForm>++++<wps:ResponseDocument+storeExecuteResponse="false">++++++<wps:Output+asReference="false">++++++++<ows:Identifier>output</ows:Identifier>++++++</wps:Output>++++</wps:ResponseDocument>++</wps:ResponseForm></wps:Execute>'
        wps_request = urllib2.Request(url_wps,process_input)
        wps_open = urllib2.urlopen(wps_request)
        wps_read = wps_open.read()

        plot = TimeSeriesConverter(wps_read)

    context = {"timeseries_plot":timeseries_plot,
'plot':plot,
'text_input_options':text_input_options,
'name':name,
'select_interval': select_interval,
'select_stat':select_stat,
'show_time':show_time,
'no_url':no_url,
'output_converter':output_converter

}
    
    return render(request, 'ts_converter/home.html', context)



