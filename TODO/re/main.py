# By. woshishabi

# 本程序基于bug运行，不建议做更改
# This program is based on bug, please DO NOT change it without thinking

import gui
import settings

if __name__ == '__main__':
    sl_settings = settings.ServerLauncherSettings()
    main = gui.ServerLauncherGUI(sl_settings)
    main.root.mainloop()
