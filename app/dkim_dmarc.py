#dkim生成常量
PREFIX_DKIM_DOMAIN='dmddkim._domainkey.'
PREFIX_DKIM_CNAME='dmddkim._domainkey.'
PREFIX_DMARC_DOMAIN='_dmarc.'
PREFIX_DMARC_TXT='v=DMARC1;p=none;rua=mailto:dmarc@'
import requests,json,re

def new_dkim_dmarc(domain,license):
    #进行dkim的查询
    result={}
    newdata_list=[]
    #根据信息生成dkim的domain
    dkim_domain = PREFIX_DKIM_DOMAIN + domain.strip()
    #将这个信息添加到result字典中
    result['dkim'] = ['生成正确的dkim domain: '+dkim_domain]
    print('dkim_domain:' + dkim_domain)
    #根据信息生成正确的dkim值
    dkim_correct_record = PREFIX_DKIM_CNAME + license.strip()
    print('dkim_correct_record:'+dkim_correct_record)
    #将值加入到列表中
    result['dkim'].append('生成正确的CNAME记录：'+dkim_correct_record)
    result['dkim'].append('下方为查询结果')
    #定义查询链接
    dnslookup = 'https://dns.google.com/resolve?name=' + dkim_domain + '&type=5'
    print('dkim查询地址'+dnslookup)
    proxies = {
        "http": "http://127.0.0.1:1087",
        "https": "http://127.0.0.1:1087", }
    #开始获取google dns的信息
    try:
        r = requests.get(dnslookup, timeout=3)
        #r = requests.get(dnslookup, proxies=proxies,timeout=4)
        r = r.json()
        print('google查询数据:')
        print(r)
        if len(r['Answer']) == 1:
            data = (r['Answer'][0]['data'])
            if data.startswith('"') and data.endswith('"'):
                data = data[1:-1]
            # 去除查询结果后面的.
            if data.endswith('.'):
                data = data[:-1]
            data = "".join(data.split())
        # 判断得到的查询的结果长度是1个以上的话运行如下代码
        elif len(r['Answer']) > 1:
            newdata = r['Answer']
            # 将多个答案整合到一起，并做一下数据处理
            for x in newdata:
                if x['data'].startswith('"') and x['data'].endswith('"'):
                    x['data'] = x['data'][1:-1]
                # 去除查询结果后面的.
                if data.endswith('.'):
                    data = data[:-1]
                data = "".join(data.split())
                newdata_list.append(x['data'])
            data = newdata_list
        result['dkim'].append(data)
    #如果cname查询不到，尝试查询txt记录
    except KeyError:
        print('there is no value of cname')
        #查询dkim的txt记录
        dnslookup = 'https://dns.google.com/resolve?name=' + dkim_domain + '&type=16'
        try:
            r = requests.get(dnslookup, timeout=3)
            #r = requests.get(dnslookup, proxies=proxies, timeout=4)
            r = r.json()
            print('google查询数据:')
            print(r)
            if len(r['Answer']) == 1:
                data = (r['Answer'][0]['data'])
                if data.startswith('"') and data.endswith('"'):
                    data = data[1:-1]
                # 去除查询结果后面的.
                if data.endswith('.'):
                    data = data[:-1]
                data = "".join(data.split())
            # 判断得到的查询的结果长度是1个以上的话运行如下代码
            elif len(r['Answer']) > 1:
                newdata = r['Answer']
                # 将多个答案整合到一起，并做一下数据处理
                for x in newdata:
                    if x['data'].startswith('"') and x['data'].endswith('"'):
                        x['data'] = x['data'][1:-1]
                    # 去除查询结果后面的.
                    if x['data'].endswith('.'):
                        x['data'] = x['data'][:-1]
                        x['data'] = "".join(x['data'].split())
                    newdata_list.append(x['data'])
                data = newdata_list
            result['dkim'].append(data)
            print(data)
            #查询对于的正确dkim txt值
            dnslookup = 'https://dns.google.com/resolve?name=' + dkim_correct_record + '&type=16'
            r = requests.get(dnslookup, timeout=3)
            #r = requests.get(dnslookup, proxies=proxies, timeout=4)
            r = r.json()
            dkim_correct_record=[dkim_correct_record]
            dkim_txt_data = (r['Answer'][0]['data'])
            if dkim_txt_data.startswith('"') and dkim_txt_data.endswith('"'):
                dkim_txt_data = dkim_txt_data[1:-1]
                # 去除查询结果后面的.
            if dkim_txt_data.endswith('.'):
                dkim_txt_data = dkim_txt_data[:-1]
            dkim_txt_data = "".join(dkim_txt_data.split())
            dkim_correct_record.append(dkim_txt_data)
            #加入TXT查询结果的提示，以便跳过后续验证
            index_result = result['dkim'].index('下方为查询结果')
            result['dkim'][index_result] = ['没有CNAME查询结果，下方为TXT查询结果，请联系TS进行验证']
        except KeyError:
            print('there is no value of txt')
            result['dkim'].append('没有任何配置信息')
    except requests.exceptions.ConnectionError:
        print('timeout')
        result['dkim'].append('网络超时')
    print('dkim最后查询值')
    print(result)
    #进行dmarc的查询
    #根据信息生成dmarc的domain
    dmarc_domain = PREFIX_DMARC_DOMAIN + domain
    print(dmarc_domain)
    #根据信息生成正确的dmarc值
    dmarc_correct_record = PREFIX_DMARC_TXT + domain
    print(dmarc_correct_record)
    #将这个信息添加到result字典中
    result['dmarc'] = ['生成正确的Dmarc domain: '+dmarc_domain]
    result['dmarc'].append('生成正确的TXT记录  :  '+dmarc_correct_record)
    result['dmarc'].append('下方为查询结果')
    print('dmarc域名和值')
    print(result)
    #定义查询链接
    dnslookup = 'https://dns.google.com/resolve?name=' + dmarc_domain + '&type=16'
    print('dmarc查询地址'+dnslookup)
    try:
        r = requests.get(dnslookup, timeout=3)
        #r = requests.get(dnslookup, proxies=proxies,timeout=4)
        r = r.json()
        print('google查询数据:')
        print(r)
        if len(r['Answer']) == 1:
            data = (r['Answer'][0]['data'])
            if data.startswith('"') and data.endswith('"'):
                data = data[1:-1]
                # 去除查询结果后面的.
            if data.endswith('.'):
                data = data[:-1]
            data = "".join(data.split())
        # 判断得到的查询的结果长度是1个以上的话运行如下代码
        elif len(r['Answer']) > 1:
            newdata = r['Answer']
            # 将多个答案整合到一起，并做一下数据处理
            for x in newdata:
                if x['data'].startswith('"') and x['data'].endswith('"'):
                    x['data'] = x['data'][1:-1]
                # 去除查询结果后面的.
                if x['data'].endswith('.'):
                    x['data'] = x['data'][:-1]
                    x['data'] = "".join(x['data'].split())
                newdata_list.append(x['data'])
            data = newdata_list
        result['dmarc'].append(data)
    except KeyError:
        print('there is no value')
        result['dmarc'].append('没有任何配置信息')
    except requests.exceptions.ConnectionError:
        print('timeout')
        result['dmarc'].append('网络超时')
    print('dkim dmarc 查询结果')
    print(result)
    print(result['dkim'])
    #开始进行结果验证
    if '网络超时'not in str(result['dkim']) and '没有CNAME查询结果，下方为TXT查询结果，请联系TS进行验证' not in str(result['dkim']) and '没有任何配置信息'not in str(result['dkim']):
        print('dkim正确值')
        print(dkim_correct_record)
        for x in result['dkim'][3:]:
            print('bug')
            print(x)
            if x ==dkim_correct_record:
                result['dkim'].append('配置正确')
            elif x in dkim_correct_record:
                result['dkim'].append('配置正确')
            else:
                x_regex1=re.sub('webpower.asia', 'dmdelivery.com',x, count=0, flags=re.IGNORECASE)
                x_regex2=re.sub('dmdelivery.com','webpower.asia',x, count=0, flags=re.IGNORECASE)
                if dkim_correct_record==x_regex1 or dkim_correct_record==x_regex2:
                    result['dkim'].append('配置正确')
                else:
                    result['dkim'].append('配置错误')

    print('dkim验证结果')
    print(result)
    if '网络超时' not in str(result['dmarc']) and '没有任何配置信息' not in str(result['dmarc']) :
        print('dmarc正确值' + dmarc_correct_record)
        for x in result['dmarc'][3:]:
            if x ==dmarc_correct_record:
                result['dmarc'].append('配置正确')
            else:
                result['dmarc'].append('配置错误')
    print('dmarc验证结果')
    print(result)
    print('模块返回值')
    print(result)
    return result



def gen_dkim_dmarc(domain, license):
    # 需要根据用户填入的信息生成正确的dkim域名和对应的cname值
    gen_dkim_dmarc_result={}
    dkim_domain = PREFIX_DKIM_DOMAIN + domain
    print(dkim_domain)
    dkim_correct_record = PREFIX_DKIM_CNAME + license
    print(dkim_correct_record)
    #根据以上信息，生成正确的dmarc域名和对应的txt值
    dmarc_domain=PREFIX_DMARC_DOMAIN+domain
    print(dmarc_domain)
    dmarc_correct_record=PREFIX_DMARC_TXT+domain
    print(dmarc_correct_record)
    #将生成的信息添加到dictionary中
    gen_dkim_dmarc_result[dkim_domain]=dkim_correct_record
    print(str(gen_dkim_dmarc_result))
    gen_dkim_dmarc_result[dmarc_domain]=dmarc_correct_record
    print(str(gen_dkim_dmarc_result))
    return gen_dkim_dmarc_result


