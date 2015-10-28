from tethys_apps.base import TethysAppBase, url_map_maker
from tethys_apps.base import PersistentStore


class TsConverter(TethysAppBase):
    """
    Tethys app class for ts converter.
    """

    name = 'timeseries viewer'
    index = 'timeseries_viewer:home'
    icon = 'timeseries_viewer/images/icon.gif'
    package = 'timeseries_viewer'
    root_url = 'timeseries_viewer'
    color = '#f1c40f'
        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='timeseries_viewer/',
                           controller='timeseries_viewer.controllers.home'),

                    UrlMap(name='temp_waterml',
                           url='temp_waterml/{folder}/{id}',
                           controller='ts_converter.controllers.temp_waterml')
        )
        return url_maps
