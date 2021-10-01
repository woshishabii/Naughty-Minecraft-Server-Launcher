class ServerLauncherSettings:
    def __init__(self):
        # 项目信息 / Projct Info
        self.version = ['ALpha', '0.0.3']
        self.name = 'Naughty Minecraft Server Launcher'
        self.author = 'woshishabi'
        # 用户界面设置 / GUI settings
        self.title = f'{self.name} {self.version}'
        # 默认版本目录 / Default Versions Directory
        self.versions_path = '.server'
        # 下载源 / Download Source
        self.sources = {
            'getbukkit-vanilla': 'https://getbukkit.org/download/vanilla',
            'getbukkit-spigot': 'https://getbukkit.org/download/spigot',
            'getbukkit-craftbukkit': 'https://getbukkit.org/download/craftbukkit',
        }
        # 原版服务器配置翻译 -> server.properties / Server Properties Translate
        self.vanillaConfigTranslate = {
            'enable-jmx-monitoring': '通过JMX检测服务器每刻耗时',
            'rcon.port': 'RCON远程访问端口',
            'gamemode': '新玩家的游戏模式',
            'enable-command-block': '启用命令方块',
            'enable-query': '允许使用GameSpy4协议的服务器监听器，用于获取服务器信息',
            'level-name': '世界名称及存档文件夹名称',
            'motd': '玩家客户端在多人游戏服务器列表中现实的服务器信息',
            'query.port': '设置监听服务器的端口号',
            'pvp': '开启PVP',
            'difficulty': '游戏难度',
            'network-compression-threshold': '服务器数据包压缩限额',
            'require-resource-pack': '强制使用服务器提供的材质包',
            'max-tick-time': '每tick最长时间（超时看门狗将会强制关闭服务器）',
            'use-native-transport': '使用针对Linux平台的数据包收发优化',
            'max-players': '服务器同时容纳最大玩家数量',
            'online-mode': '是否查验玩家登录验证信息(是否允许盗版玩家登录)',
            'enable-status': '是否使服务器在服务器列表中显示为在线的',
            'allow-flight': '允许玩家在安装添加飞行功能的mod前提下在生存模式飞行',
            'broadcast-rcon-to-ops': '向所有在线OP发送通知RCON执行的命令输出',
            'view-distance': '设置服务端发送给客户端的世界数据量，也就是设置玩家各个方向上的区块数量（半径）决定服务器的视距',
            'server-ip': '将服务器与一个特定IP绑定，建议留空',
            'resource-pack-prompt': '用于在强制使用服务器材质包时在资源包提示界面显示自定义信息（可包含多行文本）',
            'allow-nether': '允许玩家进入下界',
            'server-port': '改变服务器监听的端口号',
            'enable-rcon': '是否允许远程访问服务器控制台',
            'sync-chunk-writes': '是否以同步模式写入区块文件',
            'op-permission-level': '设置使用/op命令式OP的权限等级',
            'prevent-proxy-connections': '如果服务器发送的ISP/AS和Mojang的验证服务器的不一样，玩家就会被踢出',
            'resource-pack': '可输入指向一个资源包的URL,玩家可选择是否使用改资源包（应在:和=钱添加反斜线）',
            'entity-broadcast-range-percentage': '控制实体需要距离玩家多近才会将数据包发给客户端',
            'rcon.password': 'RCON远程访问的密码',
            'player-idle-timeout': '玩家挂机自动踢出时间',
            'force-gamemode': '玩家重新登录时强制设为默认游戏模式',
            'rate-limit': '玩家被踢出服务期前，可以发送的数据包数量',
            'hardcore': '忽略难度设置设为hard，死后自动切换为旁观模式(单机极限模式)',
            'white-list': '启用服务器的白名单，op无需加入',
            'broadcast-console-to-ops': '向所有在线OP发送执行命令的输出',
            'spawn-npcs': '是否生成村民',
            'spawn-animals': '是否生成动物',
            'snooper-enabled': '是否允许服务端定期发送统计数据到http://snoop.minecraft.net',
            'function-permission-level': '设定函数的默认权限模式',
            'spawn-monsters': '是否生成攻击性生物',
            'enforce-whitelist': '在服务器上强制执行白名单',
            'resource-pack-sha1': '资源包的SHA-1值，必须使用小写十六进制，用于验证资源包的完整性',
            'spawn-protection': '保护出生点（2x+1）',
            'max-world-size': '设置可让世界边界获得的最大半径值',
            'debug': '调试模式',
        }
        # Spigot 服务器配置翻译 -> spigot.yml / Spigot Properties Translate
        self.spigotConfigTranslate = {
            'config-version': '配置文件版本',
            'settings': '系统设置',
            'messages': '输出信息',
            'stats': '标志',
            'commands': '命令',
            'advancements': '成就',
            'players': '玩家',
            'world-settings': '世界设置',
            'tab-complete': 'TAB补全需要输入的字数',
            'send-namespaced': 'TAB时显示命名空间(如/minecraft:tp)',
            'silent-commandblock-console': '是否将命令方块输出到聊天栏',
            'log': '是否将玩家提交的指令记录在日志中',
            'spam-exclusions': '不受防刷屏影响的指令',
            'replace-commands': '使用原版行为而不是spigot优化后的行为',
        }
