import requests
import tldextract

def icp_check(domain):
    domain_extract = tldextract.extract(domain)
    domain_1 = domain_extract[1]
    domain_2 = domain_extract[2]
    domain = domain_1 + '.' + domain_2
    print(domain)
    result=''
    url='http://api.juheapi.com/japi/beian'
    key='c222dac155d7123ecef69c6807cdfbcd'
    type='1'
    keyword=domain
    v='1.0'
    params={'key':key,'type':type,'keyword':keyword,'v':v}
    try:
        r=requests.get(url,params=params,timeout=30)
        result=r.json()
        print(result)
        result = result['result'][0]
        print(result)
        return result
    except Exception:
        if len(result)>0:
            return result
        else:
            result={'发生错误':'请稍后重试'}
            return result
