# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class storageFile(object):
    def __init__(self):
        #数据的存储目录
        self.dataDir = 'F:/CNPOIdata/'

    def  writeTxtFile(self,fileName,strs):
        file_path = self.dataDir.encode("utf-8") + fileName.encode("utf-8") + u'.txt'.encode("utf-8")

        try:
            f = open(file_path, "a")
            f.writelines(strs.encode("utf-8"))
        except IOError, e:
            f.close()
            print e.message
        finally:
            f.close()



