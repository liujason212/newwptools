from app import  app
from flask import render_template,flash,redirect
from app import dnscheck,dkim_dmarc,icp_check
from .forms import DnsCheck
import os,time
from app import sqlite_db

@app.route('/dnscheck.html',methods=['GET','POST'])
#@app.route("/index")
def dns():
    form=DnsCheck()
    result={}
    result_icp={}
    result1=''
    result2=''
    result3=''
    result4=''
    my_list = []
    if form.validate_on_submit():
        localtime = time.strftime("%H:%M:%S", time.localtime())
        domain_to_check = form.domain.data
        license_to_check = form.license.data
        flash('提交成功: %s 域名%s 平台地址%s' % (localtime,domain_to_check,license_to_check))
        password = form.password.data
        domain_to_check=domain_to_check.strip()
        license_to_check=license_to_check.strip()
        #根据用户选择进行查询选择
        if form.check_type.data=='dns-cn':
            result=dnscheck.dnscheck(domain_to_check,'CN')
            real_password = sqlite_db.get_db_password()
            if password == real_password:
                result_icp=icp_check.icp_check(domain_to_check)
            elif password !=real_password and password !='':
                result_icp='密码错误'
        if form.check_type.data=='dns-eu':
            result=dnscheck.dnscheck(domain_to_check,'EU')
        elif form.check_type.data=='dkim_dmarc':
            result=dkim_dmarc.new_dkim_dmarc(domain_to_check,license_to_check)
        #如果是生成dkim dmac运行如下代码
        elif form.check_type.data=='gen_dkim_dmarc':
            result= dkim_dmarc.gen_dkim_dmarc(domain_to_check,license_to_check)
            print('hello' + str(result))
            for key,value in result.items():
                print(key)
                my_list.append(key)
                my_list.append(value)
                print ('mylist'+str(my_list))
            result1 = my_list[0:1]
            result1 = ','.join(result1)
            result2 = my_list[1:2]
            result2 = ','.join(result2)
            result3 = my_list[2:3]
            result3 = ','.join(result3)
            result4 = my_list[3:4]
            result4 = ','.join(result4)
            return render_template('gen.html', form=form, result1=result1, result2=result2, result3=result3,result4=result4,domain_to_check=domain_to_check,license_to_check=license_to_check)

    return render_template('dnscheck.html', form=form, result=result,result_icp=result_icp)
