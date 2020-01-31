from webapp.models import  PCR
import ogr
import gdal
import osr
import osgeo
import os, os.path, shutil
import osgeo.ogr
import osgeo.osr
from osgeo import osr
import osgeo.ogr as ogr
import osgeo.osr as osr
from gdalconst import *
import csv
from osgeo import ogr
import operator
from math import radians, cos, sin, asin, sqrt, atan2, degrees
import glob

def number_of_available_drivers():
    cnt = ogr.GetDriverCount()
    formatsList = []  # Empty List
    for i in range(cnt):
        driver = ogr.GetDriver(i)
        driverName = driver.GetName()
        if not driverName in formatsList:
            formatsList.append(driverName)
    formatsList.sort()
    reply= input ("whether want to see driver list answer in yes/no")
    if reply =="yes":
        print ("\n".join(formatsList))
    return (cnt,formatsList)


def creating_directory():
    folderName = "POLICELOCATION"
    folderPath = "C:/Users\Hp\Desktop\DATA"
    path = folderPath + '\\' + folderName
    if os.path.exists("%s" % path):
        shutil.rmtree("%s" % path)
    os.mkdir("%s" % path)
    return (path, folderName)

def entered_driver_availiblity(count,list):
    numberOfDriver=count
    driverList = list
    x = input("Enter driver name:")
    if x in driverList:
        print("ok")
        return x
    else:
        print("Value Error:%s is not in list" %x)

def plocation():
    a = PCR.object.all()
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    folderLocation, folderName = creating_directory()
    name = "POLICELOCATION"
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("layer", spatialReference)
    fieldDef = osgeo.ogr.FieldDefn("name", osgeo.ogr.OFTInteger64)
    fieldDef.SetWidth(10)
    dstLayer.CreateField(fieldDef)
    for i in range(len(a)):
        lat = a[i].mpoly[1]
        lon = a[i].mpoly[0]
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(lon, lat)
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        feature.SetGeometry(point)
        feature.SetField("name", int(a[i].pcrid))
        dstLayer.CreateFeature(feature)
        feature.Destroy()
    dstFile.Destroy()
    return dstPath

#plocation()