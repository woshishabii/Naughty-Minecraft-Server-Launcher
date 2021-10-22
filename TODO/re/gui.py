import time
import tkinter
import tkinter.messagebox
import os
import requests
from bs4 import BeautifulSoup
import easygui
from retry import retry
import multitasking
import signal

import settings
import link_handler

class ServerLauncherGUI:
    def __init__(self, sl_settings: settings.ServerLauncherSettings):
        self.sl_settings = sl_settings

        if not os.path.exists(self.sl_settings.versions_path):
            os.mkdir(self.sl_settings.versions_path)

        self.versions = os.listdir(self.sl_settings.versions_path)

        if len(self.versions):
            self.current_version = self.versions[0]
        else:
            self.current_version = None

        self.root = tkinter.Tk()
        self.root.geometry('500x400')
        self.root.title(self.sl_settings.title)

        self.currentVersionVar = tkinter.StringVar()
        self.LabelSelectedVersion = tkinter.Label(self.root,
                                                  textvariable=self.currentVersionVar,
                                                  bg='#116FCE',
                                                  fg='white',
                                                  font=('Microsoft Yahei', 12),
                                                  width=50,
                                                  height=2)

        self.currentVersionVar.set(f'当前版本：{self.current_version}')
        self.LabelSelectedVersion.pack()
        # 切换版本 Button
        self.ButtonChangeVersion = tkinter.Button(self.root,
                                                  text='切换版本',
                                                  command=self.change_version,
                                                  width=30,
                                                  height=2)
        self.ButtonChangeVersion.pack()
        # 下载服务器 Button
        self.ButtonDownloadVersion = tkinter.Button(self.root,
                                                    text='下载服务端',
                                                    command=self.download_version,
                                                    width=30,
                                                    height=2)
        self.ButtonDownloadVersion.pack()
        # 启动服务器 Button
        self.ButtonStartServer = tkinter.Button(self.root,
                                                text='启动服务器',
                                                command=self.run_version,
                                                width=30,
                                                height=2)
        self.ButtonStartServer.pack()

    def change_version(self):
        self.ChangeVersionWindow = tkinter.Toplevel()
        self.ChangeVersionWindow.title('切换版本')
        self.ListBoxSelectVersion = tkinter.Listbox(self.ChangeVersionWindow)
        self.versionList = os.listdir(self.sl_settings.versions_path)
        # print(self.versionList)
        for temp in self.versionList:
            self.ListBoxSelectVersion.insert('end', temp)
        self.ListBoxSelectVersion.pack()
        self.ButtonSelectVersionSubmit = tkinter.Button(self.ChangeVersionWindow,
                                                        text='确定',
                                                        width=20,
                                                        height=2,
                                                        command=self.submitSelectVersion)
        self.ButtonSelectVersionSubmit.pack()

    def submitSelectVersion(self):
        self.current_version = self.ListBoxSelectVersion.get(self.ListBoxSelectVersion.curselection())
        self.currentVersionVar.set(f'当前版本：{self.current_version}')
        self.ChangeVersionWindow.destroy()

    def download_version(self):
        self.DownloadVersionWindow = tkinter.Toplevel()
        self.DownloadVersionsVar = tkinter.StringVar()
        self.DownloadVersionWindow.title('下载服务端')
        self.ListBoxSelectDownloadPlatform = tkinter.Listbox(self.DownloadVersionWindow,
                                                             width=30)
        self.download_link_handler = link_handler.LinkHandler(self.sl_settings)
        for temp in self.download_link_handler.available_sources:
            self.ListBoxSelectDownloadPlatform.insert('end', temp)
        self.ListBoxSelectDownloadPlatform.bind('<Double-Button-1>', self.update_download_version_var)
        self.ListBoxSelectDownloadPlatform.pack()
        self.ListBoxSelectDownloadVersion = tkinter.Listbox(self.DownloadVersionWindow,
                                                            listvariable=self.DownloadVersionsVar,
                                                            width=30)
        self.ListBoxSelectDownloadVersion.pack()
        self.ButtonStartDownload = tkinter.Button(self.DownloadVersionWindow,
                                                  text='开始下载',
                                                  width=30,
                                                  height=2,
                                                  command=self.download_version_start)
        self.ButtonStartDownload.pack()

    def update_download_version_var(self, event):
        self.platform_choice = self.ListBoxSelectDownloadPlatform.get(self.ListBoxSelectDownloadPlatform.curselection())
        if self.platform_choice == 'getbukkit-vanilla':
            self.download_link_handler.get_vanilla_link_list_via_getbukkit()
            self.DownloadVersionsVar.set(list(self.download_link_handler.versions['getbukkit-vanilla'].keys()))
        elif self.platform_choice == 'getbukkit-spigot':
            self.download_link_handler.get_spigot_link_list_via_getbukkit()
            self.DownloadVersionsVar.set(list(self.download_link_handler.versions['getbukkit-spigot'].keys()))
        elif self.platform_choice == 'getbukkit-craftbukkit':
            self.download_link_handler.get_craftbukkit_link_list_via_getbukkit()
            self.DownloadVersionsVar.set(list(self.download_link_handler.versions['getbukkit-craftbukkit'].keys()))
        elif self.platform_choice in ['mojang-vanilla-old_alpha', 'mojang-vanilla-snapshot', 'mojang-vanilla-release']:
            self.download_link_handler.get_vanilla_link_list_via_mojang()
            self.DownloadVersionsVar.set(list(self.download_link_handler.versions[self.platform_choice]))

    def download_version_start(self):
        self.version_choice = self.ListBoxSelectDownloadVersion.get(self.ListBoxSelectDownloadVersion.curselection())

        if self.platform_choice in ['getbukkit-vanilla', 'getbukkit-spigot', 'getbukkit-craftbukkit']:
            self.getbukkit_request = requests.get(self.download_link_handler.versions[self.platform_choice][self.version_choice]['page-link'])
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
            if self.download_request.status_code == 200:
                self.DownloadVersionName = easygui.enterbox(msg='输入新版本名称：', title='下载新版本',
                                                            default=f'{self.platform_choice[10:]}-{self.version_choice}')
                if self.DownloadVersionName == None:
                    self.DownloadVersionProgressWindow.destroy()
                    self.DownloadVersionWindow.destroy()
                    return
                try:
                    os.mkdir(f'{self.sl_settings.versions_path}/{self.DownloadVersionName}')
                    os.mkdir(f'{self.sl_settings.versions_path}/{self.DownloadVersionName}/server')
                except:
                    tkinter.messagebox.showerror(title='文件夹已存在', message=f'{self.DownloadVersionName}已存在')
                    self.DownloadVersionProgressWindow.destroy()
                    self.DownloadVersionWindow.destroy()
                    return
                def get_file_size(url: str, raise_error: bool = False) -> int:
                    self.response = requests.head(url)
                    self.size= self.response.headers.get('Content-Length')
                    if (self.size == None) and (raise_error == True):
                        raise ValueError('该文件不支持多线程分段下载！')
                    return int(self.size)
                self.f = open(f'{self.sl_settings.versions_path}/{self.server_name}/server/{self.server_name}.jar', 'wb')
                self.file_size = get_file_size(temp.get('href'))

                @retry(tries=self.sl_settings.retries)
                @multitasking.task
                def start_download(start: int, end: int) -> None:
                    _headers = self.sl_settings.headers.copy()
                    _headers['Range'] = f'bytes={start}-{end}'
                    self.response = session.get(temp.get('href'), headers=_headers, stream=True)
                    chunks = []
                    for chunk in self.response.iter_content(chunk_size=self.sl_settings.chunk_size):
                        chunks.append(chunk)
                        print(self.sl_settings.chunk_size)
                    self.f.seek(start)
                    for chunk in chunks:
                        self.f.write(chunk)
                    del chunks

                session = requests.Session()
                each_size = min(each_size, self.file_size)

                '''
                self.DownloadVersionProgressWindow = tkinter.Toplevel()
                self.DownloadVersionProgressWindow.title(f'正在下载：{self.platform_choice} - {self.version_choice}')
                self.DownloadVersionProgressWindow.geometry('630x150')
                self.DownloadVersionProgressLabel = tkinter.Label(self.DownloadVersionProgressWindow, text='下载进度')
                self.DownloadVersionProgressLabel.place(x=50, y=60)
                self.DownloadVersionProgressCanvas = tkinter.Canvas(self.DownloadVersionProgressWindow,
                                                                    width=465,
                                                                    height=22,
                                                                    bg='white')
                self.DownloadVersionProgressCanvas.place(x=110, y=60)
                self.DownloadVersionProgressBar = self.DownloadVersionProgressCanvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
                self.DownloadVersionName = easygui.enterbox(msg='输入新版本名称：', title='下载新版本', default=f'{self.platform_choice[10:]}-{self.version_choice}')
                if self.DownloadVersionName == None:
                    self.DownloadVersionProgressWindow.destroy()
                    self.DownloadVersionWindow.destroy()
                    return
                try:
                    os.mkdir(f'{self.sl_settings.versions_path}/{self.DownloadVersionName}')
                    os.mkdir(f'{self.sl_settings.versions_path}/{self.DownloadVersionName}/server')
                except:
                    tkinter.messagebox.showerror(title='文件夹已存在', message=f'{self.DownloadVersionName}已存在')
                    self.DownloadVersionProgressWindow.destroy()
                    self.DownloadVersionWindow.destroy()
                    return
                '''



    def run_version(self):
        if self.current_version == None:
            return
        else:
            self.working_directory = os.getcwd()
            os.chdir(f'{self.sl_settings.versions_path}/{self.current_version}/server')
            os.system(f'start {self.sl_settings.java_path} -Xms1G -Xmx2G -jar {self.current_version}.jar nogui')
            os.chdir(self.working_directory)

