# By. woshishabi

import os
import pathlib

import requests
from bs4 import BeautifulSoup
import re

class LinkHandler():
    def __init__(self):
        self.source = {
            'vanilla':'https://getbukkit.org/download/vanilla',
            'spigot':'https://getbukkit.org/download/spigot',
            'craftbukkit':'https://getbukkit.org/download/craftbukkit',
        }
        self.data = {}
        self.soups = {}
        self.versions = {}
        self.sizes = {}
        self.release_date = {}
        self.links = {}
        self.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        self.download_path = '.server'

        self.resolveVanillaLinks()
        self.resolveSpigotLinks()
        self.resolveCraftBukkitLinks()
    
    def resolveVanillaLinks(self):
        # Get data of the getbukkit website and instance it into a BeautifulSoup object
        self.data['vanilla'] = requests.get(self.source['vanilla'])
        print(f"[LOG] Vanilla status code {self.data['vanilla'].status_code}")
        self.soups['vanilla'] = BeautifulSoup(self.data['vanilla'].text, 'html.parser')
        # Get version list
        self.versions['vanilla'] = []
        for temp in self.soups['vanilla'].find_all('h2'):
            self.versions['vanilla'].append(str(temp)[4:-5])
        self.sizes_temp = []
        self.release_date_temp = []
        for temp in self.soups['vanilla'].find_all('h3'):
            temp = str(temp)[4:-5]
            # print(temp)
            if re.match(r'^[0-9][0-9].[0-9] MB$', temp, re.I|re.M) or re.match(r'^[0-9].[0-9] MB$', temp, re.I|re.M) or re.match(r'^[0-9][0-9].[0-9][0-9] MB$', temp, re.I|re.M) or re.match(r'^[0-9].[0-9][0-9] MB$', temp, re.I|re.M):
                self.sizes_temp.append(temp)
            else:
                for weekday in self.weekdays:
                    if weekday in temp:
                        self.release_date_temp.append(temp)
        self.links_temp = []
        for temp in self.soups['vanilla'].find_all('a'):
            if temp.get('href').startswith('https://getbukkit.org/get/'):
                self.links_temp.append(temp.get('href'))
        
        # 将数据与版本合并
        self.sizes['vanilla'] = dict(zip(self.versions['vanilla'], self.sizes_temp))
        self.release_date['vanilla'] = dict(zip(self.versions['vanilla'], self.release_date_temp))
        self.links['vanilla'] = dict(zip(self.versions['vanilla'], self.links_temp))

    def resolveSpigotLinks(self):
        # Get data of the getbukkit website and instance it into a BeautifulSoup object
        self.data['spigot'] = requests.get(self.source['spigot'])
        print(f"[LOG] Spigot status code {self.data['spigot'].status_code}")
        self.soups['spigot'] = BeautifulSoup(self.data['spigot'].text, 'html.parser')
        # Get version list
        self.versions['spigot'] = []
        for temp in self.soups['spigot'].find_all('h2'):
            self.versions['spigot'].append(str(temp)[4:-5])
        self.sizes_temp = []
        self.release_date_temp = []
        for temp in self.soups['spigot'].find_all('h3'):
            temp = str(temp)[4:-5]
            # print(temp)
            if re.match(r'^[0-9][0-9].[0-9] MB$', temp, re.I|re.M) or re.match(r'^[0-9][0-9].[0-9][0-9] MB$', temp, re.I|re.M) or re.match(r'^[0-9][0-9].[0-9][0-9]$', temp, re.I|re.M):
                self.sizes_temp.append(temp)
            else:
                for weekday in self.weekdays:
                    if weekday in temp:
                        self.release_date_temp.append(temp)
        self.links_temp = []
        for temp in self.soups['spigot'].find_all('a'):
            if temp.get('href').startswith('https://getbukkit.org/get/'):
                self.links_temp.append(temp.get('href'))
        
        # 合并数据
        self.sizes['spigot'] = dict(zip(self.versions['spigot'], self.sizes_temp))
        self.release_date['spigot'] = dict(zip(self.versions['spigot'], self.release_date_temp))
        self.links['spigot'] = dict(zip(self.versions['spigot'], self.links_temp))

    def resolveCraftBukkitLinks(self):
        # Get data of the getbukkit website and instance it into a BeautifulSoup object
        self.data['craftbukkit'] = requests.get(self.source['craftbukkit'])
        print(f"[LOG] CraftBukkit status code : {self.data['craftbukkit'].status_code}")
        self.soups['craftbukkit'] = BeautifulSoup(self.data['craftbukkit'].text, 'html.parser')
        # Get version list
        self.versions['craftbukkit'] = []
        for temp in self.soups['craftbukkit'].find_all('h2'):
            self.versions['craftbukkit'].append(str(temp)[4:-5])
        self.sizes_temp = []
        self.release_date_temp = []
        for temp in self.soups['craftbukkit'].find_all('h3'):
            temp = str(temp)[4:-5]
            # print(temp)
            if re.match(r'^[0-9][0-9].[0-9] MB$', temp, re.I|re.M) or re.match(r'^[0-9][0-9].[0-9][0-9] MB$', temp, re.I|re.M) or re.match(r'^[0-9].[0-9][0-9] MB$', temp, re.I|re.M):
                self.sizes_temp.append(temp)
            else:
                for weekday in self.weekdays:
                    if weekday in temp:
                        self.release_date_temp.append(temp)
        self.links_temp = []
        for temp in self.soups['craftbukkit'].find_all('a'):
            if temp.get('href').startswith('https://getbukkit.org/get/'):
                self.links_temp.append(temp.get('href'))
        
        # 合并数据
        self.sizes['craftbukkit'] = dict(zip(self.versions['craftbukkit'], self.sizes_temp))
        self.release_date['craftbukkit'] = dict(zip(self.versions['craftbukkit'], self.release_date_temp))
        self.links['craftbukkit'] = dict(zip(self.versions['craftbukkit'], self.links_temp))

    def downloadVersion(self, edition, version, server_name=None):
        '''
        if os.path.exists(self.download_path):
            pass
        else:
            os.mkdir(self.download_path)
        if server_name:
            server_path = f'{self.download_path}/{server_name}'
        else:
            server_path = f'{self.download_path}/{edition}_{version}'
        if not os.path.exists(server_path):
            os.mkdir(server_path)
        '''
        
        if os.path.exists(self.download_path):
            pass
        else:
            os.mkdir(self.download_path)
        
        if server_name:
            self.server_name = server_name
        else:
            self.server_name = f'{edition}-{version}'
        
        self.server_path = f'{self.download_path}/{self.server_name}'
        
        if os.path.exists(self.server_path):
            pass
        else:
            os.mkdir(self.server_path)

        # 通过getbukkit网页获取Mojang下载链接
        self.page_request = requests.get(self.links[edition][version])
        print(f"[LOG] Getting getbukkit redirect link status code : {self.page_request.status_code}")
        self.page_soup = BeautifulSoup(self.page_request.text, 'html.parser')
        for temp_link in self.page_soup.find_all('a'):
            if temp_link.get('href').startswith('https://launcher.mojang.com/v1/objects/'):
                self.jar_link = temp_link.get('href')
                # print(self.jar_link)
        self.jar_request = requests.get(self.jar_link, stream=True)
        print(f'[LOG] Mojang website status code {self.jar_request.status_code}')
        print('[LOG] Download Started')
        with open(f'{self.server_path}/{self.server_name}.jar', mode='wb') as jar:
            for chunk in self.jar_request.iter_content(chunk_size=1024):
                if chunk:
                    jar.write(chunk)

'''
test = LinkHandler()
'''

'''
# print(test.versions)
# print(test.sizes)
# print(test.release_date)
# print(test.links)
'''

'''
with open('versions.py', mode='w') as f:
    f.write(str(test.versions))
with open('sizes.py', mode='w') as f:
    f.write(str(test.sizes))
with open('release_date.py', mode='w') as f:
    f.write(str(test.release_date))
with open('links.py', mode='w') as f:
    f.write(str(test.links))
'''

'''
test.downloadVersion('vanilla', '1.17.1')
'''