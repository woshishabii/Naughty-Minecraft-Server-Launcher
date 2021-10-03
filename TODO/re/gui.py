import tkinter
import os

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
        pass

    def run_version(self):
        pass

