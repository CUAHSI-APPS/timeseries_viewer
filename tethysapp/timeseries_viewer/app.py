from tethys_apps.base import TethysAppBase, url_map_maker


class TimeSeriesViewer(TethysAppBase):
    """
    Tethys app class for time series viewer
    """

    name = 'CUAHSI Data Series Viewer'
    index = 'timeseries_viewer:home'
    icon = 'timeseries_viewer/images/viewer_icon2.png'
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
                           url='chart_data/{res_id}/{src}',
                           controller='timeseries_viewer.controllers.chart_data'),
                    UrlMap(name='api',
                           url='api',
                           controller='timeseries_viewer.api.home'),
                    UrlMap(name='view_counter',
                           url='view_counter',
                           controller='timeseries_viewer.controllers.view_counter'),
                    UrlMap(name='error_report',
                           url='error_report',
                           controller='timeseries_viewer.controllers.error_report'),
                    UrlMap(name='api_list_apps',
                           url='api/list_apps',
                           controller='timeseries_viewer.api.list_apps'),

                    UrlMap(name='api_list_apps_help',
                           url='api/list_apps_help',
                           controller='timeseries_viewer.api.list_apps_help'),

                    UrlMap(name='hydroshare',
                           url='hydroshare',
                           controller='timeseries_viewer.controllers.hydroshare'),

                    UrlMap(name='get_hydroshare_res',
                           url='get_hydroshare_res',
                           controller='timeseries_viewer.controllers.get_hydroshare_res')


        )
        return url_maps
