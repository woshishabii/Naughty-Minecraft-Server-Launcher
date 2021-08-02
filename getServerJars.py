# By. woshishabi

import requests
from bs4 import BeautifulSoup
import re

class LinkHandler():
    def __init__(self):
        self.source = {
            'vanilla':'https://getbukkit.org/download/vanilla',
            'spigot':'https://getbukkit.org/download/spigot',
        }
        self.data = {}
        self.soups = {}
        self.versions = {}
        self.sizes = {}
        self.release_date = {}
        self.pagelink = {}
        self.links = {}
        self.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    def resolveVanillaLinks(self):
        # Get data of the getbukkit website and instance it into a BeautifulSoup object
        self.data['vanilla'] = requests.get(self.source['vanilla'])
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

''' 测试程序
test = LinkHandler()
test.resolveVanillaLinks()
test.resolveSpigotLinks

# print(test.versions)
# print(test.sizes)
# print(test.release_date)
# print(test.links)

test = LinkHandler()
test.resolveVanillaLinks()
test.resolveSpigotLinks()

with open('versions.json', mode='w') as f:
    f.write(str(test.versions))

with open('sizes.json', mode='w') as f:
    f.write(str(test.sizes))

with open('release_date.json', mode='w') as f:
    f.write(str(test.release_date))

with open('links.json', mode='w') as f:
    f.write(str(test.links))
'''