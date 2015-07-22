from tethys_apps.base import TethysAppBase, url_map_maker


class TsConverter(TethysAppBase):
    """
    Tethys app class for ts converter.
    """

    name = 'ts converter'
    index = 'ts_converter:home'
    icon = 'ts_converter/images/icon.gif'
    package = 'ts_converter'
    root_url = 'ts-converter'
    color = '#f1c40f'
        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='ts-converter',
                           controller='ts_converter.controllers.home'),
        )

        return url_maps