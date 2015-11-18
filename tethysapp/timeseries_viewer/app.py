from tethys_apps.base import TethysAppBase, url_map_maker
from tethys_apps.base import PersistentStore


class TsConverter(TethysAppBase):
    """
    Tethys app class for ts converter.
    """

    name = 'timeseries viewer'
    index = 'timeseries_viewer:home'
    icon = 'timeseries_viewer/images/viewer_icon2.gif'
    package = 'timeseries_viewer'
    root_url = 'timeseries_viewer'
    # color = '#ffff4d'

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='timeseries_viewer/',
                           controller='timeseries_viewer.controllers.home'),

                    UrlMap(name='temp_waterml',
                           url='temp_waterml/{id}',
                           controller='timeseries_viewer.controllers.temp_waterml')
        )
        return url_maps
