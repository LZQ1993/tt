# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as pq


class GetProxy(object):
    def __init__(self):
        # 代理ip网站
        self.url = 'http://www.xicidaili.com/nn/'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        self.file = r'F:\lizhiqPro\carpatent\proxies.txt'
        # 用于检查代理ip是否可用
        self.check_url = 'https://www.python.org/'
        self.title = 'Welcome to Python.org'

    def get_page(self):
        response = requests.get(self.url, headers=self.header)
        return response.text

    def page_parse(self, response):
        stores = []
        result = pq(response)('#ip_list')
        for p in result('tr').items():
            if p('tr > td').attr('class') == 'country':
                ip = p('td:eq(1)').text()
                port = p('td:eq(2)').text()
                protocol = p('td:eq(5)').text().lower()
                # if protocol == 'socks4/5':
                #     protocol = 'socks5'
                proxy = '{}://{}:{}'.format(protocol, ip, port)
                stores.append(proxy)
        return stores

    def start(self):
        response = self.get_page()
        proxies = self.page_parse(response)
        print(len(proxies))
        file = open(self.file, 'w')
        i = 0
        for proxy in proxies:
            try:
                check = requests.get(self.check_url, headers=self.header, proxies={'http': proxy}, timeout=1)
                check_char = pq(check.text)('head > title').text()
                if check_char == self.title:
                    print('%s is useful' % proxy)
                    file.write(proxy + '\n')
                    i += 1
            except Exception as e:
                continue
        file.close()
        print('Get %s proxies' % i)

if __name__ == "__main__":
    get = GetProxy()
    get.start()