import requests
import json
import mysqlDaoe
import time
import random

class EleCap(object):

    # 初始化函数
    def __init__(self):
        # 加载数据库
        self.ms = mysqlDaoe.MysqlDao()
        # 创建session会话
        self.session = requests.session()
        # 请求地址
        self.url = "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml"
        # 构建请求form数据
        # 可通过data2post['resultPagination.start']=60(或其他条件)来改变返回数据内容, 增加12来抓后面的12条数据
        self.resquest_iteration = 0
        self.data = {
            "resultPagination.limit": "12",
            "resultPagination.sumLimit": "10",
            "resultPagination.start": "0",
            "resultPagination.totalCount": "",
            "searchCondition.sortFields": "-APD,+PD",
            "searchCondition.searchType": "Sino_foreign",
            "searchCondition.originalLanguage": "",
            "searchCondition.extendInfo['MODE']": "MODE_TABLE",
            "searchCondition.extendInfo['STRATEGY']": "STRATEGY_CALCULATE",
            "searchCondition.searchExp": "",
            "searchCondition.executableSearchExp": "",
            "searchCondition.dbId": "",
            "searchCondition.literatureSF": "",
            "searchCondition.targetLanguage": "",
            "searchCondition.resultMode": "",
            "searchCondition.strategy": "",
            "searchCondition.searchKeywords": ""
        }
        # 构建请求头
        self.headers = {
            'Accept': 'application/json, text/javascript,*/*;q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh,zh-CN;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '1432',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.pss-system.gov.cn',
            'Origin': 'http://www.pss-system.gov.cn',
            'Referer': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        # 构建cookie，并填入header
        co1 = "WEE_SID=_-NZyYhZJIO0dF6LT8ESni8cbaAXC24C5dE9OY_mxNwQwaeILXaz!218255454!-601920043!1534809704537;"
        co2 = "IS_LOGIN=true; wee_username=QWVyaWMwMDc%3D; wee_password=TFpRMTM1OTE5OTAyMjFMWg%3D%3D;"
        co3 = "JSESSIONID=_-NZyYhZJIO0dF6LT8ESni8cbaAXC24C5dE9OY_mxNwQwaeILXaz!218255454!-601920043;"
        co4 = "hibext_instdsigdipv2=1; _ga=GA1.3.1678005571.1530947667; _gid=GA1.3.748374959.1530947667"
        cookie = co1 + co2 + co3 + co4
        self.headers['Cookie'] = cookie

    # 爬取数据入口函数
    def patent(self):
        IPC_Index, executableSearchExp, literatureSF_and_searchExp, resultMode, searchKeywords, total = self.loadData();
        proxie_list, user_agents = self.loadproxy()
        print("爬取数据中...")
        # for i in range(0,len(IPC_Index)):
        for i in range(0, 1):
            self.data["searchCondition.executableSearchExp"] = executableSearchExp[i]
            self.data["searchCondition.searchType"] = literatureSF_and_searchExp[i]
            self.data["searchCondition.literatureS"] = literatureSF_and_searchExp[i]
            self.data["searchCondition.resultMode"] = resultMode[i]
            self.data["searchCondition.searchKeywords"] = searchKeywords[i]
            self.data["resultPagination.totalCount"] = str(total[i])
            if total[i] % 12 == 0:
                it_num = int(total[i] / 12)
            else:
                it_num = int(total[i] / 12) + 1
            for i in range(0, it_num):
                self.resquest_iteration = 0
                self.data['resultPagination.start'] = str(i * 12)
                response = self.network(proxie_list, user_agents)
                if response != "":
                    response = response.decode('utf-8')
                    jsonstr2dict = self.dealdata(response, proxie_list, user_agents)
                    if jsonstr2dict != "":
                        self.addData(jsonstr2dict)
                    else:
                        continue
                else:
                    continue
        self.ms.close()
        print("爬取完毕")

    def dealdata(self, response, proxie_list, user_agents):
        try:
            jsonstr2dict = json.loads(response)
            return jsonstr2dict
        except:
            return ""

    def network(self, proxie_list, user_agents):
        if self.resquest_iteration < 10:
            self.resquest_iteration = self.resquest_iteration + 1
            time.sleep(random.randint(4, 8))
            # 随机选择一个代理
            proxies = random.choice(proxie_list)
            us = random.choice(user_agents)
            self.headers['User-Agent'] = us
            try:
                response = self.session.post(url=self.url, data=self.data, headers=self.headers,
                                             proxies=proxies).content
                print(response)
            except:
                response = self.network(proxie_list, user_agents)
            return response
        else:
            return ""

    # 加载爬取数据条件数据信息
    def loadData(self):
        print("正在加载数据...")
        IPC_Index = [
            "H01G11/50",
            "H01G11/06",
        ]

        total = [323,362]

        executableSearchExp = [
            "VDB:((ICST='H01G11/50' AND (KW_CPP='电池电容' OR KW_CPP='电容电池' OR KW_CPP='电容型电容' OR KW_CPP='不对称超电容' "
            "OR KW_CPP='不对称超级电容' OR KW_CPP='非对称超级电容' OR KW_CPP='不对称的超级电容' OR KW_CPP='非对称超电容' "
            "OR KW_CPP='非对称超级电容' OR KW_CPP='非对称的超电容' OR KW_CPP='非对称的超级电容' OR KW_CPP='混合超级电容' "
            "OR KW_CPP='混合超电容' OR KW_CPP='混合型超级电容' OR KW_CPP='混合型超电容' OR KW_CPP='超级混合电容' "
            "OR KW_CPP='锂' OR KW_CPP='锂电容' OR KW_CPP='锂离子电容' OR KW_CPP='电容型锂离子电池' OR KW_CPP='电容型锂电池' "
            "OR KW_CPP='LIC' OR KW_CPP='LICs' OR KW_CPP='LHC' OR KW_CPP='LHCs')))",
            "VDB:((ICST='H01G11/06' AND (KW_CPP='电池电容' OR KW_CPP='电容电池' OR KW_CPP='电容型电容' OR KW_CPP='不对称超电容' "
            "OR KW_CPP='不对称超级电容' OR KW_CPP='非对称超级电容' OR KW_CPP='不对称的超级电容' OR KW_CPP='非对称超电容' "
            "OR KW_CPP='非对称超级电容' OR KW_CPP='非对称的超电容' OR KW_CPP='非对称的超级电容' OR KW_CPP='混合超级电容' "
            "OR KW_CPP='混合超电容' OR KW_CPP='混合型超级电容' OR KW_CPP='混合型超电容' OR KW_CPP='超级混合电容' "
            "OR KW_CPP='锂' OR KW_CPP='锂电容' OR KW_CPP='锂离子电容' OR KW_CPP='电容型锂离子电池' OR KW_CPP='电容型锂电池' "
            "OR KW_CPP='LIC' OR KW_CPP='LICs' OR KW_CPP='LHC' OR KW_CPP='LHCs')))",
        ]
        literatureSF_and_searchExp= [
            "((IPC分类号=(H01G11/50) AND 关键词=(电池电容  OR  电容电池  OR  电容型电容 OR 不对称超电容  "
            "OR 不对称超级电容 OR  非对称超级电容 OR  不对称的超级电容 OR  非对称超电容  OR 非对称超级电容  "
            "OR 非对称的超电容  OR 非对称的超级电容 OR  混合超级电容 OR  混合超电容  OR 混合型超级电容 "
            "OR  混合型超电容 OR  超级混合电容 OR  锂 OR  锂电容  OR 锂离子电容  OR 电容型锂离子电池 "
            "OR  电容型锂电池 OR  LIC  OR LICs  OR LHC  OR LHCs)))",
            "((IPC分类号=(H01G11/06) AND 关键词=(电池电容  OR  电容电池  OR  电容型电容 OR 不对称超电容  "
            "OR 不对称超级电容 OR  非对称超级电容 OR  不对称的超级电容 OR  非对称超电容  OR 非对称超级电容  "
            "OR 非对称的超电容  OR 非对称的超级电容 OR  混合超级电容 OR  混合超电容  OR 混合型超级电容 "
            "OR  混合型超电容 OR  超级混合电容 OR  锂 OR  锂电容  OR 锂离子电容  OR 电容型锂离子电池 "
            "OR  电容型锂电池 OR  LIC  OR LICs  OR LHC  OR LHCs)))",
        ]
        resultMode = [
            "undefined",
            "undefined",
        ]
        searchKeywords = [
            "[非][ ]{0,}[对][ ]{0,}[称][ ]{0,}[超][ ]{0,}[级][ ]{0,}[电][ ]{0,}[容][ ]{0,},[非][ ]{0,}[对][ ]{0,}[称][ ]{0,}[超][ ]{0,}[电][ ]{0,}[容][ ]{0,},"
            "[非][ ]{0,}[对][ ]{0,}[称][ ]{0,}[的][ ]{0,}[超][ ]{0,}[级][ ]{0,}[电][ ]{0,}[容][ ]{0,},[非][ ]{0,}[对][ ]{0,}[称][ ]{0,}[的][ ]{0,}[超][ ]{0,}[电][ ]{0,}[容][ ]{0,},"
            "[锂][ ]{0,}[离][ ]{0,}[子][ ]{0,}[电][ ]{0,}[容][ ]{0,},[锂][ ]{0,}[电][ ]{0,}[容][ ]{0,},[锂][ ]{0,},[超][ ]{0,}[级][ ]{0,}[混][ ]{0,}[合][ ]{0,}[电][ ]{0,}[容][ ]{0,},"
            "[电][ ]{0,}[池][ ]{0,}[电][ ]{0,}[容][ ]{0,},[电][ ]{0,}[容][ ]{0,}[电][ ]{0,}[池][ ]{0,},[电][ ]{0,}[容][ ]{0,}[型][ ]{0,}[锂][ ]{0,}[离][ ]{0,}[子][ ]{0,}[电][ ]{0,}[池][ ]{0,},"
            "[电][ ]{0,}[容][ ]{0,}[型][ ]{0,}[锂][ ]{0,}[电][ ]{0,}[池][ ]{0,},[电][ ]{0,}[容][ ]{0,}[型][ ]{0,}[电][ ]{0,}[容][ ]{0,},[混][ ]{0,}[合][ ]{0,}[超][ ]{0,}[级][ ]{0,}[电][ ]{0,}[容][ ]{0,},"
            "[混][ ]{0,}[合][ ]{0,}[超][ ]{0,}[电][ ]{0,}[容][ ]{0,},[混][ ]{0,}[合][ ]{0,}[型][ ]{0,}[超][ ]{0,}[级][ ]{0,}[电][ ]{0,}[容][ ]{0,},[混][ ]{0,}[合][ ]{0,}[型][ ]{0,}[超][ ]{0,}[电][ ]{0,}[容][ ]{0,},"
            "[不][ ]{0,}[对][ ]{0,}[称][ ]{0,}[超][ ]{0,}[级][ ]{0,}[电][ ]{0,}[容][ ]{0,},[不][ ]{0,}[对][ ]{0,}[称][ ]{0,}[超][ ]{0,}[电][ ]{0,}[容][ ]{0,},[不][ ]{0,}[对][ ]{0,}[称][ ]{0,}[的][ ]{0,}[超][ ]{0,}[级][ ]{0,}[电][ ]{0,}[容][ ]{0,},"
            "[L][ ]{0,}[I][ ]{0,}[C][ ]{0,}[s][ ]{0,},[L][ ]{0,}[I][ ]{0,}[C][ ]{0,},[L][ ]{0,}[H][ ]{0,}[C][ ]{0,}[s][ ]{0,},[L][ ]{0,}[H][ ]{0,}[C][ ]{0,},[H][ ]{0,}[0][ ]{0,}[1][ ]{0,}[G][ ]{0,}[1][ ]{0,}[1][ ]{0,}[/][ ]{0,}[5][ ]{0,}[0][ ]{0,}",

            "[非][ ]{0,}[对][ ]{0,}[称][ ]{0,}[超][ ]{0,}[级][ ]{0,}[电][ ]{0,}[容][ ]{0,},[非][ ]{0,}[对][ ]{0,}[称][ ]{0,}[超][ ]{0,}[电][ ]{0,}[容][ ]{0,},"
            "[非][ ]{0,}[对][ ]{0,}[称][ ]{0,}[的][ ]{0,}[超][ ]{0,}[级][ ]{0,}[电][ ]{0,}[容][ ]{0,},[非][ ]{0,}[对][ ]{0,}[称][ ]{0,}[的][ ]{0,}[超][ ]{0,}[电][ ]{0,}[容][ ]{0,},"
            "[锂][ ]{0,}[离][ ]{0,}[子][ ]{0,}[电][ ]{0,}[容][ ]{0,},[锂][ ]{0,}[电][ ]{0,}[容][ ]{0,},[锂][ ]{0,},[超][ ]{0,}[级][ ]{0,}[混][ ]{0,}[合][ ]{0,}[电][ ]{0,}[容][ ]{0,},"
            "[电][ ]{0,}[池][ ]{0,}[电][ ]{0,}[容][ ]{0,},[电][ ]{0,}[容][ ]{0,}[电][ ]{0,}[池][ ]{0,},[电][ ]{0,}[容][ ]{0,}[型][ ]{0,}[锂][ ]{0,}[离][ ]{0,}[子][ ]{0,}[电][ ]{0,}[池][ ]{0,},"
            "[电][ ]{0,}[容][ ]{0,}[型][ ]{0,}[锂][ ]{0,}[电][ ]{0,}[池][ ]{0,},[电][ ]{0,}[容][ ]{0,}[型][ ]{0,}[电][ ]{0,}[容][ ]{0,},[混][ ]{0,}[合][ ]{0,}[超][ ]{0,}[级][ ]{0,}[电][ ]{0,}[容][ ]{0,},"
            "[混][ ]{0,}[合][ ]{0,}[超][ ]{0,}[电][ ]{0,}[容][ ]{0,},[混][ ]{0,}[合][ ]{0,}[型][ ]{0,}[超][ ]{0,}[级][ ]{0,}[电][ ]{0,}[容][ ]{0,},[混][ ]{0,}[合][ ]{0,}[型][ ]{0,}[超][ ]{0,}[电][ ]{0,}[容][ ]{0,},"
            "[不][ ]{0,}[对][ ]{0,}[称][ ]{0,}[超][ ]{0,}[级][ ]{0,}[电][ ]{0,}[容][ ]{0,},[不][ ]{0,}[对][ ]{0,}[称][ ]{0,}[超][ ]{0,}[电][ ]{0,}[容][ ]{0,},[不][ ]{0,}[对][ ]{0,}[称][ ]{0,}[的][ ]{0,}[超][ ]{0,}[级][ ]{0,}[电][ ]{0,}[容][ ]{0,},"
            "[L][ ]{0,}[I][ ]{0,}[C][ ]{0,}[s][ ]{0,},[L][ ]{0,}[I][ ]{0,}[C][ ]{0,},[L][ ]{0,}[H][ ]{0,}[C][ ]{0,}[s][ ]{0,},[L][ ]{0,}[H][ ]{0,}[C][ ]{0,},[H][ ]{0,}[0][ ]{0,}[1][ ]{0,}[G][ ]{0,}[1][ ]{0,}[1][ ]{0,}[/][ ]{0,}[5][ ]{0,}[0][ ]{0,}",
        ]
        print("加载完毕")
        return IPC_Index,executableSearchExp,literatureSF_and_searchExp,resultMode,searchKeywords,total

    def loadproxy(self):
        file = r'F:\lizhiqPro\carpatent\proxies.txt'
        proxy_list = []
        dict = {}
        with open(file, "r") as f:
            line = f.readline()
            while line:
                dict.clear()
                line = f.readline().strip("\n")
                p = line.split("://")[0]
                dict[p] = line
                proxy_list.append(dict.copy())

            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
                "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
                "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
                "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
            ]
        return proxy_list, user_agents

    # 爬取数据的解析及插入数据库
    def addData(self, dict):
        if dict['searchResultDTO'] != None:
            data = dict['searchResultDTO']['searchResultRecord']
            for i in range(0, len(data)):
                inventName, applyNum, applyDate, publicNum, publicDate, IPCnum, applyPeople, inventPeople = "", "", "", "", "", "", "", ""
                inventInfo = data[i]['fieldMap']
                inventName = str(inventInfo['TIVIEW'])
                applyNum = str(inventInfo['APO'])
                applyDate = str(inventInfo['APD_VALUE'])
                publicNum = str(inventInfo['PN'])
                publicDate = str(inventInfo['PD'])
                IPCnum = str(inventInfo['IC'])
                applyPeople = str(inventInfo['PAVIEW'])
                inventPeople = str(inventInfo['INVIEW'])
                # 数据插入
                self.ms.add(inventName, applyNum, applyDate, publicNum, publicDate, IPCnum, applyPeople, inventPeople)


#################  主函数  ######################
if __name__ == "__main__":
    eleCap = EleCap()
    eleCap.patent()