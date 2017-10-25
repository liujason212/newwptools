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
            final_result=result['response']
            del final_result['uri']
            return final_result
            print(final_result)
        else:
        #整理json数据
            result=result['response']['result']['Accounts']['row']['FL']
            final_result={}

            for x in result:
                print(x)
                print(x['val'])

                final_result[x['val']]=x['content']
            print(final_result)
        del final_result['ACCOUNTID']
        del final_result['SMOWNERID']
        return final_result
    else:
        final_result={'密码错误':'请确认后重新输入'}
        return final_result





'''  # 存储在str中
        xml_str = response.read()
        xml_str = xml_str.decode('utf-8')
        # print (xml_str)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(xml_str, 'xml')
        text = soup.get_text(",")
        print('the feedback message is ' + text)
        if text == '4422,There is no data to show':
            print('There is no data to show')
            #nonlocal error_message
            error_message = text
        else:
            # 分割成列表
            import re
            output = re.split(r',', text)
            output = re.split(r',', text)
            # 使用nonlocal 将变量定义为非全局变量
            #nonlocal client_owner, client_name, wp_client_number
            client_owner = output[2]
            client_name = output[3]
            wp_client_number = output[4]
            print('归属小组是%s\n客户名称是%s\nWP client number是 %s' % (client_owner, client_name, wp_client_number))
    else:
        error_message = 'wrong password'
    
    '''