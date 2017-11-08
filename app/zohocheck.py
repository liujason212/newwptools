import requests
import os, sys
from app import sqlite_db
mypath = os.getcwd()

def zoho_check(keyword,password,type):
    SEARCH_CLIENTNAME = '(Account Name|contains|*%s*)' % (keyword)
    SEARCH_DMD='(dmd平台地址|contains|*%s*)' % (keyword)

    # zoho模块名称，这里是查询clients
    module_name = 'Accounts'
    real_password =sqlite_db.get_db_password()
    print('zhaobug')
    print(real_password)
    print(mypath)
    if password == real_password:
        authtoken =sqlite_db.get_db_token()
        # 显示哪些列
        selectColumns = 'Account Owner,WP Client Number,Account Name,Client level,dmd平台地址,'
        # 根据选择判断搜索什么
        if type=='CLIENT':
            searchCondition=SEARCH_CLIENTNAME
        else:
            searchCondition =SEARCH_DMD
        # 写入链接的参数
        params = {'authtoken': authtoken, 'scope': 'crmapi', 'selectColumns': selectColumns,
                  'searchCondition': searchCondition}
        #final_URL = "https://crm.zoho.com.cn/crm/private/json/" + module_name + "/getSearchRecords"
        final_URL = "https://crm.zoho.com.cn/crm/private/json/Accounts/getSearchRecords"
        #data = urllib.parse.urlencode(params).encode("utf-8")
        #request = urllib.request.Request(final_URL, data)
        #response = urllib.request.urlopen(request)
        #我用requests来写一下
        r=requests.get(final_URL,params=params)
        print(r.url)
        result=r.json()
        #先判断下
        if 'result' not in str(result):
            final_result = result['response']
            del final_result['uri']
            return final_result
            print(final_result)
        else:
            # 整理json数据
            print('原始查询结果')
            print(result)
            try:
                result = result['response']['result']['Accounts']['row']['FL']
                final_result = {}

                for x in result:
                    print(x)
                    print(x['val'])

                    final_result[x['val']] = x['content']
                print(final_result)
                del final_result['ACCOUNTID']
                del final_result['SMOWNERID']
                return final_result
            # 当获取到多条记录后，反馈如下信息
            except TypeError:
                final_result = {'有多条查询结果': '请输入更多关键字进行查询'}
                print(final_result)
                return final_result
            #访问出错进行提示
            except requests.RequestException:
                final_result = {'有错误': '请重试'}
                print(final_result)
                return final_result
    else:
        final_result={'密码错误':'请确认后重新输入'}
        return final_result




