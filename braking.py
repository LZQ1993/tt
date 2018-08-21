import requests
import json
import mysqlDaob
import time
import random
class Braking(object):

    # 初始化函数
    # 初始化函数
    def __init__(self):
        # 加载数据库
        self.ms = mysqlDaob.MysqlDao()
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
        co1 = "WEE_SID=P7JeoY8HhwwVoV2bS3yXyp3TCnFvfYGieknpnpgX-JL7AZZ59S3e!405055628!472174867!1534890970887;"
        co2 = "IS_LOGIN=true; wee_username=ZnRmdDEwMA==; wee_password=MTIzNDU2Nzg5YWE=;"
        co3 = "JSESSIONID=P7JeoY8HhwwVoV2bS3yXyp3TCnFvfYGieknpnpgX-JL7AZZ59S3e!405055628!472174867;"
        co4 = "hibext_instdsigdipv2=1; _ga=GA1.3.1678005571.1530947667; _gid=GA1.3.748374959.1530947667"
        cookie = co1 + co2 + co3 + co4
        self.headers['Cookie'] = cookie

    # 爬取数据入口函数
    def patent(self):
        IPC_Index, executableSearchExp, literatureSF_and_searchExp, resultMode, searchKeywords, total = self.loadData();
        proxie_list, user_agents = self.loadproxy()
        print("爬取数据中...")
        for i in range(0, len(IPC_Index)):
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
            for j in range(0, it_num):
                self.resquest_iteration = 0
                self.data['resultPagination.start'] = str(j * 12)
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
            print(i)
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
            time.sleep(random.randint(10, 60))
            # 随机选择一个代理
            proxies = random.choice(proxie_list)
            us = random.choice(user_agents)
            self.headers['User-Agent'] = us
            try:
                response = self.session.post(url=self.url, data=self.data, headers=self.headers,
                                             proxies=proxies).content
            except:
                response = self.network(proxie_list, user_agents)
            return response
        else:
            return ""

    # 加载爬取数据条件数据信息
    def loadData(self):
        print("正在加载数据...")
        IPC_Index = [
            "B60W30",
            "B60W20",
            "B60W10",
            "B60K6/20",
            "B60L7/1+",
            "B60L7/2+",
        ]

        total = [20,25,24,5,16772,11578]

        executableSearchExp = [
            "VDB:((ICST='B60W30' AND (KW_CPP='新能源汽车' OR KW_CPP='电制动能量回收')))",
            "VDB:((ICST='B60W20' AND (KW_CPP='新能源汽车' OR KW_CPP='电制动能量回收')))",
            "VDB:((ICST='B60W10' AND (KW_CPP='新能源汽车' OR KW_CPP='电制动能量回收')))",
            "VDB:((ICST='B60K6/20' AND (KW_CPP='新能源汽车' OR KW_CPP='电制动能量回收')))",
            "VDB:(((ICST='b60l7/1%' NOT ICST='b60l7/28') NOT (KW_CPP='新能源汽车' OR KW_CPP='电制动能量回收')))",
            "VDB:(((ICST='b60l7/2%' NOT ICST='b60l7/28') NOT (KW_CPP='新能源汽车' OR KW_CPP='电制动能量回收')))"
        ]
        literatureSF_and_searchExp= [
            "((IPC分类号=(B60W30) AND 关键词=(新能源汽车 OR 电制动能量回收)))",
            "((IPC分类号=(B60W20) AND 关键词=(新能源汽车 OR 电制动能量回收)))",
            "((IPC分类号=(B60W10) AND 关键词=(新能源汽车 OR 电制动能量回收)))",
            "((IPC分类号=(B60K6/20) AND 关键词=(新能源汽车 OR 电制动能量回收)))",
            "((IPC分类号=(b60l7/1+ NOT b60l7/28)  NOT 关键词=(新能源汽车  OR  电制动能量回收)))",
            "((IPC分类号=(b60l7/2+ NOT b60l7/28)  NOT 关键词=(新能源汽车  OR  电制动能量回收)))"

        ]
        resultMode = [
            "undefined",
            "undefined",
            "undefined",
            "undefined",
            "SEARCH_MODE",
            "SEARCH_MODE",
        ]
        searchKeywords = [
            "[电][ ]{0,}[制][ ]{0,}[动][ ]{0,}[能][ ]{0,}[量][ ]{0,}[回][ ]{0,}[收][ ]{0,},[新][ ]{0,}[能][ ]{0,}[源][ ]{0,}[汽][ ]{0,}[车][ ]{0,},[B][ ]{0,}[6][ ]{0,}[0][ ]{0,}[W][ ]{0,}[3][ ]{0,}[0][ ]{0,}",
            "[电][ ]{0,}[制][ ]{0,}[动][ ]{0,}[能][ ]{0,}[量][ ]{0,}[回][ ]{0,}[收][ ]{0,},[新][ ]{0,}[能][ ]{0,}[源][ ]{0,}[汽][ ]{0,}[车][ ]{0,},[B][ ]{0,}[6][ ]{0,}[0][ ]{0,}[W][ ]{0,}[2][ ]{0,}[0][ ]{0,}",
            "[电][ ]{0,}[制][ ]{0,}[动][ ]{0,}[能][ ]{0,}[量][ ]{0,}[回][ ]{0,}[收][ ]{0,},[新][ ]{0,}[能][ ]{0,}[源][ ]{0,}[汽][ ]{0,}[车][ ]{0,},[B][ ]{0,}[6][ ]{0,}[0][ ]{0,}[W][ ]{0,}[1][ ]{0,}[0][ ]{0,}",
            "[电][ ]{0,}[制][ ]{0,}[动][ ]{0,}[能][ ]{0,}[量][ ]{0,}[回][ ]{0,}[收][ ]{0,},[新][ ]{0,}[能][ ]{0,}[源][ ]{0,}[汽][ ]{0,}[车][ ]{0,},[B][ ]{0,}[6][ ]{0,}[0][ ]{0,}[K][ ]{0,}[6][ ]{0,}[/][ ]{0,}[2][ ]{0,}[0][ ]{0,}",
            "[电][ ]{0,}[制][ ]{0,}[动][ ]{0,}[能][ ]{0,}[量][ ]{0,}[回][ ]{0,}[收][ ]{0,},[新][ ]{0,}[能][ ]{0,}[源][ ]{0,}[汽][ ]{0,}[车][ ]{0,},[B][ ]{0,}[6][ ]{0,}[0][ ]{0,}[l][ ]{0,}[7][ ]{0,}[/][ ]{0,}[2][ ]{0,}[8][ ]{0,},[B][ ]{0,}[6][ ]{0,}[0][ ]{0,}[l][ ]{0,}[7][ ]{0,}[/][ ]{0,}[1][ ]{0,}[ ]{0,}",
            "[电][ ]{0,}[制][ ]{0,}[动][ ]{0,}[能][ ]{0,}[量][ ]{0,}[回][ ]{0,}[收][ ]{0,},[新][ ]{0,}[能][ ]{0,}[源][ ]{0,}[汽][ ]{0,}[车][ ]{0,},[b][ ]{0,}[6][ ]{0,}[0][ ]{0,}[l][ ]{0,}[7][ ]{0,}[/][ ]{0,}[2][ ]{0,}[8][ ]{0,},[b][ ]{0,}[6][ ]{0,}[0][ ]{0,}[l][ ]{0,}[7][ ]{0,}[/][ ]{0,}[2][ ]{0,}[ ]{0,}"
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
    braking = Braking()
    braking.patent()