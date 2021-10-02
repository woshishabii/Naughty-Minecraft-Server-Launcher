import tkinter
import os

import settings

class ServerLauncherGUI:
    def __init__(self, sl_settings: settings.ServerLauncherSettings):
        self.sl_settings = sl_settings


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
                                                command=lambda: self.sl_functions.runVersion(
                                                    self.sl_functions.current_version),
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
        self.ChangeVersionWindow.destroy()
