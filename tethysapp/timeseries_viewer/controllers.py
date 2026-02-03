# coding=utf-8
#
# Created by Matthew Bayles, 2016
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from tethys_portal.views.accounts import login_view
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
import os
import re
from . import utilities
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from wsgiref.util import FileWrapper
# from PyQt4.QtCore import QTimer
use_hs_client_helper = True
# Backwards compatibility with older versions of Tethys
try:
    from tethys_services.backends.hs_restclient_helper import get_oauth_hs
except:
    use_hs_client_helper = False

from tethys_sdk.routing import controller

# helper controller for fetching the WaterML file
# @login_required()
@controller(name='temp_waterml', url='temp_waterml/{id}', app_workspace=True)
def temp_waterml(request, id):
    # base_path = utilities.get_workspace() + "/id"
    base_path = utilities.get_workspace()
    file_path = base_path + "/" + id
    response = HttpResponse(FileWrapper(open(file_path)),
                            content_type='application/xml')
    return response

@login_required()
@controller(name='home', url='home')
def home(request):
    message = request.GET.getlist('WofUri')
    print(message)
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

# @login_required()
@csrf_exempt
@never_cache
@controller(url='chart_data/{res_id}/{src}')
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
    try:
        file_meta = utilities.unzip_waterml(request, res_id, src)

        print("done with python")
        return JsonResponse(file_meta)
    
    except Exception as e:
        match = re.search(r"Exception\('(.*)'\)", str(e))
        if match:
            error_message = match.group(1)
        else:
            error_message = str(e)
        
        return JsonResponse({"error": error_message})
    
# @login_required()
@controller(name='get_hydroshare_res', url='get_hydroshare_res')
def get_hydroshare_res(request):
    hs_list = []
    print("getting hydroshare list")
    logged_in_through_hydroshare = False
    try:
        loggedin_through_hydroshare = request.user.social_auth.filter(provider='hydroshare').exists()
    except:
        pass

    if use_hs_client_helper and logged_in_through_hydroshare:
        hs = get_oauth_hs(request)
    else:
        try:
            hs = utilities.getOAuthHS(request)
        except Exception as e:
            return JsonResponse({"error": str(e)})
        
    # resource_types = ['CompositeResource','NetcdfResource','TimeSeriesResource']
    resource_types = ['TimeSeriesResource']
    # resource_types = ['CompositeResource']
    resource_list = hs.getResourceList(types =resource_types)
    for resource in resource_list:
        # if resource.resource_type ==''
        print(resource)
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
        resource_list = hs.getResourceList(full_text_search="#{%Application%Data Series Viewer%}")
    for resource in resource_list:
        # if resource.resource_type ==''
        print(resource)
        hs_res_id = resource['resource_id']
        legend = "<div style='text-align:center'><input class = 'checkbox' name = 'res_hydroshare' id =" + hs_res_id + " type='checkbox' onClick ='check_box(this.id);' status ='unchecked'>" + "</div>"
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
# @login_required()
@controller(name='hydroshare', ur='hydroshare')
def hydroshare(request):
    """Home controller if page is launched from HydroShare"""
    utilities.view_counter(request)

    context = {}
    return render(request, 'timeseries_viewer/home.html', context)

# @login_required()
@controller(name='view_counter', url='view_counter')
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
# @login_required()
@controller(name='error_report', url='error_report')
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
