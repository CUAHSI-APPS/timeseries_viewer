# coding=utf-8
#
# Created by Matthew Bayles, 2016
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
import requests
import utilities
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
import sqlite3
from wsgiref.util import FileWrapper
use_hs_client_helper = True
# Backwards compatibility with older versions of Tethys
try:
    from tethys_services.backends.hs_restclient_helper import get_oauth_hs
except Exception as ex:
    use_hs_client_helper = False


# helper controller for fetching the WaterML file
def temp_waterml(request, id):
    # base_path = utilities.get_workspace() + "/id"
    base_path = utilities.get_workspace()
    file_path = base_path + "/" + id
    response = HttpResponse(FileWrapper(open(file_path)),
                            content_type='application/xml')
    return response


def home(request):
    """Home controller if page is launched from HydroShare"""
    context = {}
    return render(request, 'timeseries_viewer/home.html', context)

def test():
    print "d"
@csrf_exempt
@never_cache
def chart_data(request, res_id, src):
    """
    Get data for each site

    Parameters
    __________
    request : http request object
        A list of lists. Each list contains the site code, source, site name,
        and url of each requested site
    res_id : str

    Returns
    _______
    list
        A list of dictionaries containing data required for graphing. Includes
        x and y values, variable, and name

    Notes
    _____
    The  return list also includes additional site data about each NOAA site.
    This site data is formatted differently then the main site data.

    """
    # id from USGS Gauge Viewer app
    # if "xmlrest" in src:
    #     res_id = request.POST.get('url_xml')
    #     # Creates a unique id for the time series
    #     xml_id = str(uuid.uuid4())
    file_meta = utilities.unzip_waterml(request, res_id, src)
    # print file_meta
    # if we don't have the xml file, download and unzip it
    # file_number = int(file_meta['file_number'])
    # file_path = file_meta['file_path']
    # file_type = file_meta['file_type']
    # error = file_meta['error']
    # if error == '':
    #     if file_type == 'waterml':
    #         # file_path = utilities.waterml_file_path(res_id,xml_id)
    #         data_for_chart.append(utilities.Original_Checker(file_path))
    #     elif file_type == '.json.refts':
    #         for i in range(0, file_number):
    #             # file_path = temp_dir+'/id/timeserieslayer'+str(i)+'.xml'
    #             file_path = temp_dir+'/timeserieslayer'+str(i)+'.xml'
    #             data_for_chart.append(utilities.Original_Checker(file_path))
    #     elif file_type == 'sqlite':
    #         print file_path
    #         conn = sqlite3.connect(file_path)
    #         c = conn.cursor()
    #         c.execute('SELECT Results.ResultID FROM Results')
    #         num_series = c.fetchall()
    #         conn.close()
    #         for series in num_series:
    #             str_series = str(series[0])
    #             data_for_chart.append(utilities.parse_odm2(file_path,
    #                                                        str_series))
    # if isinstance(data_for_chart[0],basestring)==True:
    #     error = data_for_chart[0]
    # # print data_for_chart
    # return JsonResponse({'data':data_for_chart,'error':error})
    return JsonResponse(file_meta)


# seperate handler for request originating from hydroshare.org
@csrf_exempt
@login_required()
def hydroshare(request):
    """Home controller if page is launched from HydroShare"""
    context = {}
    return render(request, 'timeseries_viewer/home.html', context)


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
    return JsonResponse({"Error Reports": content})
