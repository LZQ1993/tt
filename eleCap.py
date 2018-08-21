import requests
import json
import mysqlDaoe
import time

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
        co1 = "WEE_SID=Mz1VXwjGcRt-LjSIDtEGV1tKV3yLCNjqE75P0IMkh2FyxgufFdUW!-694876610!-555599661!1534735616198;"
        co2 = "IS_LOGIN=true; wee_username=QWVyaWMwMDc%3D; wee_password=TFpRMTM1OTE5OTAyMjFMWg%3D%3D;"
        co3 = "JSESSIONID=Mz1VXwjGcRt-LjSIDtEGV1tKV3yLCNjqE75P0IMkh2FyxgufFdUW!-694876610!-555599661;"
        co4 = "hibext_instdsigdipv2=1; _ga=GA1.3.1678005571.1530947667; _gid=GA1.3.748374959.1530947667"
        cookie = co1 + co2 + co3 + co4
        self.headers['Cookie'] = cookie

    # 爬取数据入口函数
    def patent(self):
        IPC_Index, executableSearchExp, literatureSF_and_searchExp, resultMode, searchKeywords, total = self.loadData();
        print("爬取数据中...")
        for i in range(0,len(IPC_Index)):
            self.data["searchCondition.executableSearchExp"] = executableSearchExp[i]
            self.data["searchCondition.searchType"] =  literatureSF_and_searchExp[i]
            self.data["searchCondition.literatureS"] = literatureSF_and_searchExp[i]
            self.data["searchCondition.resultMode"] = resultMode[i]
            self.data["searchCondition.searchKeywords"] = searchKeywords[i]
            self.data["resultPagination.totalCount"] = str(total[i])
            if total[i]%12 == 0:
                it_num = int(total[i]/12)
            else:
                it_num = int(total[i] / 12) +1
            for i in range(0,it_num):
                self.data['resultPagination.start'] = str(i*12)
                time.sleep(2)
                response = self.session.post(url=self.url, data=self.data, headers=self.headers).content
                response = response.decode('utf-8')
                jsonstr2dict = json.loads(response)
                # try:
                #     jsonstr2dict = json.loads(response)
                # except:

                self.addData(jsonstr2dict)
        self.ms.close()
        print("爬取完毕")

    # 加载爬取数据条件数据信息
    def loadData(self):
        print("正在加载数据...")
        IPC_Index = [
            "H01G",
        ]

        total = [20,25,24,5,16735,11570]

        executableSearchExp = [
            "VDB:((ICST='B60W30' AND (KW_CPP='新能源汽车' OR KW_CPP='电制动能量回收')))",

        ]
        literatureSF_and_searchExp= [
            "((IPC分类号=(B60W30) AND 关键词=(新能源汽车 OR 电制动能量回收)))",

        ]
        resultMode = [
            "SEARCH_MODE",
        ]
        searchKeywords = [
            "[电][ ]{0,}[制][ ]{0,}[动][ ]{0,}[能][ ]{0,}[量][ ]{0,}[回][ ]{0,}[收][ ]{0,},[新][ ]{0,}[能][ ]{0,}[源][ ]{0,}[汽][ ]{0,}[车][ ]{0,},[B][ ]{0,}[6][ ]{0,}[0][ ]{0,}[W][ ]{0,}[3][ ]{0,}[0][ ]{0,}",
           ]
        print("加载完毕")
        return IPC_Index,executableSearchExp,literatureSF_and_searchExp,resultMode,searchKeywords,total

    # 爬取数据的解析及插入数据库
    def addData(self,dict):
        data = dict['searchResultDTO']['searchResultRecord']
        for i in range(0,len(data)):
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
            self.ms.add(inventName,applyNum,applyDate,publicNum,publicDate,IPCnum,applyPeople,inventPeople)

#################  主函数  ######################
if __name__ == "__main__":
    eleCap = EleCap()
    eleCap.patent()