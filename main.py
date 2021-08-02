# By. woshishabi

import os

import requests
from bs4 import BeautifulSoup
import re

import easygui

class ServerLauncherSettings():
    def __init__(self):
        # 版本设置 / Version Settings
        self.server_dir = '.server'
        # 源设置 / Source Settings
        self.source = {
            'vanilla':'https://getbukkit.org/download/vanilla',
            'spigot':'https://getbukkit.org/download/spigot',
            'craftbukkit':'https://getbukkit.org/download/craftbukkit',
        }

class Server():
    def __init__(self, edition, version, sl_settings, name=None):
        # 检测是否给出服务器配置名称
        # 如果未给出则根据服务端类型、版本创建一个名字
        if name:
            self.name = name
        else:
            self.name = f'{edition}-{version}'

        self.edition = edition
        self.version = version
        self.sl_settings = sl_settings
        
        self.server_path = f'{self.sl_settings.server_dir}/{self.name}'
    def download(self, links):
        # 检测是否存在存储目录，如果没有则创建
        if os.path.exists(self.sl_settings.server_dir):
            pass
        else:
            os.mkdir(self.sl_settings.server_dir)
        # 创建配置目录
        if not os.path.exists(self.sl_settings):
            os.mkdir(self.server_path)
        # 解析getbukkit信息网页获取下载链接
        self.page_request = requests.get(links[self.edition][self.version])
        print(f'[LOG] Getting getbukkit website, status code: {self.page_request.status_code}')
        self.soup = BeautifulSoup(self.page_request.text, 'html.parser')
        for a in self.soup.find_all('a'):
            if a.get('href').startswith('https://launcher.mojang.com/v1/objects/'):
                self.download_link = a.get('href')
                # print(self.download_link)
                break
        self.file_request = requests.get(self.download_link, stream=True)
        with open(f'{self.server_path}/{self.name}.jar', mode='wb') as jar:
            for chunk in self.file_request.iter_content(chunk_size=2048):
                if chunk:
                    jar.write(chunk)
    def start(self):
        working_dir = os.getcwd()
        os.chdir(self.server_path)
        os.system(f'java -Xmx2G -jar {self.name}.jar')
        os.chdir(working_dir)

