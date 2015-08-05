from tethys_apps.base import TethysAppBase, url_map_maker
from tethys_apps.base import PersistentStore

class TsConverter(TethysAppBase):
    """
    Tethys app class for ts converter.
    """

    name = 'ts converter'
    index = 'ts_converter:home'
    icon = 'ts_converter/images/icon.gif'
    package = 'ts_converter'
    root_url = 'ts_converter'
    color = '#f1c40f'
        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='ts_converter/',
                           controller='ts_converter.controllers.home'),

                    UrlMap(name='View_R_Code',
                           url='View_R_Code',
                           controller='ts_converter.controllers.View_R_Code')


        )

        return url_maps

    def persistent_stores(self):
        """
        Add one or more persistent stores
        """
        stores = (PersistentStore(name='urls_db',
                                  initializer='init_stores:init_urls_db',
                                  spatial=False),

                  PersistentStore(name='rscript_db',
                                  initializer='init_stores:init_rscript_db',
                                  spatial=False
                                                )


        )

        return stores
