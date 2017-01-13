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
    app1 = {'name': 'Data Series Viewer',
            'url': 'https://appsdev.hydroshare.org/apps/timeseries-viewer/',
            # 'url': 'http://apps.hydroshare.org/apps/timeseries-viewer',
            'description': 'View graph and descriptive statistics for selected time series',
            'min_series': 1,
            'max_series': 5,
            'icon': 'https://appsdev.hydroshare.org/static/timeseries_viewer/images/viewer_icon2.gif'}

    app2 = {'name': 'Correlation Tool',
            'url': 'https://appsdev.hydroshare.org/apps/correlation-tool/',
            'description': 'Correlation analysis and scatter plot of two time series',
            'min_series': 2,
            'max_series': 2,
            'icon': 'https://appsdev.hydroshare.org/static/correlation_tool/images/corelation_2.gif',
            }
    app3 = {'name': 'Gap Filler Tool',
            'url': 'https://appsdev.hydroshare.org/apps/gap-filler-tool/',
            'description': 'Fills gaps in a time series',
            'min_series': 1,
            'max_series': 1,
            'icon': 'https://appsdev.hydroshare.org/static/gap_filler_tool/images/icon.gif',
            }
    app4 = {'name': 'Create HydroShare Resource',
            # 'name': 'HydroShare Resource Creator',
            'url': 'https://appsdev.hydroshare.org/apps/hydroshare-resource-creator/',
            'description': 'Creates a HydroShare resource from selected time series',
            'min_series': 1,
            'max_series': 10,
            'icon': 'https://appsdev.hydroshare.org/static/hydroshare_resource_creator/images/icon.gif',
            }

    return JsonResponse({"apps":[app1, app2, app3, app4]})
    # return JsonResponse({"apps":[app1]})
