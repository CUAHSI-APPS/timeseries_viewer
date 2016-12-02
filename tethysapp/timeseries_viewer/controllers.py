from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from wsgiref.util import FileWrapper
from django.contrib.auth.decorators import login_required
import os
from datetime import datetime
import requests
import utilities
import tempfile
from hs_restclient import HydroShare, HydroShareAuthOAuth2, HydroShareNotAuthorized, HydroShareNotFound
from suds.transport import TransportError
from suds.client import Client
from xml.sax._exceptions import SAXParseException
from django.conf import settings
import uuid
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
import urllib
# -- coding: utf-8--

# helper controller for fetching the WaterML file
def temp_waterml(request, id):
    base_path = utilities.get_workspace() + "/id"
    file_path = base_path + "/" + id
    response = HttpResponse(FileWrapper(open(file_path)), content_type='application/xml')
    return response

# formats the time series for highcharts

# @ensure_csrf_cookie
@csrf_exempt
@never_cache
def chart_data(request, res_id, src,id_qms):
    test = ''
    xml_id = None
    xml_rest = False
    if "xmlrest" in src:
        xml_rest = True
        test = request.POST.get('url_xml')
        xml_id =  str(uuid.uuid4())

    # print datetime.now()
    # checks if we already have an unzipped xml file
    file_path = utilities.waterml_file_path(res_id,xml_rest,xml_id)
    # if we don't have the xml file, downloads and unzips it
    if not os.path.exists(file_path):
        utilities.unzip_waterml(request, res_id, src, test,xml_id)

    # returns an error message if the unzip_waterml failed
    if not os.path.exists(file_path):
        data_for_chart = {'status': 'Resource file not found'}
    else:
        # parses the WaterML to a chart data object
        data_for_chart = utilities.Original_Checker(file_path,id_qms)
    # print "JSON Reponse"
    # print datetime.now()
    print "end of chart data"
    return JsonResponse(data_for_chart)


# home page controller
@csrf_exempt
@never_cache
def home(request):
    ids=[]
    meta =[]
    source=[]
    quality=[]
    method=[]
    sourceid=[]

    try: #Check to see if request if from CUAHSI. For data validation
        request_url = request.META['HTTP_REFERER']

    except:
        request_url ="test"
    data = request.META['QUERY_STRING']#stores all values in the query string
    data = data.encode(encoding ='UTF-8')#encodes the data string to avoid having unicode character in string
    data  =data.split('&')
    for e in data:
        s= e.split('=')
        meta.append(s)
    for e in meta:
        print e
        if e[0] == 'Source':
            source.append(e[1])
        if e[0] == 'WofUri':
            ids.append(e[1])
        if e[0] == 'QCLID':
            quality.append(e[1])
        if e[0] == 'MethodId':
            method.append(e[1])
        if e[0] == 'SourceId':
            sourceid.append(e[1])

    utilities.viewer_counter(request)
    #the parametes passed from CUAHSI are stored in a hidden div on the home page so that the js file is able to read them
    context = {'source':source,
               'cuahsi_ids':ids,
               'quality':quality,
               'method':method,
               'sourceid':sourceid,

               }
    return render(request, 'timeseries_viewer/home.html', context)
#seperate handler for request originating from hydroshare.org
@csrf_exempt
@login_required()
def hydroshare(request):
    utilities.viewer_counter(request)
    context = {}
    return render(request, 'timeseries_viewer/home.html', context)

def getOAuthHS(request):
    hs_instance_name = "www"
    client_id = getattr(settings, "SOCIAL_AUTH_HYDROSHARE_KEY", None)
    client_secret = getattr(settings, "SOCIAL_AUTH_HYDROSHARE_SECRET", None)
    # this line will throw out from django.core.exceptions.ObjectDoesNotExist if current user is not signed in via HydroShare OAuth
    token = request.user.social_auth.get(provider='hydroshare').extra_data['token_dict']
    hs_hostname = "{0}.hydroshare.org".format(hs_instance_name)
    auth = HydroShareAuthOAuth2(client_id, client_secret, token=token)
    hs = HydroShare(auth=auth, hostname=hs_hostname)
    return hs
def view_counter(request):
    temp_dir = utilities.get_workspace()
    file_path = temp_dir[:-24] + 'view_counter.txt'
    file_temp = open(file_path, 'r')
    content = file_temp.read()
    return JsonResponse({"Number of Viewers":content})

def error_report(request):
    print os.path.realpath('controllers.py')
    temp_dir = utilities.get_workspace()
    temp_dir = temp_dir[:-24]
    file_path = temp_dir + '/error_report.txt'
    if not os.path.exists(temp_dir+"/error_report.txt"):
        file_temp = open(file_path, 'a')
        file_temp.close()
        content = ''
    else:
        file_temp = open(file_path, 'r')
        content = file_temp.read()
    return JsonResponse({"Error Reports":content})
@csrf_exempt
@never_cache
def test(request):
    import json
    request_url = request.META['QUERY_STRING']


    # not ajax
    # curl -X POST -d 'name1=value1&name2=value2&name1=value11' "http://127.0.0.1:8000/apps/timeseries-viewer/test/"

    # curl -X POST -H "Content-Type: application/json" -d '{"mylist": ["item1", "item2", "item3"], "list_type": "array"}' "http://127.0.0.1:8000/apps/timeseries-viewer/test/"

    # curl -X POST -F 'name1=value1' -F 'name2=value2' -F 'name1=value11' "http://127.0.0.1:8000/apps/timeseries-viewer/test/"

    # ajax
    # curl -X POST -H "X-Requested-With: XMLHttpRequest" -d 'name1=value1&name2=value2&name1=value11' "http://127.0.0.1:8000/apps/timeseries-viewer/test/"

    # curl -X POST -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json" -d '{"mylist": ["item1", "item2", "item3"], "list_type": "array"}' "http://127.0.0.1:8000/apps/timeseries-viewer/test/"


    result = {}
    result['query_string'] =request_url
    result["is_ajax"] = request.is_ajax()

    result["request.GET"] = request.GET
    result["request.POST"] = request.POST
    r = requests.post('http://httpbin.org/post', files={'report.xls': open('report.xls', 'rb')})
    try:
        result["request.body"] = request.body
    except:
        pass

    try:
        result["request.body -> json"] = json.loads(request.body)
    except:
        pass

    print result

    context ={"result": json.dumps(result)
               }
    return render(request, 'timeseries_viewer/test.html', context)