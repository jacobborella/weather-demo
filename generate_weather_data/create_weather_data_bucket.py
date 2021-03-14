import decimal
import datetime
from random import seed
from random import randint
import copy

def gridder():
    seed(datetime.datetime.now().timestamp())
    BUCKET_SIZE=100
    startTime=datetime.datetime(2011,3,11,0,0)
    endTime=datetime.datetime(2021,3,11,0,0)
    pos = 1
    lonmin = -180 #-180
    lonmax = 180 #180
    latmin = -90 #-90
    latmax = 90 #90
    orglatmin = latmin
    stepsize = 1
    while lonmin < lonmax:
        minTime=copy.deepcopy(startTime)
        while minTime < endTime:
            maxTime = copy.deepcopy(minTime)
            maxTime += datetime.timedelta(hours=6) * (BUCKET_SIZE - 1)
            gj = {
                "_id": {
                    "loc": str(float(lonmin)) + str(float(latmin)), 
                    "min_validTime": {"$date": str(minTime.isoformat()) + ".000+00:00"},
                    "max_validTime": {"$date": str(maxTime.isoformat()) + ".000+00:00"}
                }, 
                "calcs": []
            }
            for i in range(BUCKET_SIZE):
                gj['calcs'].append({'temp': randint(-30, 40)})
            minTime += datetime.timedelta(hours=6) * BUCKET_SIZE
            yield(gj)
        latmin += (stepsize)
        pos += 1
        if latmin == latmax:
            latmin = orglatmin
            lonmin += (stepsize)
print("[")
j = 0
for i in gridder():
    if j > 0:
        print(",")
    print(str(i).replace("'","\""))
    j += 1
print("]")
