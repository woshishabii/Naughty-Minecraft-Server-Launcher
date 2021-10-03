import requests
from bs4 import BeautifulSoup
import re
import json

from settings import ServerLauncherSettings


class LinkHandler:
    def __init__(self, sl_settings: ServerLauncherSettings):
        self.sl_settings = sl_settings

        self.requests_object = {}
        self.beautifulsoup_object = {}
        self.versions = {}

        self.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.available_sources = [
            'getbukkit-vanilla',
            'getbukkit-spigot',
            'getbukkit-craftbukkit',
            'mojang-vanilla-old_alpha',
            'mojang-vanilla-snapshot',
            'mojang-vanilla-release',
        ]

    def get_vanilla_link_list_via_getbukkit(self):
        self.requests_object['getbukkit-vanilla'] = requests.get(self.sl_settings.sources['getbukkit-vanilla'])
        print('[LOG]', 'Getbukkit page got! Status: ', self.requests_object['getbukkit-vanilla'].status_code)
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
        # self.download_link_temp = []
        '''
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
                    print(temp.get('href'))
                    self.download_link_temp.append(temp.get('href'))
        '''
        self.versions['getbukkit-vanilla'] = {}
        for temp in range(len(self.versions_temp)):
            # print(self.versions_temp[temp])
            self.versions['getbukkit-vanilla'][self.versions_temp[temp]] = {
                'size': self.sizes_temp[temp],
                'release-data': self.release_data_temp[temp],
                'page-link': self.getbukkit_link_temp[temp],
            }

    def get_spigot_link_list_via_getbukkit(self):
        self.requests_object['getbukkit-spigot'] = requests.get(self.sl_settings.sources['getbukkit-spigot'])
        print('[LOG]', 'Getbukkit page got! Status: ', self.requests_object['getbukkit-spigot'].status_code)
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
        '''
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
        '''
        self.versions['getbukkit-spigot'] = {}
        for temp in range(len(self.versions_temp)):
            # print(self.versions_temp[temp])
            # print(self.sizes_temp[temp])
            self.versions['getbukkit-spigot'][self.versions_temp[temp]] = {
                'size': self.sizes_temp[temp],
                'release-data': self.release_data_temp[temp],
                'page-link': self.getbukkit_link_temp[temp],
            }

    def get_craftbukkit_link_list_via_getbukkit(self):
        self.requests_object['getbukkit-craftbukkit'] = requests.get(self.sl_settings.sources['getbukkit-craftbukkit'])
        print('[LOG]', 'Getbukkit page got! Status: ', self.requests_object['getbukkit-craftbukkit'].status_code)
        self.beautifulsoup_object['getbukkit-craftbukkit'] = BeautifulSoup(
            self.requests_object['getbukkit-craftbukkit'].text,
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
        '''
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
        '''
        self.versions['getbukkit-craftbukkit'] = {}
        for temp in range(len(self.versions_temp)):
            # print(self.versions_temp[temp])
            # print(self.sizes_temp[temp])
            self.versions['getbukkit-craftbukkit'][self.versions_temp[temp]] = {
                'size': self.sizes_temp[temp],
                'release-data': self.release_data_temp[temp],
                'page-link': self.getbukkit_link_temp[temp],
            }

    def get_vanilla_link_list_via_mojang(self):
        self.versions_manifest_json_temp = requests.get(self.sl_settings.sources['mojang-vanilla'])
        self.versions_manifest_json = json.loads(self.versions_manifest_json_temp.text)
        # print(len(self.versions_manifest_json['versions']))
        self.versions['mojang-vanilla-old_alpha'] = {}
        self.versions['mojang-vanilla-snapshot'] = {}
        self.versions['mojang-vanilla-release'] = {}
        for temp in self.versions_manifest_json['versions']:
            # print(temp)
            if temp['type'] == 'old_alpha':
                self.versions['mojang-vanilla-old_alpha'][temp['id']] = {
                    'release-data': temp['releaseTime'],
                    'json-link': temp['url'],
                }
            elif temp['type'] == 'snapshot':
                self.versions['mojang-vanilla-snapshot'][temp['id']] = {
                    'release-data': temp['releaseTime'],
                    'json-link': temp['url'],
                }
            elif temp['type'] == 'release':
                self.versions['mojang-vanilla-release'][temp['id']] = {
                    'release-data': temp['releaseTime'],
                    'json-link': temp['url'],
                }


# sl_settings = ServerLauncherSettings()
# test = LinkHandler(sl_settings)
# test.get_vanilla_link_list_via_getbukkit()
# test.get_spigot_link_list_via_getbukkit()
# test.get_craftbukkit_link_list_via_getbukkit()
# test.get_vanilla_link_list_via_mojang()
# print(test.versions)
# print(len(test.versions['mojang-vanilla-release']))
