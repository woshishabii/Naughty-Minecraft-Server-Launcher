# By. woshishabi

# 本程序基于bug运行，请勿瞎改
# This program is based on bug, please do not change it without thinking

import os
import re
import sys

import easygui
import requests
from bs4 import BeautifulSoup

class ServerLauncherSettings():
    def __init__(self):
        # 项目信息 / Project Infomation
        self.version = '0.0.1 alpha'
        self.name = '我的世界服务器工具'
        self.author = 'woshishabi'
        # 用户界面设置 / GUI settings
        self.title = f'{self.name} {self.version}'
        # 默认版本设置 / Default Versions Settings
        self.versions_path = '.server'
        # 设置下载源 / Download Source
        self.source = {
            'vanilla':'https://getbukkit.org/download/vanilla',
            'spigot':'https://getbukkit.org/download/spigot',
            'craftbukkit':'https://getbukkit.org/download/craftbukkit',
        }

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
            temp = str(temp)[4:-5]
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
            temp = str(temp)[4:-5]
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
        self.soups['craftbukkit'] = BeautifulSoup(self.getbukkit_requests['craftbukkit'].text, 'html.parser')
        # 获取版本列表
        self.versions['craftbukkit'] = []
        for temp in self.soups['craftbukkit'].find_all('h2'):
            self.versions['craftbukkit'].append(str(temp)[4:-5])
        # 获取服务端文件大小、发布日期
        self.sizes_temp = []
        self.release_date_temp = []
        for temp in self.soups['craftbukkit'].find_all('h3'):
            # 去除HTML标签
            temp = str(temp)[4:-5]
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
    def __init__(self, sl_settings):
        self.sl_settings = sl_settings
        self.got_link = False
        self.versions = os.listdir(self.sl_settings.versions_path)
        if len(self.versions):
            self.current_version = self.versions[0]
            print(f'[LOG] Current Version {self.current_version}')
        else:
            self.current_version = None
    def onStart(self):
        if not os.path.exists(self.sl_settings.versions_path):
            os.mkdir(self.sl_settings.versions_path)
            easygui.msgbox(msg='\t\t\t欢迎使用我的世界服务器工具\n\t\t\tBy. woshishabi', title=self.sl_settings.title, ok_button='开始使用！')
    def choose_function(self):
        self.function = []
        if self.current_version == None:
            self.function.append('未选择服务端')            
        else:
            self.function.append(f'当前选择的服务端: {self.current_version}')
        self.function.append('下载服务端')
        self.function.append('启动服务器')
        self.function.append('尚未完工')
        self.choice = easygui.choicebox(msg='选择操作', title=self.sl_settings.title, choices=self.function, preselect=0)
        print(self.choice)
        if self.choice == f'当前选择的服务端: {self.current_version}':
            self.chooseVersion()
        elif self.choice == '下载服务端':
            self.downloadVersion()
        elif self.choice == '启动服务器':
            self.runVersion(self.current_version)
        elif self.choice == '尚未完工':
            easygui.msgbox(msg='这个项目还没有完成')
        elif self.choice == None:
            sys.exit()
    def downloadVersion(self):
        if not self.got_link:
            self.linkhandler = LinkHandler(self.sl_settings)
            self.linkhandler.resolveVanilla()
            self.linkhandler.resolveSpigot()
            self.linkhandler.resolveCraftBukkit()
            self.got_link = True

        self.editions = list(self.linkhandler.versions.keys())

        self.edition_choice = easygui.choicebox(msg='选择服务端类型', title=self.sl_settings.title,
                                                choices=self.editions, preselect=0)
        if self.edition_choice != None:
            self.versions_info = {}
            for version in self.linkhandler.versions[self.edition_choice]:
                self.versions_info[f'{version} - {self.linkhandler.sizes[self.edition_choice][version]} - {self.linkhandler.release_date[self.edition_choice][version]}'] = version
            self.version_choice = easygui.choicebox(msg='请选择服务端版本', title=self.sl_settings.title, 
                                                    choices=list(self.versions_info.keys()), preselect=0)
            if not self.version_choice:
                return
            print(self.version_choice)
        else:
            return
        self.server_name = easygui.enterbox(msg='请输入新配置的名称', title='创建新配置', default=f'{self.edition_choice}-{self.versions_info[self.version_choice]}')
        try:
            os.mkdir(f'{self.sl_settings.versions_path}/{self.server_name}')
            os.mkdir(f'{self.sl_settings.versions_path}/{self.server_name}/server')
        except:
            easygui.ynbox(msg=f'指定的版本名称已存在，请重新命名\n如果你确定没有创建此版本，请删除{self.sl_settings.versions_path}/{self.server_name}', 
                        title='指定版本名称已存在', 
                        choices=('[<Y>] 确定', '[<C>] 取消'), cancel_choice='[<C>] 取消')
            return
        easygui.msgbox(msg='即将开始下载', title=self.sl_settings.title, ok_button='开始')
        self.getbukkit_request = requests.get(self.linkhandler.getbukkit_links[self.edition_choice][self.versions_info[self.version_choice]])
        # print(self.linkhandler.getbukkit_links[self.edition_choice][self.versions_info[self.version_choice]])
        self.getbukkit_soup = BeautifulSoup(self.getbukkit_request.text, 'html.parser')
        for temp in self.getbukkit_soup.find_all('a'):
            if (temp.get('href').startswith('https://launcher.mojang.com/v1/objects/') 
                or temp.get('href').startswith('https://download.getbukkit.org/spigot/') 
                or temp.get('href').startswith('https://download.getbukkit.org/craftbukkit/') 
                or temp.get('href').startswith('https://cdn.getbukkit.org/craftbukkit/') 
                or temp.get('href').startswith('https://cdn.getbukkit.org/spigot') 
                or temp.get('href').startswith('https://launcher.mojang.com/mc/game/')):
                self.download_request = requests.get(temp.get('href'), stream=True)
                break
            # print(temp.get('href'))
        with open(f'{self.sl_settings.versions_path}/{self.server_name}/server/{self.server_name}.jar', mode='wb') as jar:
            for chunk in self.download_request.iter_content(chunk_size=1024):
                if chunk:
                    jar.write(chunk)
        self.eula_request = requests.get('https://account.mojang.com/documents/minecraft_eula')
        self.eula_soup = BeautifulSoup(self.eula_request.text, 'html.parser')
        for temp in self.eula_soup.find_all('div', class_='standalone'):
            self.eula_pattern = re.compile(r'<[^>]+>', re.S)
            self.eula_text = self.eula_pattern.sub('', str(temp))
            break
        self.agree_eula = easygui.ynbox(msg=self.eula_text, title='最终用户许可协议', choices=('[<A>] 同意', '[<D>] 不同意'), default_choice='[<D>] 不同意')
        while not self.agree_eula:
            easygui.msgbox(msg='要运行服务端，您必须同意Mojang最终用户许可协议')
            self.agree_eula = easygui.ynbox(msg=self.eula_text, title='最终用户许可协议', choices=('[<A>] 同意', '[<D>] 不同意'), default_choice='[<D>] 不同意')
            print(self.agree_eula)
        with open(f'{self.sl_settings.versions_path}/{self.server_name}/server/eula.txt', mode='w') as eula:
            eula.write('eula=true')
            self.current_version = self.server_name
    def runVersion(self, name):
        self.working_directory = os.getcwd()
        os.chdir(f'{self.sl_settings.versions_path}/{name}/server')
        os.system(f'java -Xms1G -Xmx2G -jar {name}.jar nogui')
        os.chdir(self.working_directory)
    def chooseVersion(self):
        temp = os.listdir(self.sl_settings.versions_path)
        if len(temp) <= 2:
            temp.append('')
            temp.append('')
        choice = easygui.choicebox(msg='请选择已有的服务端版本', title='选择服务端', choices=temp, preselect=0)
        if choice:
            self.current_version = choice
    def configVersion(self):
        pass

def test():
    sl_settings = ServerLauncherSettings()
    sl_gui = ServerLauncherGUI(sl_settings)

    sl_gui.onStart()
    while True:
        sl_gui.choose_function()

test()
