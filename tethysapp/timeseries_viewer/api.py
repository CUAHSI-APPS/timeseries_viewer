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
    production = False
    app_host =request.META['HTTP_HOST']
    if 'appsdev.hydroshare' in app_host:
        base_url = 'https://appsdev.hydroshare.org/'
        production = False
        # return JsonResponse({"apps": [app1, app2]})
    elif 'hs-apps.hydroshare.org' in app_host:
        base_url = 'https://hs-apps.hydroshare.org/'
        production = True
    elif 'hs-apps-dev.hydroshare.org' in app_host:
        base_url = 'https://hs-apps-dev.hydroshare.org/'
        production = False
    elif 'apps.hydroshare.org' in app_host:
        base_url = 'http://apps.hydroshare.org/'
        production = True
    else:
        base_url = 'http://127.0.0.1:8000/'
        production = False
    # Data Series Viewer App
    app1 = {'name': 'Time Series Viewer',
            # 'url': 'https://appsdev.hydroshare.org/apps/timeseries-viewer',
            'url': base_url + 'apps/timeseries-viewer',
            'description': 'View graph and descriptive statistics for selected time series',
            'min_series': 1,
            'max_series': 5,
            'icon': base_url + 'static/timeseries_viewer/images/viewer_icon2.gif'}
    # HydroShare Resource Creator App
    app2 = {'name': 'Export to HydroShare',
            'url': base_url + 'apps/hydroshare-resource-creator/',
            'description': 'Creates a HydroShare resource from selected time series',
            'min_series': 1,
            'max_series': 10,
            'icon': base_url + 'static/hydroshare_resource_creator/images/tool.svg',
            }
    # Recession Analyzer App
    app3 = {'name': 'Recession Analyzer',
            'url': base_url + 'apps/recession-analyzer/',
            'description': 'Creates a HydroShare resource from selected time series',
            'min_series': 1,
            'max_series': 10,
            'icon': base_url + 'static/recession_analyzer/images/icon.gif',
            }
    # Time Series Manager App
    app4 = {'name': 'Time Series Manager',
            'url': base_url + 'apps/hydroshare-timeseries-manager/',
            'description': 'Import and edit HydroShare timeseries data',
            'min_series': 1,
            'max_series': 100,
            'icon': base_url + 'static/hydroshare_timeseries_manager/images/icon.gif',
            }

    if production:
        return JsonResponse({"apps": [app1, app2]})
    else:
        return JsonResponse({"apps": [app1, app2, app4]})
