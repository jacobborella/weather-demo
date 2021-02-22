import gdal
import numpy as np
import statistics
import osr
import math
import pymongo
import datetime
import sys

# Open file
print( 'Number of arguments:' + str( len(sys.argv)) + 'arguments.')
print( 'Argument List:' +  str(sys.argv))

dataset = gdal.Open(sys.argv[1], gdal.GA_ReadOnly)
#connect to mongo
connection = pymongo.MongoClient('mongodb+srv://<user>:<password>@<clustername>.vortb.mongodb.net/test?retryWrites=true')
db = connection['test']
if(len(sys.argv) > 2 and sys.argv[2] == 'TRUE'):
  db.weather.drop()
  db.weather.create_index([('_id.validTime', 1), ('_id.loc', '2dsphere')])

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


print("(y_size, x_size, rastercount)" + str(range(x_size)) + ", " + str(range(y_size)) + ", " + str(range(dataset.RasterCount)))

#TODO: for now a constant gribRefTime is assumed for the whole dataset
gribRefTime=int(datetime.datetime(2020,12,20,18,0).timestamp())
bulkUpdates=[]
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

    for idx, m in enumerate(dataArray):
      gribValidTime = datetime.datetime.fromtimestamp(float(metadata[idx]['GRIB_VALID_TIME'].split(' ')[2]))
      gribValidTime = int(gribValidTime.timestamp())
      value = int(m[row][col] * 100)#TODO verify trunc to two digits
      insertElement={}
      insertElement['calcs'] = []
      #TODO: do some transformation, since grid precision is 0.25
  #    insertElement['_id'] = str(int(longitude * 100)) + str(int(longlat[1] * 100)) + str(gribRefTime)
      _id = {
            'loc': [ longitude, longlat[1]],
            'validTime': gribValidTime
      }
      #insertElement['gribRefTime'] = int(gribRefTime.strftime("%Y%m%d%H"))#TODO assumed same for all datapoints in a raster
      #insertElement['gribRefTime']=gribRefTime
      #insertElement['TMP'][str(int(gribValidTime.strftime("%Y%m%d%H")))] =  value #TODO: TMP hardcoded
      bulkUpdates.append(pymongo.UpdateOne(
          {'_id': _id},
          {'$push': {'calcs': {
             'refTime': gribRefTime,
             'TMP': value
          }}}, upsert=True
          ))
  print("row " + str(row) + " processed.")
  if(row%5 == 0):
    db.weather.bulk_write(bulkUpdates)
    print("wrote to db after row " + str(row))
    bulkUpdates=[]

