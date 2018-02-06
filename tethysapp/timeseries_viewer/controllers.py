# coding=utf-8
#
# Created by Matthew Bayles, 2016
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
import os
import requests
import utilities
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
import sqlite3
from wsgiref.util import FileWrapper
import ast as ast
import json
import netCDF4
from selenium import webdriver
import shapely.wkt
import shapely.geometry
import shapely.ops
# import pyproj
from osgeo import ogr
from osgeo import osr
# from PyQt4.QtCore import QTimer
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
    # utilities.view_counter(request)
    # forcing_proj4 = '+proj=lcc +lat_1=30 +lat_2=60 +lat_0=40 +lon_0=-97 +x_0=0 +y_0=0 +a=6370000 +b=6370000 +units=m +no_defs'
    # wkt_epsg = 4326
    # wkt_str = 'Point(917499 318499.9)'
    # reproject = utilities.reproject_wkt_gdal("proj4",
    #                                          forcing_proj4,
    #                                          "epsg",
    #                                          wkt_epsg,
    #                                          wkt_str)
    context = {}
    return render(request, 'timeseries_viewer/home.html', context)

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

    file_meta = utilities.unzip_waterml(request, res_id, src)

    print "done with python"
    return JsonResponse(file_meta)


def get_hydroshare_res(request):
    hs_list = []
    print "getting hydroshare list"
    if use_hs_client_helper:
        hs = get_oauth_hs(request)
    else:
        hs = utilities.getOAuthHS(request)
    # resource_types = ['CompositeResource','NetcdfResource','TimeSeriesResource']
    resource_types = ['TimeSeriesResource']
    # resource_types = ['CompositeResource']
    resource_list = hs.getResourceList(types =resource_types )
    for resource in resource_list:
        # if resource.resource_type ==''
        print resource
        hs_res_id = resource['resource_id']
        legend = "<div style='text-align:center'><input class = 'checkbox' name = 'res_hydroshare' id =" + hs_res_id+" type='checkbox' onClick ='check_box(this.id);' status ='unchecked'>" + "</div>"
        title = resource['resource_title']
        type = resource['resource_type']
        author = resource['creator']
        update = resource['date_last_updated']
        hs_dic = dict(legend=legend,
                      title=title,
                      type=type,
                      author=author,
                      update=update,
                      resource_id=hs_res_id)
        hs_list.append(hs_dic)
    hs_response = dict(error='', data=hs_list)
    return JsonResponse(hs_response)

# seperate handler for request originating from hydroshare.org
@csrf_exempt
@login_required()
def hydroshare(request):
    """Home controller if page is launched from HydroShare"""
    utilities.view_counter(request)

    context = {}
    return render(request, 'timeseries_viewer/home.html', context)


def view_counter(request):
    temp_dir = utilities.get_workspace()
    file_path = temp_dir + '/timeseries_viewer_view_counter.txt'
    if not os.path.exists(file_path):
        file_temp = open(file_path, 'w')
        file_temp.write('0')
        file_temp.close()
    file_temp = open(file_path, 'r')
    content = file_temp.read()
    return JsonResponse({"Number of Viewers":content})


# @user_passes_test(lambda u: u.is_superuser)
@staff_member_required
def error_report(request):
    content = None
    e = None
    temp_dir = utilities.get_workspace()
    file_path = temp_dir + '/timeseries_viewer_error_report.txt'
    if not os.path.exists(temp_dir+"/timeseries_viewer_error_report.txt"):
        file_temp = open(file_path, 'a')
        file_temp.write('')
        file_temp.close()
        content = ''

    file_temp = open(file_path, 'r')
    content = file_temp.read()
        # try:
        #     content = ast.literal_eval(content)
        # except Exception as e:

            # content = content
    return HttpResponse(content)
    # return JsonResponse(content)