class LinkHandler():
    def __init__(self, sl_settings):
        self.sl_settings = sl_settings
        self.getbukkit_requests = {}
        self.soups = {}
        self.versions = {}
        self.sizes = {}
        self.release_date = {}
        self.getbukkit_links = {}
        self.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    def resolveVanilla(self):
        # 解析原版服务端数据
        # 获取getbukkit网站数据
        self.getbukkit_requests['vanilla'] = requests.get(self.sl_settings.source['vanilla'])
        print(f'[LOG] Getting getbukkit data of vanilla, status code: {self.getbukkit_requests["vanilla"].status_code}')
        # BeautifulSoup 解析
        self.soups['vanilla'] = BeautifulSoup(self.getbukkit_requests['vanilla'].text, 'html.parser')
        # 获取版本列表
        self.versions['vanilla'] = []
        for temp in self.soups['vanilla'].find_all('h2'):
            self.versions['vanilla'].append(str(temp)[4:-5])
        # 获取服务端文件大小、发布日期
        self.sizes_temp = []
        self.release_date_temp = []
        for temp in self.soups['vanilla'].find_all('h3'):
            # 去除HTML标签
            temp = str(temp[4:-5])
            # print(temp)
            # 正则表达式匹配大小
            if (re.match(r'^[0-9].[0-9] MB$', temp, re.I|re.M) 
                or re.match(r'^[0-9].[0-9][0-9] MB$', temp, re.I|re.M) 
                or re.match(r'^[0-9][0-9].[0-9] MB$', temp, re.I|re.M) 
                or re.match(r'^[0-9][0-9].[0-9][0-9] MB$', temp, re.I|re.M)):
                self.sizes_temp.append(temp)
            else:
            # 匹配发布时间
                for weekday in self.weekdays:
                    if weekday in temp:
                        self.release_date_temp.append(temp)
                        break
        # 获取下载信息页链接
        self.getbukkit_links_temp = []
        for temp in self.soups['vanilla'].find_all('a'):
            if temp.get('href').startswith('https://getbukkit.org/get/'):
                self.getbukkit_links_temp.append(temp.get('href'))
        # 合并数据
        self.sizes['vanilla'] = dict(zip(self.versions['vanilla'], self.sizes_temp))
        self.release_date['vanilla'] = dict(zip(self.versions['vanilla'], self.release_date_temp))
        self.getbukkit_links['vanilla'] = dict(zip(self.versions['vanilla'], self.getbukkit_links_temp))
    def resolveSpigot(self):
        # 解析原版服务端数据
        # 获取getbukkit网站数据
        self.getbukkit_requests['spigot'] = requests.get(self.sl_settings.source['spigot'])
        print(f'[LOG] Getting getbukkit data of spigot, status code: {self.getbukkit_requests["spigot"].status_code}')
        # BeautifulSoup 解析
        self.soups['spigot'] = BeautifulSoup(self.getbukkit_requests['spigot'].text, 'html.parser')
        # 获取版本列表
        self.versions['spigot'] = []
        for temp in self.soups['spigot'].find_all('h2'):
            self.versions['spigot'].append(str(temp)[4:-5])
        # 获取服务端文件大小、发布日期
        self.sizes_temp = []
        self.release_date_temp = []
        for temp in self.soups['spigot'].find_all('h3'):
            # 去除HTML标签
            temp = str(temp[4:-5])
            # print(temp)
            # 正则表达式匹配大小
            if (re.match(r'^[0-9][0-9].[0-9] MB$', temp, re.I|re.M) 
                or re.match(r'^[0-9][0-9].[0-9][0-9] MB$', temp, re.I|re.M) 
                or re.match(r'^[0-9][0-9].[0-9][0-9]$', temp, re.I|re.M)):
                self.sizes_temp.append(temp)
            else:
            # 匹配发布时间
                for weekday in self.weekdays:
                    if weekday in temp:
                        self.release_date_temp.append(temp)
                        break
        # 获取下载信息页链接
        self.getbukkit_links_temp = []
        for temp in self.soups['spigot'].find_all('a'):
            if temp.get('href').startswith('https://getbukkit.org/get/'):
                self.getbukkit_links_temp.append(temp.get('href'))
        # 合并数据
        self.sizes['spigot'] = dict(zip(self.versions['spigot'], self.sizes_temp))
        self.release_date['spigot'] = dict(zip(self.versions['spigot'], self.release_date_temp))
        self.getbukkit_links['spigot'] = dict(zip(self.versions['spigot'], self.getbukkit_links_temp))
    def resolveCraftBukkit(self):
        # 解析原版服务端数据
        # 获取getbukkit网站数据
        self.getbukkit_requests['craftbukkit'] = requests.get(self.sl_settings.source['craftbukkit'])
        print(f'[LOG] Getting getbukkit data of CraftBukkit, status code: {self.getbukkit_requests["craftbukkit"].status_code}')
        # BeautifulSoup 解析
        self.soups['craftbukkit'] = BeautifulSoup(self.getbukkit_requests['rcaftbukkit'].text, 'html.parser')
        # 获取版本列表
        self.versions['craftbkkit'] = []
        for temp in self.soups['craftbukkit'].find_all('h2'):
            self.versions['craftbukkit'].append(str(temp)[4:-5])
        # 获取服务端文件大小、发布日期
        self.sizes_temp = []
        self.release_date_temp = []
        for temp in self.soups['craftbukkit'].find_all('h3'):
            # 去除HTML标签
            temp = str(temp[4:-5])
            # print(temp)
            # 正则表达式匹配大小
            if (re.match(r'^[0-9].[0-9][0-9] MB$', temp, re.I|re.M) 
                or re.match(r'^[0-9][0-9].[0-9] MB$', temp, re.I|re.M) 
                or re.match(r'^[0-9][0-9].[0-9][0-9] MB$', temp, re.I|re.M)):
                self.sizes_temp.append(temp)
            else:
            # 匹配发布时间
                for weekday in self.weekdays:
                    if weekday in temp:
                        self.release_date_temp.append(temp)
                        break
        # 获取下载信息页链接
        self.getbukkit_links_temp = []
        for temp in self.soups['craftbukkit'].find_all('a'):
            if temp.get('href').startswith('https://getbukkit.org/get/'):
                self.getbukkit_links_temp.append(temp.get('href'))
        # 合并数据
        self.sizes['craftbukkit'] = dict(zip(self.versions['craftbukkit'], self.sizes_temp))
        self.release_date['craftbukkit'] = dict(zip(self.versions['craftbukkit'], self.release_date_temp))
        self.getbukkit_links['craftbukkit'] = dict(zip(self.versions['craftbukkit'], self.getbukkit_links_temp))

class ServerLauncherGUI():
    def __init__(self):
        self.on_start()
    def on_start(self):
        easygui.msgbox(msg='\t\t\t\t我的世界开服工具\n\t\t\t\tBy. woshishabi', 
                        title='我的世界开服工具  By. woshishabi', ok_button='开始')
    def on_choice(self):
        pass
    
if __name__ == '__main__':
    sl_settings = ServerLauncherSettings()
    root = ServerLauncherGUI()
    test = Server('vanilla', '1.17.1', sl_settings)
    test.start()
