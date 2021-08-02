# By. woshishabi

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
        self.pagelink = {}
        self.links = {}
        self.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

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
        self.sizes['vanilla'] = []
        self.release_date['vanilla'] = []
        for temp in self.soups['vanilla'].find_all('h3'):
            temp = str(temp)[4:-5]
            # print(temp)
            if re.match(r'^[0-9][0-9].[0-9] MB$', temp, re.I|re.M) or re.match(r'^[0-9].[0-9] MB$', temp, re.I|re.M) or re.match(r'^[0-9][0-9].[0-9][0-9] MB$', temp, re.I|re.M) or re.match(r'^[0-9].[0-9][0-9] MB$', temp, re.I|re.M):
                self.sizes['vanilla'].append(temp)
            else:
                for weekday in self.weekdays:
                    if weekday in temp:
                        self.release_date['vanilla'].append(temp)
        self.links['vanilla'] = []
        for temp in self.soups['vanilla'].find_all('a'):
            if temp.get('href').startswith('https://getbukkit.org/get/'):
                self.links['vanilla'].append(temp.get('href'))

    def resolveSpigotLinks(self):
        # Get data of the getbukkit website and instance it into a BeautifulSoup object
        self.data['spigot'] = requests.get(self.source['spigot'])
        print(f"[LOG] Spigot status code {self.data['spigot'].status_code}")
        self.soups['spigot'] = BeautifulSoup(self.data['spigot'].text, 'html.parser')
        # Get version list
        self.versions['spigot'] = []
        for temp in self.soups['spigot'].find_all('h2'):
            self.versions['spigot'].append(str(temp)[4:-5])
        self.sizes['spigot'] = []
        self.release_date['spigot'] = []
        for temp in self.soups['spigot'].find_all('h3'):
            temp = str(temp)[4:-5]
            # print(temp)
            if re.match(r'^[0-9][0-9].[0-9] MB$', temp, re.I|re.M) or re.match(r'^[0-9][0-9].[0-9][0-9] MB$', temp, re.I|re.M) or re.match(r'^[0-9][0-9].[0-9][0-9]$', temp, re.I|re.M):
                self.sizes['spigot'].append(temp)
            else:
                for weekday in self.weekdays:
                    if weekday in temp:
                        self.release_date['spigot'].append(temp)
        self.links['spigot'] = []
        for temp in self.soups['spigot'].find_all('a'):
            if temp.get('href').startswith('https://getbukkit.org/get/'):
                self.links['spigot'].append(temp.get('href'))

    def resolveCraftBukkitLinks(self):
        # Get data of the getbukkit website and instance it into a BeautifulSoup object
        self.data['craftbukkit'] = requests.get(self.source['craftbukkit'])
        print(f"[LOG] CraftBukkit status code : {self.data['craftbukkit'].status_code}")
        self.soups['craftbukkit'] = BeautifulSoup(self.data['craftbukkit'].text, 'html.parser')
        # Get version list
        self.versions['craftbukkit'] = []
        for temp in self.soups['craftbukkit'].find_all('h2'):
            self.versions['craftbukkit'].append(str(temp)[4:-5])
        self.sizes['craftbukkit'] = []
        self.release_date['craftbukkit'] = []
        for temp in self.soups['craftbukkit'].find_all('h3'):
            temp = str(temp)[4:-5]
            # print(temp)
            if re.match(r'^[0-9][0-9].[0-9] MB$', temp, re.I|re.M) or re.match(r'^[0-9][0-9].[0-9][0-9] MB$', temp, re.I|re.M) or re.match(r'^[0-9].[0-9][0-9] MB$', temp, re.I|re.M):
                self.sizes['craftbukkit'].append(temp)
            else:
                for weekday in self.weekdays:
                    if weekday in temp:
                        self.release_date['craftbukkit'].append(temp)
        self.links['craftbukkit'] = []
        for temp in self.soups['craftbukkit'].find_all('a'):
            if temp.get('href').startswith('https://getbukkit.org/get/'):
                self.links['craftbukkit'].append(temp.get('href'))


''' 测试程序
test = LinkHandler()

# print(test.versions)
# print(test.sizes)
# print(test.release_date)
# print(test.links)

with open('versions.py', mode='w') as f:
    f.write(str(test.versions))

with open('sizes.py', mode='w') as f:
    f.write(str(test.sizes))

with open('release_date.py', mode='w') as f:
    f.write(str(test.release_date))

with open('links.py', mode='w') as f:
    f.write(str(test.links))
'''