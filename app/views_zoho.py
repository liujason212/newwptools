from app import app
from flask import render_template, flash, redirect
from .forms import ZohoCheck
import os, sys,time
from app import zohocheck
mypath = os.getcwd()
print(mypath)

@app.route('/zohocheck.html', methods = ['GET', 'POST'])
#@app.route('/index')

def check():
    result={}
    form = ZohoCheck()
    if form.validate_on_submit():
        localtime = time.strftime("%H:%M:%S", time.localtime())
        flash('提交成功: %s' % (localtime))
        keyword= form.keyword.data
        password= form.password.data
        type=form.search_type.data
        try:
            result=zohocheck.zoho_check(keyword,password,type)
        except OSError as E:
            result={'异常发生':'有错误发生请稍后重试，若多次重试后无效，请联系jason liu'}
    return render_template('zohocheck.html',result=result,form=form)



'''
    def zoho_check(keyword,password):

        #from xml.etree import ElementTree as ET
        #import urllib.parse
        import urllib.request
        #zoho模块名称，这里是查询clients
        module_name = 'Accounts'
        fo=open(mypath+'/app/files/yes.txt')
        real_password=fo.read()
        print(mypath)
        if password==real_password:
            fo=open(mypath+'/app/files/tno.txt')
            authtoken=fo.read()
            print (authtoken)
            #显示哪些列
            selectColumns='Account Owner,WP Client Number,Account Name,Client level'
            #搜索条件为根据client name搜索
            searchCondition='(Account Name|contains|*%s*)'%(keyword)
            #写入链接的参数
            params = {'authtoken':authtoken,'scope':'crmapi','selectColumns':selectColumns,'searchCondition':searchCondition}
            final_URL = "https://crm.zoho.com.cn/crm/private/xml/"+module_name+"/getSearchRecords"
            data = urllib.parse.urlencode(params).encode("utf-8")
            request = urllib.request.Request(final_URL,data)
            response = urllib.request.urlopen(request)
            #存储在str中
            xml_str=response.read()
            xml_str= xml_str.decode('utf-8')
            #print (xml_str)
            from bs4 import BeautifulSoup
            soup=BeautifulSoup(xml_str,'xml')
            text=soup.get_text(",")
            print('the feedback message is '+text)
            if text=='4422,There is no data to show':
                print ('There is no data to show')
                nonlocal error_message
                error_message=text
            else:
                #分割成列表
                import re
                output=re.split(r',',text)
                output = re.split(r',', text)
                #使用nonlocal 将变量定义为非全局变量
                nonlocal client_owner,client_name,wp_client_number
                client_owner = output[2]
                client_name = output[3]
                wp_client_number = output[4]
                print ('归属小组是%s\n客户名称是%s\nWP client number是 %s' %(client_owner,client_name,wp_client_number ))
        else:
            error_message = 'wrong password'


    if form.validate_on_submit():
        keyword=form.client_name.data
        #增加了password用来做简单验证
        password=form.password.data
        zoho_check(keyword,password)
        print('归属小组是%s\n客户名称是%s\nWP client number是 %s' % (client_owner, client_name, wp_client_number))


    return render_template('zohocheck.html',
        title = '',
        form = form,
        client_name=client_name,
        client_owner=client_owner,
        wp_client_number=wp_client_number,
        error_message=error_message,
                     )



'''