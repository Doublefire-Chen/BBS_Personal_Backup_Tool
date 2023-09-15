# -*- coding: utf-8 -*-
# @Author: Bigscience
# @email: 站内信
# @Date:   2023-09-13 15:34:05
# @Last Modified by:   Doublefire.Chen
# @Last Modified time: 2023-09-15 14:07:12

import requests
from bs4 import BeautifulSoup
import re
import hashlib
from urllib.parse import urlencode, quote, unquote, urlparse, urljoin
import os
import time
from print import Print
import json


class BBS(Print):
    """docstring for BBS"""

    def __init__(self, username, password):
        super(BBS, self).__init__()
        self.username = username
        self.password = password
        self.session = requests.session()  # 使用session发送请求
        self.replyed_url = []

    def refresh_cookie(self):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://bbs.pku.edu.cn',
            'Referer': 'https://bbs.pku.edu.cn/v2/mobile/login.php',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua':
            '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        import time
        timestamp = int(time.time())
        needhash = self.password + self.username + str(
            timestamp) + self.password
        hl = hashlib.md5()
        hl.update(needhash.encode(encoding='utf8'))
        md5 = hl.hexdigest(
        )  # MD5 hash加密处理 参考：https://blog.csdn.net/m0_49589385/article/details/118400697
        data = {
            'username': self.username,
            'password': self.password,
            'keepalive': '0',
            'time': timestamp,
            't': md5
        }  # 登陆时发送请求包的data初始赋值
        global header  # 申明全局变量
        login = self.session.post('https://bbs.pku.edu.cn/v2/ajax/login.php',
                                  data=data,
                                  headers=headers)  # 发送登陆请求
        json_data = json.loads(login.text)
        if json_data['success'] == True:  # 判断是否成功发送登录请求
            self.session.cookies.update(
                login.cookies
            )  # 更新cookie 参考：https://www.cnblogs.com/zhongyehai/p/9159641.html
            r = self.session.get(
                'https://bbs.pku.edu.cn/v2/mobile/home.php')  # 登录后回到主页
            self.session.cookies.update(r.cookies)
            homepage = BeautifulSoup(r.text, "html.parser")  # 解析
            global BBS_id  # 申明全局变量
            BBS_id = re.search(r'window.username = ".+"',
                               str(homepage)).group(0).replace(
                                   '"',
                                   '').replace('window.username = ',
                                               '')  # 正则表达式匹配得到id并删去匹配用的多余字符串
            print("\033[1;36m登录成功，欢迎用户\033[1;31m" + BBS_id +
                  "\033[1;36m使用本程序\033[0m")  # 提示性输出
            self.Green_print("请根据提示选择数字继续完成您的操作")
            global cache_dir
            cache_dir = BBS_id
        else:
            self.Red_print("账号或密码输入错误，程序终止")
            exit()

    def check_cookie(self):
        r = self.session.get(
            'https://bbs.pku.edu.cn/v2/mobile/home.php')  # 登录后回到主页
        self.session.cookies.update(r.cookies)
        homepage = BeautifulSoup(r.text, "html.parser")  # 解析
        BBS_id = re.search(r'window.username = ".+"',
                           str(homepage)).group(0).replace('"', '').replace(
                               'window.username = ',
                               '')  # 正则表达式匹配得到id并删去匹配用的多余字符串
        if BBS_id.lower() == self.username.lower():
            global cache_dir
            cache_dir = BBS_id
            self.Green_print(f"cookie有效，登录用户：{self.username}")  # 提示性输出
        else:
            self.Red_print("cookie失效，正在尝试重新获取cookie")
            self.refresh_cookie()
            self.check_cookie()

    def get_uid(self, bbsid):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://bbs.pku.edu.cn',
            'Referer': 'https://bbs.pku.edu.cn/v2/mail-new.php',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua':
            '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        data_user = {"names": '["' + bbsid + '"]'}
        mail_get_uid = self.session.post(
            'https://bbs.pku.edu.cn/v2/ajax/get_userinfo_by_names.php',
            headers=headers,
            data=data_user)
        self.session.cookies.update(mail_get_uid.cookies)
        uid = re.search(r'"id":\d+',
                        mail_get_uid.text).group(0).replace('"id":',
                                                            "")  # 获取uid
        return uid

    def get_collection_root_path(self):
        uid = self.get_uid(self.username)
        headers = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://bbs.pku.edu.cn/v2/home.php',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'sec-ch-ua':
            '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        params = {
            'uid': uid,
        }

        response = requests.get('https://bbs.pku.edu.cn/v2/user.php',
                                params=params,
                                headers=headers)
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <span> element with class="personal-collection"
        span_element = soup.find('span', class_='personal-collection')

        # Find the closest <a> element following the <span> element
        a_element = span_element.find_next_sibling('a', class_='link')

        # Get the URL from the 'href' attribute of the <a> element
        path = a_element['href'].replace('collection.php?path=', '')
        path = unquote(path, 'utf-8')
        return path

    def download_resource(self, cache_dir, url):
        base_url = urlparse(url).scheme + '://' + urlparse(url).hostname

        # 移除URL中的查询参数并进行URL解码
        clean_url = unquote(re.sub(r'\?.*', '', url))
        # 获取资源相对路径
        resource_path = os.path.relpath(clean_url, base_url)
        # 拆分路径，创建多层目录
        resource_dir = os.path.join(cache_dir, os.path.dirname(resource_path))
        os.makedirs(resource_dir, exist_ok=True)
        # 拼接本地保存路径
        local_path = os.path.join(cache_dir, resource_path)

        # 检查本地文件是否已存在
        if os.path.exists(local_path):
            # print(f'已下载的资源，不再重复下载：{url}')
            return local_path

        response = self.session.get(url)
        if response.status_code == 200:
            content = response.content
            with open(local_path, 'wb') as file:
                file.write(content)
            self.Green_print('开始下载资源：' + url)
            return local_path
        else:
            self.Red_print(f'下载失败，状态码: {response.status_code}')
            return None

    def download_persional_collection_file(self, path):
        url = 'https://bbs.pku.edu.cn/v2/collection-read.php'
        self.Green_print(f'开始下载页面：{path}')
        # 使用正则表达式匹配
        the_most_right = '/' + \
            re.search(r'/([^/]+)$', path).group(0).replace('/', '')
        local_file_name = the_most_right.replace('/', '') + '.html'
        base_url = urlparse(url).scheme + '://' + urlparse(url).hostname
        headers = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'sec-ch-ua':
            '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        params = {
            'path': path,
        }

        response = self.session.get(url=url, params=params, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            '''
            # 下载页面中的CSS和JS文件
            for link in soup.find_all(['link', 'script']):
                resource_url = urljoin(url, link.get('href') or link.get('src'))
                if resource_url.startswith(base_url):
                    filename = download_resource(resource_url)
                    if filename:
                        # 更新页面中的资源链接
                        if link.name == 'link':
                            link['href'] = os.path.relpath(filename, cache_dir)
                        elif link.name == 'script':
                            link['src'] = os.path.relpath(filename, cache_dir)
            '''
            # 只下载页面中的CSS文件，因为某些js会导致异常（一直强制refresh）
            for link in soup.find_all(['link']):
                resource_url = urljoin(url, link.get('href'))
                if resource_url.startswith(base_url):
                    filename = self.download_resource(cache_dir, resource_url)
                    if filename:
                        # 更新页面中的资源链接
                        if link.name == 'link':
                            link['href'] = os.path.relpath(filename, cache_dir)
                        elif link.name == 'script':
                            link['src'] = os.path.relpath(filename, cache_dir)
            # 下载页面中的图片等资源
            for img in soup.find_all('img'):
                img_url = urljoin(url, img.get('src'))
                if img_url.startswith(base_url):
                    filename = self.download_resource(cache_dir, img_url)
                    if filename:
                        img['src'] = os.path.relpath(filename, cache_dir)

            # 下载附件类型的资源
            for a in soup.find_all('a', {'data-no-pjax': True}):
                attachment_url = a.get('href')
                if attachment_url and attachment_url.startswith(
                        'https://bbs.pku.edu.cn/attach/'):
                    filename = self.download_resource(cache_dir,
                                                      attachment_url)
                    if filename:
                        a['href'] = os.path.relpath(filename, cache_dir)
            # 修改所有的线上资源链接为本地相对路径
            links = soup.find_all(
                'a',
                href=re.compile(
                    r'^(collection\.php\?path=|collection-read\.php\?path=)'))
            # 遍历找到的链接并替换为"local_link"
            for link in links:
                #link['href'] = 'local_link'
                need_to_replace = link['href']
                need_to_replace = unquote(need_to_replace, 'utf-8')
                the_most_right_witn_html_tag = re.search(
                    r'/([^/]+)$', need_to_replace).group(0).replace(
                        '/', '') + '.html'
                link['href'] = the_most_right_witn_html_tag
            links = soup.find_all('a',
                                  href=re.compile(r'^/v2/collection-read.php'))
            for link in links:
                need_to_replace = link['href']
                need_to_replace = unquote(need_to_replace, 'utf-8')
                the_most_right_witn_html_tag = re.search(
                    r'/([^/]+)$', need_to_replace).group(0).replace(
                        '/', '') + '.html'
                link['href'] = the_most_right_witn_html_tag
            # 修改登录状态，使其正常显示，因为没有加载js文件，所以需要手动修改，css默认是显示not-login，于是我们删除原有not-login的div块，并将have-login的div块类别修改为not-login从而使其正常显示
            not_login_divs = soup.find('div', class_='not-login')
            not_login_divs.extract()
            have_login_divs = soup.find('div', class_='have-login')
            have_login_divs['class'] = ['not-login']

            # 打通个人文集与站内信的链接
            custom_html_block = """
<span id="icon-mail">
    <a href="mail-type-1.html">
        <img src="v2/images/home/iconfont-xinjian.png">
        <span class="notice-digit" style="display: none;">0</span>
    </a>
</span>
"""
            # 找到要替换的代码块元素
            code_block = soup.find('span', id='icon-mail')

            # 创建一个新的Beautiful Soup对象来解析自定义HTML代码块
            custom_soup = BeautifulSoup(custom_html_block, 'html.parser')

            # 用自定义代码块替换原始代码块
            code_block.replace_with(custom_soup)

            # 保存更新后的HTML文件
            with open(os.path.join(cache_dir, local_file_name),
                      'w',
                      encoding='utf-8') as file:
                file.write(str(soup))
            self.Green_print(f'file_page下载完成：path={path}，休息6s后继续')
            time.sleep(6)
        else:
            self.Red_print("网络错误")
            self.Red_print(f'url:{url},path:{path}')
            self.Red_print(str(response.status_code))

    def get_dir_max_page_num(self, path):
        headers = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'sec-ch-ua':
            '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        params = {
            'path': path,
        }
        url = 'https://bbs.pku.edu.cn/v2/collection.php'
        response = self.session.get(url=url, params=params, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paging_hide_while_sorting = soup.find(
                'div', class_='paging hide-while-sorting')
            try:
                max_num = re.search(
                    r'/ \d+',
                    paging_hide_while_sorting.text).group(0).replace('/ ', '')
                return max_num
            except:
                return 1
        else:
            self.Red_print("网络错误")
            self.Red_print(f'url:{url}')
            self.Red_print(str(response.status_code))
            exit()

    def refresh_cache_dir(self, new_cache_dir):
        global cache_dir
        cache_dir = new_cache_dir

    def download_persional_collection_dir(self, path, page_num):
        page_num = int(page_num)
        url = 'https://bbs.pku.edu.cn/v2/collection.php'
        self.Green_print(f'开始下载页面：{path}')
        # 使用正则表达式匹配
        the_most_right = '/' + \
            re.search(r'/([^/]+)$', path).group(0).replace('/', '')
        base_url = urlparse(url).scheme + '://' + urlparse(url).hostname
        headers = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'sec-ch-ua':
            '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        max_num = self.get_dir_max_page_num(path)
        while page_num <= int(max_num):

            params = {
                'path': path,
                'page': str(page_num),
            }
            response = self.session.get(url=url,
                                        params=params,
                                        headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                collection_items = soup.find_all('div',
                                                 class_='collection-item')
                for item in collection_items:
                    item_url = item.find('a', class_="item-name")['href']
                    sub_path = unquote(item_url, 'utf-8')
                    if 'collection.php' in sub_path:
                        sub_path = sub_path.replace('collection.php?path=', '')
                        self.download_persional_collection_dir(sub_path, 1)
                    elif 'collection-read.php' in sub_path:
                        sub_path = sub_path.replace(
                            'collection-read.php?path=', '')
                        self.download_persional_collection_file(sub_path)
                '''
                # 下载页面中的CSS和JS文件
                for link in soup.find_all(['link', 'script']):
                    resource_url = urljoin(url, link.get('href') or link.get('src'))
                    if resource_url.startswith(base_url):
                        filename = download_resource(resource_url)
                        if filename:
                            # 更新页面中的资源链接
                            if link.name == 'link':
                                link['href'] = os.path.relpath(filename, cache_dir)
                            elif link.name == 'script':
                                link['src'] = os.path.relpath(filename, cache_dir)
                '''
                # 只下载页面中的CSS文件，因为某些js会导致异常（一直强制refresh）
                for link in soup.find_all(['link']):
                    resource_url = urljoin(url, link.get('href'))
                    if resource_url.startswith(base_url):
                        filename = self.download_resource(
                            cache_dir, resource_url)
                        if filename:
                            # 更新页面中的资源链接
                            if link.name == 'link':
                                link['href'] = os.path.relpath(
                                    filename, cache_dir)
                            elif link.name == 'script':
                                link['src'] = os.path.relpath(
                                    filename, cache_dir)
                # 下载页面中的图片等资源
                for img in soup.find_all('img'):
                    img_url = urljoin(url, img.get('src'))
                    if img_url.startswith(base_url):
                        filename = self.download_resource(cache_dir, img_url)
                        if filename:
                            img['src'] = os.path.relpath(filename, cache_dir)

                # 下载附件类型的资源
                for a in soup.find_all('a', {'data-no-pjax': True}):
                    attachment_url = a.get('href')
                    if attachment_url and attachment_url.startswith(
                            'https://bbs.pku.edu.cn/attach/'):
                        filename = self.download_resource(
                            cache_dir, attachment_url)
                        if filename:
                            a['href'] = os.path.relpath(filename, cache_dir)
                # 修改所有的线上资源链接为本地相对路径
                links = soup.find_all(
                    'a',
                    href=re.compile(
                        r'^(collection\.php\?path=|collection-read\.php\?path=)'
                    ))
                # 遍历找到的链接并替换为"local_link"
                for link in links:
                    #link['href'] = 'local_link'
                    need_to_replace = link['href']
                    need_to_replace = unquote(need_to_replace, 'utf-8')
                    the_most_right_witn_html_tag = re.search(
                        r'/([^/]+)$', need_to_replace).group(0).replace(
                            '/', '') + '.html'
                    link['href'] = the_most_right_witn_html_tag
                links = soup.find_all(
                    'a', href=re.compile(r'^/v2/collection-read.php'))
                for link in links:
                    need_to_replace = link['href']
                    need_to_replace = unquote(need_to_replace, 'utf-8')
                    the_most_right_witn_html_tag = re.search(
                        r'/([^/]+)$', need_to_replace).group(0).replace(
                            '/', '') + '.html'
                    link['href'] = the_most_right_witn_html_tag
                link_tags = soup.find_all('a',
                                          href=re.compile(r'\?path=groups'))

                # 循环遍历每个<a>标签，找到与页面相关的链接，进行本地替换
                for link_tag in link_tags:
                    # 获取原始链接
                    original_link = link_tag['href']
                    original_link = unquote(original_link, 'utf-8')
                    num = re.search(r'page=\d+', original_link)
                    # detect if the num is noneType
                    if num is None:
                        to_be_replaced = the_most_right.replace('/',
                                                                '') + '.html'
                    else:
                        num = num.group(0).replace('page=', '')
                        to_be_replaced = the_most_right.replace(
                            '/', '') + '-' + num + '.html'
                    link_tag['href'] = to_be_replaced
                    # 更新<a>标签的链接属性
                    #link_tag['href'] = modified_link
                # 修改登录状态，使其正常显示，因为没有加载js文件，所以需要手动修改，css默认是显示not-login，于是我们删除原有not-login的div块，并将have-login的div块类别修改为not-login从而使其正常显示
                not_login_divs = soup.find('div', class_='not-login')
                not_login_divs.extract()
                have_login_divs = soup.find('div', class_='have-login')
                have_login_divs['class'] = ['not-login']

                # 打通个人文集与站内信的链接
                custom_html_block = """
<span id="icon-mail">
    <a href="mail-type-1.html">
        <img src="v2/images/home/iconfont-xinjian.png">
        <span class="notice-digit" style="display: none;">0</span>
    </a>
</span>
"""
                # 找到要替换的代码块元素
                code_block = soup.find('span', id='icon-mail')

                # 创建一个新的Beautiful Soup对象来解析自定义HTML代码块
                custom_soup = BeautifulSoup(custom_html_block, 'html.parser')

                # 用自定义代码块替换原始代码块
                code_block.replace_with(custom_soup)

                # 保存更新后的HTML文件
                if page_num == 1:
                    local_file_name = the_most_right.replace('/', '') + '.html'
                else:
                    local_file_name = the_most_right.replace(
                        '/', '') + '-' + str(page_num) + '.html'
                with open(os.path.join(cache_dir, local_file_name),
                          'w',
                          encoding='utf-8') as file:
                    file.write(str(soup))
                self.Green_print(
                    f'dir_page下载完成：path={path},page_num={page_num}，休息6s后继续')
                time.sleep(6)
                page_num += 1
            else:
                self.Red_print("网络错误")
                self.Red_print(f'url:{url},path:{path},page_num:{page_num}')
                self.Red_print(str(response.status_code))

    def download_personal_collection(self):
        # 创建一个目录来保存缓存文件
        # self.check_cookie()
        os.makedirs(cache_dir, exist_ok=True)
        path = self.get_collection_root_path()
        self.download_persional_collection_dir(path, 1)
        self.Green_print("个人文集下载完成")

    def get_mail_max_page_num(self, type):
        headers = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'sec-ch-ua':
            '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        params = {
            'type': type,
            'page': '1',
        }
        response = self.session.get('https://bbs.pku.edu.cn/v2/mail.php',
                                    params=params,
                                    headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        paging = soup.find('div', class_='paging')
        max_num = re.search(r'/ \d+', paging.text).group(0).replace('/ ', '')
        return max_num

    def download_personal_mail_file(self, postid, type):
        url = 'https://bbs.pku.edu.cn/v2/mail-read.php'
        base_url = urlparse(url).scheme + '://' + urlparse(url).hostname
        headers = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'sec-ch-ua':
            '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        params = {
            'type': type,
            'postid': postid,
        }

        response = self.session.get(url=url, params=params, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 只下载页面中的CSS文件，因为某些js会导致异常（一直强制refresh）
            for link in soup.find_all(['link']):
                resource_url = urljoin(url, link.get('href'))
                if resource_url.startswith(base_url):
                    filename = self.download_resource(cache_dir, resource_url)
                    if filename:
                        # 更新页面中的资源链接
                        if link.name == 'link':
                            link['href'] = os.path.relpath(filename, cache_dir)
                        elif link.name == 'script':
                            link['src'] = os.path.relpath(filename, cache_dir)
            # 下载页面中的图片等资源
            for img in soup.find_all('img'):
                img_url = urljoin(url, img.get('src'))
                if img_url.startswith(base_url):
                    filename = self.download_resource(cache_dir, img_url)
                    if filename:
                        img['src'] = os.path.relpath(filename, cache_dir)

            # 下载附件类型的资源
            for a in soup.find_all('a', {'data-no-pjax': True}):
                attachment_url = a.get('href')
                if attachment_url and attachment_url.startswith(
                        'https://bbs.pku.edu.cn/attach/'):
                    filename = self.download_resource(cache_dir,
                                                      attachment_url)
                    if filename:
                        a['href'] = os.path.relpath(filename, cache_dir)
            # 更新<a>标签的链接属性
            #link_tag['href'] = modified_link
            # 修改登录状态，使其正常显示，因为没有加载js文件，所以需要手动修改，css默认是显示not-login，于是我们删除原有not-login的div块，并将have-login的div块类别修改为not-login从而使其正常显示
            not_login_divs = soup.find('div', class_='not-login')
            not_login_divs.extract()
            have_login_divs = soup.find('div', class_='have-login')
            have_login_divs['class'] = ['not-login']

            # 遍历，替换所有的php为html
            link_tags = soup.find_all('a', href=True)

            for link in link_tags:
                old_href = link['href']
                new_href = re.sub(r'\.php\b', '.html', old_href)
                link['href'] = new_href

            # 遍历，替换一些特殊位置的url
            link_tags = soup.find_all('a', href=True)

            for link in link_tags:
                # self.Red_print(link['href'])
                old_href = link['href']
                if old_href == 'mail.html':
                    link['href'] = 'mail-type-1.html'
                elif old_href == 'mail.html?type=4':
                    link['href'] = 'mail-type-4.html'
                elif old_href == 'mail.html?type=3':
                    link['href'] = 'mail-type-3.html'
                elif "/v2/mail-read.html?postid=" in old_href:
                    replace_postid = old_href.replace(
                        '/v2/mail-read.html?postid=', '')
                    link['href'] = replace_postid + '.html'
                elif "/v2/mail-read.html?type=4&postid=" in old_href:
                    replace_postid = old_href.replace(
                        "/v2/mail-read.html?type=4&postid=", '')
                    link['href'] = replace_postid + '.html'
                elif "/v2/mail-read.html?type=3&postid=" in old_href:
                    replace_postid = old_href.replace(
                        "/v2/mail-read.html?type=3&postid=", '')
                    link['href'] = replace_postid + '.html'
                elif '/v2/mail.html' in old_href:
                    replace_type = re.search(r'type=(\d+)',
                                             link['href']).group(0).replace(
                                                 'type=', '')
                    replace_num = re.search(r'page=(\d+)',
                                            link['href']).group(0).replace(
                                                'page=', '')
                    if replace_num == '1':
                        link['href'] = 'mail-type-' + replace_type + '.html'
                    else:
                        link['href'] = 'mail-type-' + \
                            replace_type+'-'+replace_num+'.html'
                elif '/v2/mail-read.html' in old_href:
                    replace_postid = re.search(r'postid=(\d+)',
                                               link['href']).group(0).replace(
                                                   'postid=', '')
                    link['href'] = replace_postid + '.html'
                elif old_href == '?type=4':  # 替换已发送邮箱的链接为local link
                    link['href'] = 'mail-type-4.html'
                elif old_href == '?type=1':  # 替换收件箱的链接为local link
                    link['href'] = 'mail-type-1.html'
                elif old_href == '?type=3':  # 替换星标收件箱的链接为local link
                    link['href'] = 'mail-type-3.html'
                # self.Green_print(link['href'])
            # 打通个人文集与站内信的链接
                old_a = soup.find('a', class_='sub-button')
                old_a['href'] = BBS_id + '.html'

            # 保存更新后的HTML文件
            local_file_name = postid + '.html'
            with open(os.path.join(cache_dir, local_file_name),
                      'w',
                      encoding='utf-8') as file:
                file.write(str(soup))
            self.Green_print(
                f'file_page下载完成：postid={postid},type={type}，休息6s后继续')
            time.sleep(6)
        else:
            self.Red_print("网络错误")
            self.Red_print(f'url:{url},postid:{postid}')
            self.Red_print(str(response.status_code))

    def download_star_image(self):
        self.Green_print('开始下载star图标')
        starn_url = 'https://bbs.pku.edu.cn/v2/images/global/starn.png'
        stary_url = 'https://bbs.pku.edu.cn/v2/images/global/stary.png'
        self.download_resource(cache_dir, starn_url)
        self.download_resource(cache_dir, stary_url)

    def download_personal_mail_dir(self, type):
        url = 'https://bbs.pku.edu.cn/v2/mail.php'
        headers = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'sec-ch-ua':
            '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        mail_page_max_num = self.get_mail_max_page_num(type)
        page_num = 1
        while page_num <= int(mail_page_max_num):
            params = {
                'type': type,
                'page': page_num,
            }
            if type == 1:
                self.Green_print('开始下载收件箱页面：' + str(page_num))
            elif type == 4:
                self.Green_print('开始下载发件箱页面：' + str(page_num))
            elif type == 3:
                self.Green_print('开始下载星标收件箱页面：' + str(page_num))
            base_url = urlparse(url).scheme + '://' + urlparse(url).hostname
            response = self.session.get(url=url,
                                        params=params,
                                        headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                mail_items = soup.find_all('div',
                                           class_='list-item row-wrapper')
                for item in mail_items:
                    old_url = item.find('a', class_='link')
                    item_url = unquote(old_url['href'], 'utf-8')
                    if type == 1:
                        postid = item_url.replace('mail-read.php?postid=', '')
                    elif type == 4:
                        postid = item_url.replace(
                            'mail-read.php?type=4&postid=', '')
                    elif type == 3:
                        postid = item_url.replace(
                            'mail-read.php?type=3&postid=', '')
                    old_url['href'] = postid + '.html'
                    self.download_personal_mail_file(postid, type)
                # 只下载页面中的CSS文件，因为某些js会导致异常（一直强制refresh）
                for link in soup.find_all(['link']):
                    resource_url = urljoin(url, link.get('href'))
                    if resource_url.startswith(base_url):
                        filename = self.download_resource(
                            cache_dir, resource_url)
                        if filename:
                            # 更新页面中的资源链接
                            if link.name == 'link':
                                link['href'] = os.path.relpath(
                                    filename, cache_dir)
                            elif link.name == 'script':
                                link['src'] = os.path.relpath(
                                    filename, cache_dir)
                # 下载页面中的图片等资源
                for img in soup.find_all('img'):
                    img_url = urljoin(url, img.get('src'))
                    if img_url.startswith(base_url):
                        filename = self.download_resource(cache_dir, img_url)
                        if filename:
                            img['src'] = os.path.relpath(filename, cache_dir)

                # 下载附件类型的资源
                for a in soup.find_all('a', {'data-no-pjax': True}):
                    attachment_url = a.get('href')
                    if attachment_url and attachment_url.startswith(
                            'https://bbs.pku.edu.cn/attach/'):
                        filename = self.download_resource(
                            cache_dir, attachment_url)
                        if filename:
                            a['href'] = os.path.relpath(filename, cache_dir)

                # 遍历找到页数栏的链接并替换为"local_link"
                links = soup.find('div', class_='paging').find_all('a',
                                                                   href=True)
                for link in links:
                    if type == 1:
                        if link['href'] == 'mail.php':
                            link['href'] = 'mail-type-1.html'
                        elif '?page=' in link['href']:
                            num = link['href'].replace('?page=', '')
                            link['href'] = 'mail-type-1-' + num + '.html'
                    elif type == 4:
                        if link['href'] == '?type=4':
                            link['href'] = 'mail-type-4.html'
                        elif '?type=4&page=' in link['href']:
                            replace_page_num = re.search(
                                r'page=(\d+)',
                                link['href']).group(0).replace('page=', '')
                            link['href'] = 'mail-type-4-' + \
                                replace_page_num+'.html'
                    elif type == 3:
                        if link['href'] == '?type=3':
                            link['href'] = 'mail-type-3.html'
                        elif '?type=3&page=' in link['href']:
                            replace_page_num = re.search(
                                r'page=(\d+)',
                                link['href']).group(0).replace('page=', '')
                            link['href'] = 'mail-type-3-' + \
                                replace_page_num+'.html'
                # 遍历，替换所有的php为html
                link_tags = soup.find_all('a', href=True)

                for link in link_tags:
                    old_href = link['href']
                    new_href = re.sub(r'\.php\b', '.html', old_href)
                    link['href'] = new_href

                # 遍历，替换一些特殊位置的url
                link_tags = soup.find_all('a', href=True)

                for link in link_tags:
                    # self.Red_print(link['href'])
                    old_href = link['href']
                    if old_href == 'mail.html':
                        link['href'] = 'mail-type-1.html'
                    elif old_href == 'mail.html?type=4':
                        link['href'] = 'mail-type-4.html'
                    elif old_href == "/v2/mail.html?type=4":
                        link['href'] = 'mail-type-4.html'
                    elif old_href == 'mail.html?type=3':
                        link['href'] = 'mail-type-3.html'
                    elif '/v2/mail.html' in old_href:
                        replace_type = re.search(
                            r'type=(\d+)',
                            link['href']).group(0).replace('type=', '')
                        replace_num = re.search(r'page=(\d+)',
                                                link['href']).group(0).replace(
                                                    'page=', '')
                        if replace_num == '1':
                            link[
                                'href'] = 'mail-type-' + replace_type + '.html'
                        else:
                            link['href'] = 'mail-type-' + \
                                replace_type+'-'+replace_num+'.html'
                    elif '/v2/mail-read.html?postid=' in old_href:
                        replace_postid = old_href.replace(
                            '/v2/mail-read.html?postid=', '')
                        link['href'] = replace_postid + '.html'
                    elif old_href == '?type=4':  # 替换已发送邮箱的链接为local link
                        link['href'] = 'mail-type-4.html'
                    elif old_href == '?type=1':  # 替换收件箱的链接为local link
                        link['href'] = 'mail-type-1.html'
                    elif old_href == '?type=3':  # 替换星标收件箱的链接为local link
                        link['href'] = 'mail-type-3.html'
                    # self.Green_print(link['href'])
                # 更新<a>标签的链接属性
                #link_tag['href'] = modified_link
                # 修改登录状态，使其正常显示，因为没有加载js文件，所以需要手动修改，css默认是显示not-login，于是我们删除原有not-login的div块，并将have-login的div块类别修改为not-login从而使其正常显示
                not_login_divs = soup.find('div', class_='not-login')
                not_login_divs.extract()
                have_login_divs = soup.find('div', class_='have-login')
                have_login_divs['class'] = ['not-login']

                # 打通个人文集与站内信的链接
                old_a = soup.find('a', class_='sub-button')
                old_a['href'] = BBS_id + '.html'

                # 保存更新后的HTML文件
                if page_num == 1:
                    local_file_name = 'mail-' + 'type-' + str(type) + '.html'
                else:
                    local_file_name = 'mail-'+'type-' + \
                        str(type)+'-'+str(page_num)+'.html'
                with open(os.path.join(cache_dir, local_file_name),
                          'w',
                          encoding='utf-8') as file:
                    file.write(str(soup))
                self.Green_print(
                    f'dir_page下载完成：url:{url},type:{type},page_num:{page_num}，休息6s后继续'
                )
                time.sleep(6)
                page_num += 1
            else:
                self.Red_print("网络错误")
                self.Red_print(f'url:{url},type:{type},page_num:{page_num}')
                self.Red_print(str(response.status_code))

    def download_personal_mail(self):
        # self.check_cookie()
        # 创建一个目录来保存缓存文件
        os.makedirs(cache_dir, exist_ok=True)
        self.download_star_image()
        self.download_personal_mail_dir(1)
        self.download_personal_mail_dir(4)
        self.download_personal_mail_dir(3)
        self.Green_print('个人站内信下载完成')
