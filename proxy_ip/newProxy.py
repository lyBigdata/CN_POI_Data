# -*- coding:utf-8 -*-

'''
建立爬虫代理ip池:
    在爬取网站信息的过程中，有些网站为了防止爬虫，可能会限制每个ip的访问速度或访问次数。
对于限制访问速度的情况，我们可以通过time.sleep进行短暂休眠后再次爬取。
对于限制ip访问次数的时候我们需要通过代理ip轮换去访问目标网址。
所以建立并维护好一个有效的代理ip池也是爬虫的一个准备工作。
网上提供免费代理ip的网址很多，下面我们以西刺网站为例来建立一个有效的代理ip池。
'''

import time
import urllib2

#构造请求代理ip网站链接
#生成要爬取目标网址的链接
def get_url(url):     # 国内高匿代理的链接
    url_list = []
    for i in range(1,100):
        url_new = url + str(i)
        url_list.append(url_new)
    return url_list


#获取网页内容
#get_content：接受的参数是传入的目标网站链接
def get_content(url):     # 获取网页内容
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
    headers = {'User-Agent': user_agent}
    req= urllib2.Request(url=url, headers=headers)
    res  = urllib2.urlopen(req)
    contents = res.read()
    return contents.decode('utf-8')


#提取网页中ip地址和端口号信息
#get_info：接收从get_content函数传来的网页内容，并使用etree解析出ip和端口号，将端口号和ip写入data.
def get_info(content):      # 提取网页信息 / ip 端口
    from lxml import etree
    datas_ip = etree.HTML(content).xpath('//table[contains(@id,"ip_list")]/tr/td[2]/text()')
    datas_port = etree.HTML(content).xpath('//table[contains(@id,"ip_list")]/tr/td[3]/text()')
    with open("data.txt", "w") as fd:
        for i in range(0,len(datas_ip)):
            out = u""
            out += u"" + datas_ip[i]
            out += u":" + datas_port[i]
            fd.write(out + u"\n")     # 所有ip和端口号写入data文件

#验证代理ip的有效性
#verif_ip：使用ProxyHandler建立代理，使用代理ip访问某网址，查看是否得到响应。如数据有效，则保存到data2.txt文件
def verif_ip(ip,port):    # 验证ip有效性
    user_agent ='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
    headers = {'User-Agent':user_agent}
    proxy = {'http':'http://%s:%s'%(ip,port)}
    print(proxy)

    proxy_handler = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)

    test_url = "https://www.baidu.com/"
    req = urllib2.Request(url=test_url,headers=headers)
    time.sleep(6)
    try:
        res = urllib2.urlopen(req)
        time.sleep(3)
        content = res.read()
        if content:
            print('that is ok')
            with open("data2.txt", "a") as fd:       # 有效ip保存到data2文件夹
                fd.write(ip + u":" + port)
                fd.write("\n")
        else:
            print('its not ok')
    except urllib2.URLError as e:
        print(e.reason)


#主程序
if __name__ == "__main__":
    url = 'http://www.xicidaili.com/nn/'
    url_list = get_url(url)
    for i in url_list:
        print(i)
        content = get_content(i)
        time.sleep(3)
        get_info(content)

    with open("dali.txt", "r") as fd:
        datas = fd.readlines()
        for data in datas:
            print(data.split(u":")[0])
            # print('%d : %d'%(out[0],out[1]))
            verif_ip(data.split(u":")[0],data.split(u":")[1])