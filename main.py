# -*- coding: utf-8 -*-
# @Author: Bigscience
# @email: 站内信
# @Date:   2023-09-13 15:34:05
# @Last Modified by:   Doublefire.Chen
# @Last Modified time: 2023-09-15 14:07:12
import getpass
from urllib.parse import unquote
from BBS import BBS
from print import Print
import re


class Menu(BBS):

    def __init__(self, username, password):
        super().__init__(username, password)
        self.username = username
        self.password = password

    def main(self):
        self.SkyBlue_print(
            "0、退出程序\n1、备份个人文集或精华区\n2、备份站内信\n3、备份自己的个人文集和站内信\n4、关于本程序\n")
        choose_in_main_menu = input()
        if choose_in_main_menu == '0':
            self.Green_print("未名BBS充满了你我的珍贵记忆，我们曾经在这里相遇，相知，相聚，相爱，相骂，相思……")
            self.Red_print("但愿这份备份永远只是个备份，从未真正派上用场！")
            self.SkyBlue_print("Bigscience敬上！")
            exit()
        elif choose_in_main_menu == '1':
            self.SkyBlue_print(
                "0、退出程序\n1、备份自己的个人文集\n2、备份他人的个人文集\n3、备份精华区（不推荐，因为精华区内容量过于庞大）\n4、返回首页"
            )
            choose_in_collection_menu = input()
            if choose_in_collection_menu == '0':
                self.Green_print("未名BBS充满了你我的珍贵记忆，我们曾经在这里相遇，相知，相聚，相爱，相骂，相思……")
                self.Red_print("但愿这份备份永远只是个备份，从未真正派上用场！")
                self.SkyBlue_print("Bigscience敬上！")
                exit()
            elif choose_in_collection_menu == '1':
                self.download_personal_collection()
                self.check_cookie()
                self.main()
            elif choose_in_collection_menu == '2' or choose_in_collection_menu == '3':
                path = input("\033[32m请输入要备份的个人文集/精华区的url地址：\033[0m")
                path = unquote(path)
                path = path.replace(
                    'https://bbs.pku.edu.cn/v2/collection.php?path=', '')
                new_cache_dir = re.search(r'([^/]+)$',
                                          path).group(0).replace('/', '')
                self.refresh_cache_dir(new_cache_dir)
                self.download_persional_collection_dir(path, 1)
                self.check_cookie()
                self.main()
            elif choose_in_collection_menu == '4':
                self.main()
            else:
                self.Red_print("输入错误，请重新输入！")
                self.main()
        elif choose_in_main_menu == '2':
            self.download_personal_mail()
            self.check_cookie()
            self.main()
        elif choose_in_main_menu == '3':
            self.download_personal_collection()
            self.download_personal_mail()
            self.check_cookie()
            self.main()
        elif choose_in_main_menu == '4':
            self.Red_print(
                "开发者：Bigscience\n版本：V1.0\nGithub开源地址：https://github.com/Doublefire-Chen/BBS_Personal_Backup_Tool")
            self.check_cookie()
            self.main()
        else:
            self.Red_print("输入错误，请重新输入！")
            self.main()


def main():

    Print().welcome()
    username = input("\033[1;32m请输入用户名：\033[0m")
    password = getpass.getpass("\033[1;32m请输入密码（无回显）：\033[0m")
    MyBBS = Menu(username, password)
    MyBBS.refresh_cookie()
    MyBBS.main()


if __name__ == '__main__':
    main()
