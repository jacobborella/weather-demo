import gdal
import numpy as np
import statistics
import osr
import math
import datetime
import sys

def readData(filename, injectGrid):
    # Open file
    dataset = gdal.Open(filename, gdal.GA_ReadOnly)

    #calculate reference time from the file timestamp
    ts=sys.argv[1].partition("tmp2m.01.")[2].split(".")[0]
    gribRefTime=datetime.datetime(int(ts[0:4]),int(ts[4:6]),int(ts[6:8]),int(ts[8:10]),0)

    # Preparing transformation
    x_size = dataset.RasterXSize
    y_size = dataset.RasterYSize

    old_cs=osr.SpatialReference()
    old_cs.ImportFromWkt(dataset.GetProjection())

    wgs84_wkt = """
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]"""
    new_cs = osr.SpatialReference()
    new_cs .ImportFromWkt(wgs84_wkt)
    transform = osr.CoordinateTransformation(old_cs,new_cs) 
    geo_t = dataset.GetGeoTransform ()

    #cache raster bands
    dataArray = []
    metadata = []
    for i in range(dataset.RasterCount):
        rasterBand=dataset.GetRasterBand(i+1)
        dataArray.append(rasterBand.ReadAsArray())
        metadata.append(rasterBand.GetMetadata())


    #get reference time from the dataset
    # Parsing for valid data points
    for row in range(y_size):
        for col in range(x_size):
            #calc position 
            longlat = transform.TransformPoint(geo_t[0] + geo_t[1]*col, geo_t[3] + geo_t[5]*row)
            longitude = 180 - longlat[0]
            if(longitude < -180):
                longitude = -180.0
            if(longitude > 180):
                longitude = 180.0

            longitude=int(longitude*100)/100
            longlat=int(longlat[1]*100)/100

            loc_key=str(longitude) + ":" + str(longlat)
            if(injectGrid):
                yield({"_id": loc_key, "geometry":{"type": "Point", "coordinates": [longitude, longlat]}})
            else:
                insertElement={
                '_id': {
                    'loc': loc_key,
                    'refTime': {"$date": str(gribRefTime.isoformat()) + ".000+00:00"}
                },
                'calcs': []
                }

                for idx, m in enumerate(dataArray):
                    #gribValidTime = datetime.datetime.fromtimestamp(float(metadata[idx]['GRIB_VALID_TIME'].split(' ')[2]))
                    value = int(m[row][col] * 100)#TODO verify trunc to two digits
                    insertElement['calcs'].append(value)
                yield(insertElement)


print("[")
j = 0
for i in readData(sys.argv[1], sys.argv[2].lower()=='true'):
    if j > 0:
        print(",")
    print(str(i).replace("'","\""))
    j += 1
print("]")
