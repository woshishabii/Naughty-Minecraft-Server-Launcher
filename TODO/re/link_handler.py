import requests

from settings import ServerLauncherSettings

class LinkHandler:
    def __init__(self, sl_settings: ServerLauncherSettings):
        self.sl_settings = sl_settings

        self.requests_object = {}
        self.beautifulsoup_object = {}

    def get_vanilla_link_list_via_getbukkit(self):
        self.requests_object['getbukkit-vaniila'] = requests.get(self.sl_settings.sources['getbukkit-vanilla'])
        # TODO LOG
        self.beautifulsoup_object['getbukkit-vanilla'] =
