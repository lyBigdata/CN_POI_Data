# -*- coding:utf-8 -*-

import redis

class Py2RedisClient(object):

    def __init__(self, host, port,passwood,db=0):
        self.redis = redis.StrictRedis(host=host,port=port,password=passwood,db=db)
        try:
            pass
        except Exception, e:
            print e.message

    def write(self, key, value):
        try:
            redis_redis = redis.Redis(self.redis)
            redis_redis.setnx(key, value)
        except Exception, e:
            print e.message

    def read(self, keyName):
        try:
            redis_redis = redis.Redis(self.redis)
            keys = redis_redis.keys(keyName)
            for key in keys:
                print(str(key))
        except Exception, e:
            print e.message


if __name__ == "__main__":
    redis_client = Py2RedisClient(host="192.168.1.115", port=9999, passwood="123")
    redis_client.read("*")




