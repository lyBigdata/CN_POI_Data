#!/usr/bin/env python
# -*- coding:utf-8 -*-


# Created by zhenzi.
# User: zhenzi
# Date: 2016/12/20
# Time: 20:13
# Verdor: NowledgeData
# To change this template use File | Settings | File Templates.
#

__author__ = "zhenzi"



from math import *
from geopy.distance import vincenty

# input Lat_A 纬度A
# input Lng_A 经度A
# input Lat_B 纬度B
# input Lng_B 经度B
# output distance 距离(km)
def calcDistance(Lat_A, Lng_A, Lat_B, Lng_B):
    ra = 6378.137 * 1000  # 6378.140 赤道半径 (km)
    rb = 6356.755 * 1000 # 极半径 (km)
    flatten = (ra - rb) / ra  # 地球扁率
    rad_lat_A = radians(Lat_A)
    rad_lng_A = radians(Lng_A)
    rad_lat_B = radians(Lat_B)
    rad_lng_B = radians(Lng_B)
    pA = atan(rb / ra * tan(rad_lat_A))
    pB = atan(rb / ra * tan(rad_lat_B))
    xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
    c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
    c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (xx + dr)
    return distance

def pointDistance(pointA, pointB):
    return calcDistance(pointA[0], pointA[1], pointB[0], pointB[1])


if __name__ == "__main__":
    A = (32.060255, 118.796877) # 南京
    B = (39.904211, 116.407395) # 北京
    distance = pointDistance(A, B)
    print('Distance={0:10.3f} m'.format(distance))

    print(vincenty(A, B, ellipsoid='GRS-80').m)
