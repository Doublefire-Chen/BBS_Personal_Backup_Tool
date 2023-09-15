# -*- coding: utf-8 -*-
# @Author: Bigscience
# @email: 站内信
# @Date:   2023-09-13 15:34:05
# @Last Modified by:   Doublefire.Chen
# @Last Modified time: 2023-09-15 14:07:12
"""RED = '\033[31m'
SKYBLUE = '\033[36m'
GREEN = '\033[32m'
BOLD = '\033[1m'
END_COLOR = '\033[0m'"""

RED = '\033[1;31m'
SKYBLUE = '\033[1;36m'
GREEN = '\033[1;32m'
BOLD = '\033[1m'
END_COLOR = '\033[0m'


class Print(object):

    # 打印信息

    def SkyBlue_print(self, text):
        print(SKYBLUE + text + END_COLOR)

    def Green_print(self, text):
        print(GREEN + text + END_COLOR)

    def Red_print(self, text):
        print(RED + text + END_COLOR)

    def Bold_print(self, text):
        print(BOLD + text + END_COLOR)

    def welcome(self):  # 欢迎界面
        print('''\033[1;31mBBBBB   DDDDD   WW           WW MM    MM 
BB   B  DD  DD   WW         WW  MMM  MMM 
BBBBBB  DD   DD   WW   W   WW   MM MM MM 
BB   BB DD   DD    WW WWW WW    MM    MM 
BBBBBB  DDDDDD      WW   WW     MM    MM                 
''',
              end='')
        self.Green_print('''    ____             __             
   / __ )____ ______/ /____  ______ 
  / __  / __ `/ ___/ //_/ / / / __ \\
 / /_/ / /_/ / /__/ ,< / /_/ / /_/ /
/_____/\__,_/\___/_/|_|\__,_/ .___/ 
                           /_/      
''')
        self.SkyBlue_print("欢迎使用北大未名BBS备份工具！")
