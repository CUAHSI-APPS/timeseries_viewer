from django.shortcuts import render
from django.http import JsonResponse


def home(request):
    """
    Controller for the app home page.
    """
    context = {}
    return render(request, 'timeseries_viewer/api_home.html', context)


def list_apps_help(request):
    """
    Controller for the list_apps_help page.
    """
    context = {}
    return render(request, 'timeseries_viewer/api_list_apps.html', context)


def list_apps(request):
    """
    Controller for the list_apps page.
    """
    app1 = {'name': 'Time Series Viewer',
            'url': 'http://apps.hydroshare.org/apps/timeseries-viewer',
            'description': 'View graph and descriptive statistics of one time series',
            'min_series': 1,
            'max_series': 1,
            'icon': 'http://apps.hydroshare.org/static/timeseries_viewer/images/viewer_icon2.gif'}

    app2 = {'name': 'Time Series Converter',
            'url': 'http://apps.hydroshare.org/apps/ts-converter',
            'description': 'Convert time series to daily, weekly, monthly, or yearly aggregate',
            'min_series': 1,
            'max_series': 1,
            'icon': 'http://apps.hydroshare.org/static/ts_converter/images/hydro.gif',
            }

    return JsonResponse({"apps":[app1]})
