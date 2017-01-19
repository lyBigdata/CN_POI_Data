# -*- coding:utf-8 -*-
import  MySQLdb


class Py2MysqlClient(object):
    def __init__(self,host,passwd,port=3306,user="root"):
        try:
            self.connect = MySQLdb.connect(host=host,port=port,passwd=passwd,user=user,charset = "utf8")
        except Exception ,e:
            print e.message


    def creatDatabase(self,dbName):
        cursor = self.connect.cursor()
        sql_list = ['SET NAMES UTF8', 'SELECT VERSION()', 'CREATE DATABASE %s' % dbName]
        try:
            map(lambda sql: cursor.execute(sql), sql_list)
            self.connect.commit()

        except MySQLdb.Error, e:
            self.connect.rollback()
            print e.message

        finally:
            cursor.close()

    def creatTable(self,dbName,sql):
        cursor = self.connect.cursor()
        sqls = ["USE %s" % dbName, "SET NAMES UTF8"]
        sqls.append("ALTER DATABASE %s DEFAULT CHARACTER SET 'utf8'" % dbName)
        sqls.append(sql)
        try:
            map(lambda sql:cursor.execute(sql), sqls)
            self.connect.commit()
        except MySQLdb.Error, e:
            self.connect.rollback()
            print e.message
        finally:
            cursor.close()


    def operatorSql(self,optSql):
        cursor = self.connect.cursor()
        sqls = []
        sqls.append(optSql)
        try:
            map(lambda sql:cursor.execute(sql), sqls)
            self.connect.commit()
        except MySQLdb.Error, e:
            self.connect.rollback()
            print e.message
        finally:
            cursor.close()



if __name__=="__main__":
    mysql_client = Py2MysqlClient(host="192.168.1.8", port=2849, passwd="123456",user="ndmp")
    #mysql_client.creatDatabase(dbName="liuyuTest")
    dataSql= '''CREATE TABLE IF NOT EXISTS WORDS
                (
                id INT(11) AUTO_INCREMENT PRIMARY KEY,
                word VARCHAR(100) NOT NULL,
                pinyin VARCHAR(100) NOT NULL,
                showtimes INT(11) NOT NULL DEFAULT 0,
                weight FLOAT(11) NOT NULL DEFAULT 0.0,
                corpus_scale INT(11),
                cixing VARCHAR(10) NOT NULL,
                type1 VARCHAR(30) NOT NULL,
                type2 VARCHAR(30) NOT NULL,
                source VARCHAR(50) NOT NULL,
                gram INT(11),
                meaning TEXT NOT NULL,
                UNIQUE (word)
                )
              '''
    #mysql_client.creatTable(dbName="liuyuTest",sql=dataSql)
