from tethys_apps.base import TethysAppBase, url_map_maker


class TimeSeriesViewer(TethysAppBase):
    """
    Tethys app class for time series viewer
    """

    name = 'CUAHSI Time Series Viewer'
    index = 'timeseries_viewer:home'
    icon = 'timeseries_viewer/images/viewer_icon2.gif'
    package = 'timeseries_viewer'
    root_url = 'timeseries_viewer'
    # color = '#ffff4d'
    description = 'View time series from CUAHSI HydroClient'

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='timeseries_viewer',
                           controller='timeseries_viewer.controllers.home'),

                    UrlMap(name='temp_waterml',
                           url='temp_waterml/{id}',
                           controller='timeseries_viewer.controllers.temp_waterml'),

                    UrlMap(name='chart_data',
                           url='chart_data/{res_id}',
                           controller='timeseries_viewer.controllers.chart_data'),

                    UrlMap(name='api',
                           url='api',
                           controller='timeseries_viewer.api.home'),

                    UrlMap(name='api_list_apps',
                           url='api/list_apps',
                           controller='timeseries_viewer.api.list_apps'),

                    UrlMap(name='api_list_apps_help',
                           url='api/list_apps_help',
                           controller='timeseries_viewer.api.list_apps_help')
        )
        return url_maps
