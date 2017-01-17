# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import re
from data_spider import spider
from data_storage import storageFiles

class parser(object):
    def __init__(self):
        #初始化空的list,用来存储数据
        self.resultData = []

    def parserData(self,content):
        beautiful_soup = BeautifulSoup(content)

        #观察网页源代码发现：每个'''<div class="row"></div>'''中的内容即就是所需要解析的内容
        find_all = beautiful_soup.find_all(name="div",attrs={'class':'row'})

        #print type(find_all)
        #print find_all.__len__()

        for div in find_all:
            print  type(div)
            print "----------------------------------------"
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
            data_all = div_prov_data.findAll("href")  #省份下的各区域数据连接url

            prov_data = (prov,data_all)

            self.resultData.append(prov_data)

if __name__ == "__main__":
    pageCode = spider.spider(proxyHost="http://125.46.64.91:8080").getPageByProxy(u'http://www.poi86.com')
    parser().parserData(pageCode)