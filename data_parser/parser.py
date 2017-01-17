# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import re
from data_spider import spider
from data_storage import storageFiles

class parser(object):
    def __init__(self,url):
        #初始化空的list,用来存储数据
        self.resultData = []
        self.url = url

    def parserData(self,content):
        beautiful_soup = BeautifulSoup(content)

        #观察网页源代码发现：每个'''<div class="row"></div>'''中的内容即就是所需要解析的内容
        find_all = beautiful_soup.find_all(name="div",attrs={'class':'row'})

        #print type(find_all)
        #print find_all.__len__()

        for div in find_all:
            #print  type(div)
            #print "----------------------------------------"
            #print  div
            """
            <div class="row">
                        <div class="col-md-2">
                            <a href="/poi/province/2911.html" title="澳门特别行政区POI数据"><strong>澳门特别行政区</strong>(<small class="text-success">16948</small>)</a>
                        </div>
                        <div class="col-md-10">
                            <a href="/poi/district/2915/1.html" title="氹仔岛POI数据">氹仔岛(<small class="text-muted">1413</small>)</a>
                            <a href="/poi/district/2916/1.html" title="澳门半岛POI数据">澳门半岛(<small class="text-muted">14320</small>)</a>
                            <a href="/poi/district/2917/1.html" title="路氹城POI数据">路氹城(<small class="text-muted">906</small>)</a>
                            <a href="/poi/district/2918/1.html" title="路环岛POI数据">路环岛(<small class="text-muted">309</small>)</a>
                        </div>
            </div>
            """

            """
            #a_find = div.findAll(name='a',attrs={"href":re.compile(r'/poi')})
            a_find = div.findAll(name='a')
            '''
                <a href="/poi/province/2911.html" title="澳门特别行政区POI数据"><strong>澳门特别行政区</strong>(<small class="text-success">16948</small>)</a>
                <a href="/poi/district/2915/1.html" title="氹仔岛POI数据">氹仔岛(<small class="text-muted">1413</small>)</a>
                <a href="/poi/district/2916/1.html" title="澳门半岛POI数据">澳门半岛(<small class="text-muted">14320</small>)</a>
                <a href="/poi/district/2917/1.html" title="路氹城POI数据">路氹城(<small class="text-muted">906</small>)</a>
                <a href="/poi/district/2918/1.html" title="路环岛POI数据">路环岛(<small class="text-muted">309</small>)</a>
                '''
            for a in a_find:
                #print a
                lines = a.get("href")  #省份下的各区域数据连接url

                print lines
                #/poi/district/2926/1.html   九龙城区POI数据
                #存储成文件
                #storageFiles.storageFile().writeTxtFile(title.encode("utf-8"),lines.encode("utf-8"))
            """

            div_prov = div.find(name="div", attrs={'class' : 'col-md-2'})
            div_prov_data = div.find(name="div", attrs={'class' : 'col-md-10'})

            prov = str(unicode(div_prov.find("strong").string))  #省份信息

            #print prov

            data_all = div_prov_data.findAll("a")  #省份下的各区域数据连接url
            prov_quyu = []
            for a in data_all:
                #print a.get("href")
                prov_quyu.append(str(unicode(a.get("href"))))

            #print prov_quyu

            #字典类型{"澳门特别行政区":['/poi/district/2915/1.html', '/poi/district/2916/1.html', '/poi/district/2917/1.html', '/poi/district/2918/1.html']}
            prov_data = {prov:prov_quyu}

            self.resultData.append(prov_data)

        #遍历结果list,结果list中的数据是字典类型
        for data in self.resultData:
            #print data
            #遍历字典类型
            for l in data:
                #print str(l) #省份信息
                #print data[l] #list,省属下的市区数据URL
                for n in data[l]:
                    #print str(n)
                    shiurl =  self.url + str(n)
                    page_data = spider.spider().getPage(shiurl)
                    soup = BeautifulSoup(page_data)
                    soup_find_all = soup.find_all(name='a',attrs={"href":re.compile(r'/poi/district/')})
                    #print soup_find_all
                    #print type(soup_find_all)

                    city_data = []  #保存当前市下的所有县级别的数据的获取url
                    for href in soup_find_all: #得到当前市区下的县区的
                        href_get = href.get("href")
                        city_data.append(str(unicode(href_get)))
                        #print href_get

                    #遍历city数据url
                    for city in city_data:
                        cityurl = self.url+str(city)
                        page_data = spider.spider().getPage(cityurl)
                        soup = BeautifulSoup(page_data)

                        #<a href="javascript:;">1/43</a>
                        soup_soup_find_all = soup.find(name='a', attrs={"href": re.compile(r'javascript:;')})
                        count  = int(str(unicode(soup_soup_find_all.string)).split("/")[1])  #解析出分页数据

                        #print count

                        html = str(city).split("1.html")[0]
                        #print html

                        poi_data_url = []  #存储真正的数据最终抓取解析连接地址，当前县级别的

                        for i in range(1,count):
                            cityurl = self.url+html+str(i)+".html"
                            #print cityurl
                            page_data = spider.spider().getPage(cityurl)
                            soup = BeautifulSoup(page_data)

                            tr__find_all = soup.find_all("tr")
                            #print tr__find_all

                            for tr in tr__find_all:
                                #print type(tr.findAll("a"))
                                find_a = tr.findAll("a")

                                for link in find_a:
                                    #print link.get("href")
                                    poi_data_url.append(link.get("href"))

                        #遍历各个抓取链接，解析数据
                        for url in poi_data_url:
                            pass


if __name__ == "__main__":
    #使用代理ip抓取
    #pageCode = spider.spider(proxyHost="http://125.46.64.91:8080").getPageByProxy(u'http://www.poi86.com')

    #不使用代理ip抓取
    pageCode = spider.spider().getPage(u'http://www.poi86.com')
    parser(u'http://www.poi86.com').parserData(pageCode)