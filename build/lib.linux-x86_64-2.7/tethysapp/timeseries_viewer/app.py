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
        )

        return url_maps

    def persistent_stores(self):
        """
        Add one or more persistent stores
        """
        stores = (PersistentStore(name='urls_db',
                                  initializer='init_stores:init_urls_db',
                                  spatial=False),



        )

        return stores
