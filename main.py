# By. woshishabi

# 本程序基于bug运行，请勿瞎改
# This program is based on bug, please DO NOT change it without thinking

import os
import re
import sys
import shutil

import easygui
import requests
from bs4 import BeautifulSoup
import yaml

class PropertyReader():
    def __init__(self, fileName):
        self.fileName = fileName
        self.values = {}
        self.values_temp = []
        self.readAll()
    def readAll(self):
        with open(self.fileName, 'r') as property:
            for temp in property.readlines():
                if not temp.startswith('#'):
                    self.values_temp.append(temp.strip())
        for value in self.values_temp:
            value = value.split('=')
            self.values[value[0]] = value[1]
    def getKey(self, key):
        ''' TODO
        this function may discard the changes'''
        self.readAll()
        try:
            return self.values[key]
        except:
            return None
    def setKey(self, key, value):
        self.readAll()
        self.values[key] = value
    def save(self):
        ''' TODO 
        this function must be ran after self.readAll()
        or it will empty the file
        but it will also discard the changes
        what the fuck
        '''
        with open(self.fileName, mode='w') as property:
            for temp in self.values:
                property.write(f'{temp}={self.values[temp]}\n')
    def __str__(self):
        return self.values

class ServerLauncherSettings():
    def __init__(self):
        # 项目信息 / Project Infomation
        self.version = 'Alpha 0.0.1'
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
        # 服务器配置翻译 / Server Config Translate
        self.vanillaConfigTranslate = {
            'enable-jmx-monitoring':'通过JMX检测服务器每刻耗时',
            'rcon.port':'RCON远程访问端口',
            'gamemode':'新玩家的游戏模式',
            'enable-command-block':'启用命令方块',
            'enable-query':'允许使用GameSpy4协议的服务器监听器，用于获取服务器信息',
            'level-name':'世界名称及存档文件夹名称',
            'motd':'玩家客户端在多人游戏服务器列表中现实的服务器信息',
            'query.port':'设置监听服务器的端口号',
            'pvp':'开启PVP',
            'difficulty':'游戏难度',
            'network-compression-threshold':'服务器数据包压缩限额',
            'require-resource-pack':'强制使用服务器提供的材质包',
            'max-tick-time':'每tick最长时间（超时看门狗将会强制关闭服务器）',
            'use-native-transport':'使用针对Linux平台的数据包收发优化',
            'max-players':'服务器同时容纳最大玩家数量',
            'online-mode':'是否查验玩家登录验证信息(是否允许盗版玩家登录)',
            'enable-status':'是否使服务器在服务器列表中显示为在线的',
            'allow-flight':'允许玩家在安装添加飞行功能的mod前提下在生存模式飞行',
            'broadcast-rcon-to-ops':'向所有在线OP发送通知RCON执行的命令输出',
            'view-distance':'设置服务端发送给客户端的世界数据量，也就是设置玩家各个方向上的区块数量（半径）决定服务器的视距',
            'server-ip':'将服务器与一个特定IP绑定，建议留空',
            'resource-pack-prompt':'用于在强制使用服务器材质包时在资源包提示界面显示自定义信息（可包含多行文本）',
            'allow-nether':'允许玩家进入下界',
            'server-port':'改变服务器监听的端口号',
            'enable-rcon':'是否允许远程访问服务器控制台',
            'sync-chunk-writes':'是否以同步模式写入区块文件',
            'op-permission-level':'设置使用/op命令式OP的权限等级',
            'prevent-proxy-connections':'如果服务器发送的ISP/AS和Mojang的验证服务器的不一样，玩家就会被踢出',
            'resource-pack':'可输入指向一个资源包的URL,玩家可选择是否使用改资源包（应在:和=钱添加反斜线）',
            'entity-broadcast-range-percentage':'控制实体需要距离玩家多近才会将数据包发给客户端',
            'rcon.password':'RCON远程访问的密码',
            'player-idle-timeout':'玩家挂机自动踢出时间',
            'force-gamemode':'玩家重新登录时强制设为默认游戏模式',
            'rate-limit':'玩家被踢出服务期前，可以发送的数据包数量',
            'hardcore':'忽略难度设置设为hard，死后自动切换为旁观模式(单机极限模式)',
            'white-list':'启用服务器的白名单，op无需加入',
            'broadcast-console-to-ops':'向所有在线OP发送执行命令的输出',
            'spawn-npcs':'是否生成村民',
            'spawn-animals':'是否生成动物',
            'snooper-enabled':'是否允许服务端定期发送统计数据到http://snoop.minecraft.net',
            'function-permission-level':'设定函数的默认权限模式',
            'spawn-monsters':'是否生成攻击性生物',
            'enforce-whitelist':'在服务器上强制执行白名单',
            'resource-pack-sha1':'资源包的SHA-1值，必须使用小写十六进制，用于验证资源包的完整性',
            'spawn-protection':'保护出生点（2x+1）',
            'max-world-size':'设置可让世界边界获得的最大半径值',
            'debug':'调试模式',
        }
        self.spigotConfigTranslate = {
            'config-version':'配置文件版本',
            'settings':'系统设置',
            'messages':'输出信息',
            'stats':'标志',
            'commands':'命令',
            'advancements':'成就',
            'players':'玩家',
            'world-settings':'世界设置',
            'tab-complete':'TAB补全需要输入的字数',
            'send-namespaced':'TAB时显示命名空间(如/minecraft:tp)',
            'silent-commandblock-console':'是否将命令方块输出到聊天栏',
            'log':'是否将玩家提交的指令记录在日志中',
            'spam-exclusions':'不受防刷屏影响的指令',
            'replace-commands':'使用原版行为而不是spigot优化后的行为',
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
        if not os.path.exists(self.sl_settings.versions_path):
            os.mkdir(self.sl_settings.versions_path)
            easygui.msgbox(msg='\t\t\t欢迎使用我的世界服务器工具\n\t\t\tBy. woshishabi', title=self.sl_settings.title, ok_button='开始使用！')
        self.versions = os.listdir(self.sl_settings.versions_path)
        self.server_configs = {}
        if len(self.versions):
            self.current_version = self.versions[0]
            print(f'[LOG] Current Version {self.current_version}')
        else:
            self.current_version = None
    def choose_function(self):
        self.function = []
        if self.current_version == None:
            self.function.append('未选择服务端')            
        else:
            self.function.append(f'当前选择的服务端: {self.current_version}')
        self.function.append('下载服务端')
        self.function.append('启动服务器')
        self.function.append('配置服务器')
        self.function.append('删除服务器')
        self.function.append('尚未完工')
        self.choice = easygui.choicebox(msg='选择操作', title=self.sl_settings.title, choices=self.function, preselect=0)
        print(self.choice)
        if self.choice == f'当前选择的服务端: {self.current_version}':
            self.chooseVersion()
        elif self.choice == '下载服务端':
            self.downloadVersion()
        elif self.choice == '启动服务器':
            self.runVersion(self.current_version)
        elif self.choice == '配置服务器':
            self.configVersion()
        elif self.choice == '删除服务器':
            self.removeVersion()
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
        if self.server_name == None:
            return
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
        self.edition_options = []
        # 在这里添加受支持的配置文件 / Add the Config Files that
        if os.path.exists(f'{self.sl_settings.versions_path}/{self.current_version}/server/server.properties'):
            self.edition_options.append('原版设置(Vanilla - server.properties)')
        if os.path.exists(f'{self.sl_settings.versions_path}/{self.current_version}/server/spigot.yml'):
            self.edition_options.append('Spigot服务端设置(spigot.yml)')
        if len(self.edition_options) < 2:
            self.edition_options.append('')
            self.edition_options.append('')
        self.configVersion_choice = easygui.choicebox(msg='选择配置文件', title='配置服务器', choices=self.edition_options, preselect=0)
        if self.configVersion_choice == '原版设置(Vanilla - server.properties)':
            self.vanillaConfigs()
        elif self.configVersion_choice == 'Spigot服务端设置(spigot.yml)':
            self.spigotConfigs()
    def vanillaConfigs(self):
        self.server_configs['vanilla'] = PropertyReader(f'{self.sl_settings.versions_path}/{self.current_version}/server/server.properties')
        while True:
            self.vanillaConfigOptions = {}
            for temp in self.server_configs['vanilla'].values:
                if temp in self.sl_settings.vanillaConfigTranslate.keys():
                    self.vanillaConfigOptions[f'{self.sl_settings.vanillaConfigTranslate[temp]}  当前值为： {self.server_configs["vanilla"].values[temp]}'] = temp
                else:
                    self.vanillaConfigOptions[f'{temp}  当前值为： {self.server_configs["vanilla"].values[temp]}'] = temp
            self.config_choice = easygui.choicebox(msg='服务器配置', title='配置服务器', choices=self.vanillaConfigOptions.keys(), preselect=0)
            if self.config_choice == None:
                return
            self.config = self.vanillaConfigOptions[self.config_choice]
            if self.config == None:
                return
            self.newConfig = easygui.enterbox(msg=f'为{self.config}设置新的值', title='更改配置', default=self.server_configs['vanilla'].values[self.config])
            if self.newConfig == None:
                continue
            self.server_configs['vanilla'].setKey(self.config, self.newConfig)
            self.server_configs['vanilla'].save()
            # print(self.newConfig)
        # print(self.config)
    def spigotConfigs(self):
        while True:
            with open(f'{self.sl_settings.versions_path}/{self.current_version}/server/spigot.yml', mode='r') as spigot:
                self.server_configs['spigot.yml'] = yaml.load(spigot, Loader=yaml.FullLoader)
            self.spigotConfigOptions = {}
            # print(self.server_configs['spigot.yml'])
            for temp in self.server_configs['spigot.yml']:
                print(temp)
                if temp in self.sl_settings.spigotConfigTranslate.keys():
                    self.spigotConfigOptions[f'{self.sl_settings.spigotConfigTranslate[temp]} 当前值为： {self.server_configs["spigot.yml"][temp]}'] = temp
                else:
                    self.spigotConfigOptions[f'{temp} 当前值为： {self.server_configs["spigot.yml"][temp]}'] = temp
            easygui.choicebox(msg='', title='', choices=self.spigotConfigOptions, preselect=0)
    def removeVersion(self):
        if easygui.ynbox(msg=f'你确定要删除这个服务器吗?\n{self.current_version}将会永久失去!(真的很久!)', title='删除服务器', choices=('[<D>]删除', '[<C>]取消'), cancel_choice='[<C>]取消'):
            shutil.rmtree(f'{self.sl_settings.versions_path}/{self.current_version}')
        self.versions = os.listdir(self.sl_settings.versions_path)
        self.server_configs = {}
        if len(self.versions):
            self.current_version = self.versions[0]
            print(f'[LOG] Current Version {self.current_version}')
        else:
            self.current_version = None

def test():
    sl_settings = ServerLauncherSettings()
    sl_gui = ServerLauncherGUI(sl_settings)
    while True:
        sl_gui.choose_function()
def testProperty():
    prop = PropertyReader('server.properties')
    prop.readAll()
    # print(prop.values)
    print(len(prop.values.keys()))
    print(prop.getKey('gamemode'))
    prop.setKey('gamemode', 'creative')
    prop.save()

test()
# testProperty()