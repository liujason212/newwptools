#运行google dns api进行检查
def dnscheck(domain,geo):
    import requests
    import json

    # google dns API对于的参考代码
    dnsrecordtypes = {
        'A': '1',
        #'CNAME': '5',
        'MX': '15',
        'TXT': '16',
        #'SPF': '99',
    }

    # 反向将API中的参考代码转化
    question_type = {
        '1': 'A',
        #'5': 'CNAME',
        '15': 'MX',
        '16': 'TXT',
        #'99': 'SPF',

    }
    # dmd 国内平台的正确配置信息
    correct_value = {
        'A': ['61.147.84.43', '61.147.84.45', '61.147.84.44', '61.147.84.47'],
        'MX': ['virtualmail.webpower.asia', 'bouncemailcn.dmdelivery.com'],
        'TXT': ['v=spf1 a mx include:virtualmail.webpower.asia ~all','v=spf1 a mx include:virtualcn.dmdelivery.com -all','v=spf1 a mx include:virtualcn.dmdelivery.com ~all','v=spf1 a mx include:virtualmail.webpower.asia -all']

    }

    correct_value_eu={
        'A': ['91.197.72.25'],
        'MX': ['virtualmail.webpower.eu','virtualmail.dmdelivery.com'],
        'TXT': ['v=spf1 a mx include:virtualmail.webpower.eu ~all','v=spf1 a mx include:virtualmail.webpower.eu -all','v=spf1 a mx include:virtual.dmdelivery.com ~all','v=spf1 a mx include:virtual.dmdelivery.com -all']

    }
    answer = {'key': 'value'}
    dns_result={}
    dns_result_list=[]
    #data=''
    newdata_list = []

    for k in dnsrecordtypes :
        typenumber=dnsrecordtypes[k]
        typenumber=str(typenumber)
        dnslookup = 'https://dns.google.com/resolve?name=' + domain + '&type=' + typenumber
        print(dnslookup)
        proxies = {
            "http": "http://127.0.0.1:1087",
            "https": "http://127.0.0.1:1087", }
        try:
            #r = requests.get(dnslookup,proxies=proxies,timeout=3)
            r = requests.get(dnslookup,timeout=3)
            r = r.json()
            print(r)
            #显示需要查询什么
            question=r['Question'][0]['type']
            question=str(question)
            question=question_type[question]
            print(question)
            #判断得到的查询结果是1个的话运行如下代码
            if len(r['Answer'])==1:
                data = (r['Answer'][0]['data'])
            # 判断得到的查询的结果长度是1个以上的话运行如下代码
            elif len(r['Answer']) >1:
                newdata=r['Answer']
                #将多个答案整合到一起，并做一下数据处理
                for x in newdata:
                    print(x)
                    if x['data'].startswith('"') and x['data'].endswith('"'):
                        x['data'] = x['data'][1:-1]
                    elif question == 'MX':
                        x['data'] = x['data'][2:-1].strip()
                    try:
                        data = ' '.join(data.split())
                    except Exception:
                        pass
                    newdata_list.append(x['data'])
                    print(newdata_list)
                data=newdata_list
                print(data)
            #对单个答案进行数据整理
            if type(data)==type('string') and data.startswith('"') and data.endswith('"'):
                data=data[1:-1]
            if question=='MX'and type(data)==type('string'):
                data=data[2:-1].strip()
            # 将2个空格改为1个
            try:
                data = ' '.join(data.split())
            except Exception:
                pass
            print(data)
            #将结果和问题做成dict
            dns_result[question]=[data]
            #只是为了调用方便
            dns_result_list=dns_result[question]
            print(dns_result_list)
            #对结果，和国内平台的正确信息进行匹配
            if geo=='CN':
                # 如果data是列表的话，需要做循环判断
                if type(data) != type('string'):
                    save_list = []
                    for index, x in enumerate(data):
                        save_list.append(x)
                        if x in correct_value[question]:
                            save_list.append('配置正确')
                        else:
                            save_list.append('配置不正确')
                    dns_result[question] = save_list
                elif type(data) == type('string') and data in correct_value[question]:
                    dns_result_list.append('配置正确')
                    print('correct')
                else:
                    print('%s配置不正确' % (question))
                    dns_result_list.append('配置不正确')
            # 对结果，和国内平台的正确信息进行匹配
            elif geo=='EU':
                #如果data是列表的话，需要做循环判断
                if type(data)!=type('string') :
                    save_list=[]
                    for index,x in enumerate(data):
                        save_list.append(x)
                        if x in correct_value_eu[question]:
                            save_list.append('配置正确')
                        else:
                            save_list.append('配置不正确')
                    dns_result[question]=save_list
                elif type(data)==type('string') and data in correct_value_eu[question] :
                    dns_result_list.append('配置正确')
                    print('correct')
                else:
                    print('%s配置不正确' % (question))
                    dns_result_list.append('配置不正确')
        #如果没有查询结果或者网络超时
        except KeyError:
            print('there is no value')
            dns_result[question]=['没有查询结果']
        except requests.exceptions.ConnectionError:
            print ('timeout')
            dns_result='网络连接超时'
            break
        except requests.ReadTimeout:
            print('read timeout')
            dns_result='网络连接超时'
            break


    print('模块返回')
    print(dns_result)
    return dns_result
