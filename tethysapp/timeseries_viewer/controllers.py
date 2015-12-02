from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import os
import utilities


# -- coding: utf-8--

# helper controller for fetching the WaterML file
def temp_waterml(request, id):
    base_path = utilities.get_workspace()
    file_path = base_path + "/" +id
    response = HttpResponse(FileWrapper(open(file_path)), content_type='application/xml')
    return response


# formats the time series for highcharts
def chart_data(request, res_id):
    base_path = utilities.get_workspace()
    file_path = base_path + "/" + res_id
    if not file_path.endswith('.xml'):
        file_path += '.xml'

    if not os.path.exists(file_path):
        utilities.unzip_waterml(request, res_id)

    # - NEEDSWORK: return error message if the unzip_waterml failed

    data_for_chart = utilities.Original_Checker(file_path)

    # - NEEDSWORK: return error message if parsing the WaterML data failed

    return JsonResponse(data_for_chart)


# home page controller
def home(request):
    return render(request, 'timeseries_viewer/home.html', {})