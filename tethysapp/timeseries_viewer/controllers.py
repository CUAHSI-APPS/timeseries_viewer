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
# -- coding: utf-8--

# helper controller for fetching the WaterML file
def temp_waterml(request, id):
    base_path = utilities.get_workspace() + "/id"
    file_path = base_path + "/" + id
    response = HttpResponse(FileWrapper(open(file_path)), content_type='application/xml')
    return response

# formats the time series for highcharts
@login_required()

def chart_data(request, res_id, src):

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
        data_for_chart = utilities.Original_Checker(file_path)
    # print "JSON Reponse"
    # print datetime.now()

    return JsonResponse(data_for_chart)


# home page controller
def home(request):
    # print datetime.now()
    temp_dir = utilities.get_workspace()

    utilities.viewer_counter(request)
    # r = requests.get('http://tethys.byu.edu/apps/gaugeviewwml/waterml/?gaugeid=10254970&start=2016-06-24&end=2016-07-08', verify=False)
    # print r.content
    # getOAuthHS(request)

    context = {}
    return render(request, 'timeseries_viewer/home.html', context)



    # Code for getting waterml from hydroshare

    # modify utilites method to get generic resource .txt file with parameters for accessing waterml from the hydroserver

    # these parameters come from the generic txt file from hydroshare
    # service_url = 'http://worldwater.byu.edu/interactive/snotel/services/index.php/cuahsi_1_1.asmx?WSDL'
    #        site_code =
    #        variable_code =
    #        client = connect_wsdl_url(service_url)
    #        response = client.service.GetValues(site_code, variable_code, start_date, end_date, auth_token)


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


# def connect_wsdl_url(wsdl_url):
#     try:
#         client = Client(wsdl_url)
#     except TransportError:
#         raise Exception('Url not found')
#     except ValueError:
#         raise Exception('Invalid url')  # ought to be a 400, but no page implemented for that
#     except SAXParseException:
#         raise Exception("The correct url format ends in '.asmx?WSDL'.")
#     except:
#         raise Exception("Unexpected error")
#     return client

#
# def write_file(request):
#     sucess = {"File uploaded": "sucess"}
#     temp_dir = utilities.get_workspace()
#     file_temp_name = temp_dir + '/hydroshare/rtest.r'
#     hs = getOAuthHS(request)
#     abstract = 'My abstract'
#     title = 'My resource script'
#     keywords = ('my keyword 1', 'my keyword 2')
#     rtype = 'ScriptResource'
#     fpath = file_temp_name
#     resource_id = hs.createResource(rtype, title, resource_file=fpath, keywords=keywords, abstract=abstract)
#     # os.remove(file_temp_name)
#     return JsonResponse(sucess)


# def response(request):
#     service_url = 'http://hydroportal.cuahsi.org/nwisdv/cuahsi_1_1.asmx?WSDL'
#     site_code = '10147100'
#     variable_code = 'NWISDV:00060'
#     client = connect_wsdl_url(service_url)
#     start_date = ''
#     end_date = ''
#     auth_token = ''
#     response1 = client.service.GetValues(site_code, variable_code, start_date, end_date, auth_token)
#     # response1 = {"File uploaded":"sucess"}
#     return JsonResponse(response1)

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
