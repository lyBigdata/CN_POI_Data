# -*- coding:utf-8 -*-

import urllib2

class spider(object):
    def __init__(self):
        #初始化headers
        self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                        'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding':'en-us',
                        'Connection':'keep-alive',
                        'Referer':'http://www.baidu.com/'}

    def  getPage(self,url):
        try:
            #构建请求的request
            request = urllib2.Request(url = url,headers = self.headers)
            #利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            #将页面转化为UTF-8编码
            page = response.read().decode('utf-8')

            return page
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接目标地址失败。。。错误原因：",e.reason
                return None


if __name__ == "__main__":
    pageCode = spider().getPage("http://www.poi86.com")
    print pageCode

