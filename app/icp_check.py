import requests
import tldextract

def icp_check(domain):
    domain_extract = tldextract.extract(domain)
    domain_1 = domain_extract[1]
    domain_2 = domain_extract[2]
    domain = domain_1 + '.' + domain_2
    print(domain)
    url='http://api.juheapi.com/japi/beian'
    key='c222dac155d7123ecef69c6807cdfbcd'
    type='1'
    keyword=domain
    v='1.0'
    params={'key':key,'type':type,'keyword':keyword,'v':v}
    r=requests.get(url,params=params)
    result=r.json()
    print(result)
    if 'exceeds the limit' in str(result):
        return result
    elif result['error_code']== 0:
        result=result['result'][0]
        print(result)
        return result
    else:
        return result
