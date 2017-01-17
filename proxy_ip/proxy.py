# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from data_spider import spider
import urllib2
import gevent
import  sys

reload(sys)
sys.setdefaultencoding('utf-8')

class proxy(object):
    def __init__(self,url,filename):
        self.url = url
        self.fileName = filename
        self.all_page_count = 0

    def parserIpData(self,content):
        soup = BeautifulSoup(content)
        find_all = soup.find(name="div", attrs={"class": "pagination"})

        all_find_all = find_all.findAll(name="a")

        self.all_page_count = int(unicode(all_find_all[len(all_find_all)-2].string))

        #print self.all_page_count
        #print type(self.all_page_count)

        for a in range(1,self.all_page_count):
            thisurl = self.url+str(a)
            print thisurl
            thispage = spider.spider().getPage(thisurl)
            thissoup = BeautifulSoup(thispage)
            ips = thissoup.findAll('tr')
            try:
                f = open(self.fileName,"a")
                for x in range(1,len(ips)):
                    ip = ips[x]
                    tds = ip.findAll("td")
                    #提取代理ip
                    host = tds[1].contents[0]
                    #代理ip端口
                    port = tds[2].contents[0]
                    #代理ip使用的协议
                    protocol = tds[5].contents[0]

                    #检测ip的可用性,如果可用就写文件
                    if self.checkAlive(ip=host,port=port,protocol=protocol):
                        ip_temp = host+"\t"+port+"\t"+protocol+"\n"
                        print ip_temp
                        f.write(ip_temp)

            except Exception,e:
                print e.message
            finally:
                if not f.closed:
                    f.close()

    def checkAlive(self,ip,port,protocol):
        testUrl = "https://www.baidu.com/"
        req_timeout = 3
        cookies = urllib2.HTTPCookieProcessor()

        proxyHost = ""
        if protocol == 'HTTP' or protocol == 'HTTPS':
            proxyHost = {"http":r'http://%s:%s' % (ip, port)}
            #print proxyHost

        proxyHandler = urllib2.ProxyHandler(proxyHost)
        opener = urllib2.build_opener(cookies, proxyHandler)
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]

        try:
            req = opener.open(testUrl, timeout=req_timeout)
            result = req.read()
            #print result
            gevent.sleep(2)
            return  True
        except urllib2.HTTPError as e:
            print  e.message
            return False


if __name__=="__main__":
    url = 'http://www.xicidaili.com/nn/'
    filename = "F:/proxy/proxy.txt"

    #不使用使用代理抓取
    page = spider.spider().getPage(url)

    #使用代理抓取
    #page = spider.spider(proxyHost="http://125.46.64.91:8080").getPageByProxy(url)
    proxy(url,filename).parserIpData(page)