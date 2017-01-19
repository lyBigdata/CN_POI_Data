# -*- coding:utf-8 -*-

import pymongo

class  Py2MongoClient(object):
    def __init__(self, host, port,dbname,collectionname):
        self.mongo_client = pymongo.MongoClient(host=host, port=port)  #建立连接
        self.client_dbname = self.mongo_client[dbname]  #指定要操作的库
        self.colection_name = self.client_dbname[collectionname] #指定要操作的集合

    def findAllRecodeCount(self):  #记录总数
        find__count = self.colection_name.find().count()
        return find__count

    def insertRecode(self,data):  #插入记录到数据库
        self.colection_name.insert(data)


    def findBy(self,filterexpr):   #根据条件查询数据,若有，返回一条记录；若没有，返回None
        one = self.colection_name.find_one(filterexpr)
        return  one

    def delRecode(self,delexpr):   #根据条件删除记录
        self.colection_name.delete_many(delexpr)

    def returnAllData(self):  #返回所有的记录
        result=[]
        for one in self.colection_name.find():
            result.append(one)
        return  result

    def clearAlldatas(self):  #清空集合所有记录
        self.colection_name.remove()


if __name__ == "__main__":
    client = Py2MongoClient("192.168.1.115", 8888, "lydb", "zjy")

    information = [{"name": "quyang", "age": "25"},{"name": "liuhuan", "age": "20"}]

    client.insertRecode(information)
    print client.findAllRecodeCount()

    find_by = client.findBy({"name": "liuyu"})
    print  find_by

    client.delRecode({"name": "quyang"})

    print  client.findAllRecodeCount()

    all_data = client.returnAllData()

    for dataone in all_data:
        print dataone
    print type(all_data)

    #client.clearAlldatas()
