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
            'url': 'http://appsdev.hydroshare.org/apps/timeseries-viewer',
            'description': 'View graph and descriptive statistics for selected time series',
            'min_series': 1,
            'max_series': 5,
            'icon': 'http://appsdev.hydroshare.org/static/timeseries_viewer/images/viewer_icon2.gif'}

    app2 = {'name': 'Correlation Tool',
            'url': 'http://appsdev.hydroshare.org/apps/correlation-tool',
            'description': 'Correlation analysis and scatter plot of two time series',
            'min_series': 2,
            'max_series': 2,
            'icon': 'http://appsdev.hydroshare.org/static/correlation_tool/images/corelation_2.gif',
            }

    return JsonResponse({"apps":[app1, app2]})
