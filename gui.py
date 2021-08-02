import easygui
import easygui

class ServerLauncherGUI():
    def __init__(self):
        self.onStart()
    def onStart(self):
        easygui.msgbox(msg="\t\t\t欢迎使用我的世界服务器启动器，\n\t\t\tBy. woshishabi", title='我的世界服务器启动器', ok_button='开始')
        self.checkEvents()
    def checkEvents(self):
        choice = easygui.choicebox(msg='启动器操作', title='我的世界服务器启动器 By. woshishabi', choices=['下载服务端','启动服务器'], preselect=0)
        # print(choice)


Test = ServerLauncherGUI()