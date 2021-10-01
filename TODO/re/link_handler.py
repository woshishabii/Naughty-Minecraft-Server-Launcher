import requests
from bs4 import BeautifulSoup
import re

from settings import ServerLauncherSettings

class LinkHandler:
    def __init__(self, sl_settings: ServerLauncherSettings):
        self.sl_settings = sl_settings

        self.requests_object = {}
        self.beautifulsoup_object = {}
        self.versions = {}

        self.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def get_vanilla_link_list_via_getbukkit(self):
        self.requests_object['getbukkit-vanilla'] = requests.get(self.sl_settings.sources['getbukkit-vanilla'])
        # TODO LOG
        self.beautifulsoup_object['getbukkit-vanilla'] = BeautifulSoup(self.requests_object['getbukkit-vanilla'].text,
                                                                       'html.parser')
        self.versions_temp = []
        for temp in self.beautifulsoup_object['getbukkit-vanilla'].find_all('h2'):
            self.versions_temp.append(str(temp)[4:-5])
        self.sizes_temp = []
        self.release_data_temp = []
        for temp in self.beautifulsoup_object['getbukkit-vanilla'].find_all('h3'):
            temp = str(temp)[4:-5]
            if temp.endswith('MB'):
                self.sizes_temp.append(temp)
            else:
                for weekday in self.weekdays:
                    if weekday in temp:
                        self.release_data_temp.append(temp)
                        break
        self.getbukkit_link_temp = []
        for temp in self.beautifulsoup_object['getbukkit-vanilla'].find_all('a'):
            if temp.get('href').startswith('https://getbukkit.org/get'):
                self.getbukkit_link_temp.append(temp.get('href'))
        self.download_link_temp = []
        for temp in self.getbukkit_link_temp:
            self.getbukkit_link_request_temp = requests.get(temp)
            self.getbukkit_link_beautifulsoup_temp = BeautifulSoup(self.getbukkit_link_request_temp.text, 'html.parser')
            for temp in self.getbukkit_link_beautifulsoup_temp.find_all('a'):
                if (temp.get('href').startswith('https://launcher.mojang.com/v1/objects/')
                        or temp.get('href').startswith('https://download.getbukkit.org/spigot/')
                        or temp.get('href').startswith('https://download.getbukkit.org/craftbukkit/')
                        or temp.get('href').startswith('https://cdn.getbukkit.org/craftbukkit/')
                        or temp.get('href').startswith('https://cdn.getbukkit.org/spigot')
                        or temp.get('href').startswith('https://launcher.mojang.com/mc/game/')):
                    self.download_link_temp.append(temp.get('href'))
        self.versions['getbukkit-vanilla'] = {}
        for temp in range(len(self.versions_temp)):
            # print(self.versions_temp[temp])
            self.versions['getbukkit-vanilla'][self.versions_temp[temp]] = {
                'size': self.sizes_temp[temp],
                'release-data': self.release_data_temp[temp],
                'link': self.download_link_temp[temp],
            }

    def get_spigot_link_list_via_getbukkit(self):
        self.requests_object['getbukkit-spigot'] = requests.get(self.sl_settings.sources['getbukkit-spigot'])
        # TODO LOG
        self.beautifulsoup_object['getbukkit-spigot'] = BeautifulSoup(self.requests_object['getbukkit-spigot'].text,
                                                                       'html.parser')
        self.versions_temp = []
        for temp in self.beautifulsoup_object['getbukkit-spigot'].find_all('h2'):
            self.versions_temp.append(str(temp)[4:-5])
        self.sizes_temp = []
        self.release_data_temp = []
        for temp in self.beautifulsoup_object['getbukkit-spigot'].find_all('h3'):
            temp = str(temp)[4:-5]
            if (re.match(r'^[0-9][0-9].[0-9] MB$', temp, re.I | re.M)
                    or re.match(r'^[0-9][0-9].[0-9][0-9] MB$', temp, re.I | re.M)
                    or re.match(r'^[0-9][0-9].[0-9][0-9]$', temp, re.I | re.M)):
                self.sizes_temp.append(temp)
            else:
                for weekday in self.weekdays:
                    if weekday in temp:
                        self.release_data_temp.append(temp)
                        break
        self.getbukkit_link_temp = []
        for temp in self.beautifulsoup_object['getbukkit-spigot'].find_all('a'):
            if temp.get('href').startswith('https://getbukkit.org/get'):
                self.getbukkit_link_temp.append(temp.get('href'))
        self.download_link_temp = []
        for temp in self.getbukkit_link_temp:
            self.getbukkit_link_request_temp = requests.get(temp)
            self.getbukkit_link_beautifulsoup_temp = BeautifulSoup(self.getbukkit_link_request_temp.text, 'html.parser')
            for temp in self.getbukkit_link_beautifulsoup_temp.find_all('a'):
                if (temp.get('href').startswith('https://launcher.mojang.com/v1/objects/')
                        or temp.get('href').startswith('https://download.getbukkit.org/spigot/')
                        or temp.get('href').startswith('https://download.getbukkit.org/craftbukkit/')
                        or temp.get('href').startswith('https://cdn.getbukkit.org/craftbukkit/')
                        or temp.get('href').startswith('https://cdn.getbukkit.org/spigot')
                        or temp.get('href').startswith('https://launcher.mojang.com/mc/game/')):
                    self.download_link_temp.append(temp.get('href'))
        self.versions['getbukkit-spigot'] = {}
        for temp in range(len(self.versions_temp)):
            # print(self.versions_temp[temp])
            # print(self.sizes_temp[temp])
            self.versions['getbukkit-spigot'][self.versions_temp[temp]] = {
                'size': self.sizes_temp[temp],
                'release-data': self.release_data_temp[temp],
                'link': self.download_link_temp[temp],
            }

    def get_craftbukkit_link_list_via_getbukkit(self):
        self.requests_object['getbukkit-craftbukkit'] = requests.get(self.sl_settings.sources['getbukkit-craftbukkit'])
        # TODO LOG
        self.beautifulsoup_object['getbukkit-craftbukkit'] = BeautifulSoup(self.requests_object['getbukkit-craftbukkit'].text,
                                                                       'html.parser')
        self.versions_temp = []
        for temp in self.beautifulsoup_object['getbukkit-craftbukkit'].find_all('h2'):
            self.versions_temp.append(str(temp)[4:-5])
        self.sizes_temp = []
        self.release_data_temp = []
        for temp in self.beautifulsoup_object['getbukkit-craftbukkit'].find_all('h3'):
            temp = str(temp)[4:-5]
            if temp.endswith('MB'):
                self.sizes_temp.append(temp)
            else:
                for weekday in self.weekdays:
                    if weekday in temp:
                        self.release_data_temp.append(temp)
                        break
        self.getbukkit_link_temp = []
        for temp in self.beautifulsoup_object['getbukkit-craftbukkit'].find_all('a'):
            if temp.get('href').startswith('https://getbukkit.org/get'):
                self.getbukkit_link_temp.append(temp.get('href'))
        self.download_link_temp = []
        for temp in self.getbukkit_link_temp:
            self.getbukkit_link_request_temp = requests.get(temp)
            self.getbukkit_link_beautifulsoup_temp = BeautifulSoup(self.getbukkit_link_request_temp.text, 'html.parser')
            for temp in self.getbukkit_link_beautifulsoup_temp.find_all('a'):
                if (temp.get('href').startswith('https://launcher.mojang.com/v1/objects/')
                        or temp.get('href').startswith('https://download.getbukkit.org/spigot/')
                        or temp.get('href').startswith('https://download.getbukkit.org/craftbukkit/')
                        or temp.get('href').startswith('https://cdn.getbukkit.org/craftbukkit/')
                        or temp.get('href').startswith('https://cdn.getbukkit.org/spigot')
                        or temp.get('href').startswith('https://launcher.mojang.com/mc/game/')):
                    self.download_link_temp.append(temp.get('href'))
        self.versions['getbukkit-craftbukkit'] = {}
        for temp in range(len(self.versions_temp)):
            # print(self.versions_temp[temp])
            # print(self.sizes_temp[temp])
            self.versions['getbukkit-craftbukkit'][self.versions_temp[temp]] = {
                'size': self.sizes_temp[temp],
                'release-data': self.release_data_temp[temp],
                'link': self.download_link_temp[temp],
            }

sl_settings = ServerLauncherSettings()
test = LinkHandler(sl_settings)
# test.get_vanilla_link_list_via_getbukkit()
# test.get_spigot_link_list_via_getbukkit()
test.get_craftbukkit_link_list_via_getbukkit()
print(test.versions)