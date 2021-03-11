import decimal
import datetime
from random import seed
from random import randint
import copy

def gridder():
    seed(datetime.datetime.now().timestamp())
    NUMBER_OF_DATES=4*10#10 days worth of data in 6 hour intervals
    validTime=datetime.datetime(2021,3,11,0,0)                              #time the forecast is valid
    pos = 1
    lonmin = -180 #-180
    lonmax = 180 #180
    latmin = -90 #-90
    latmax = 90 #90
    orglatmin = latmin
    stepsize = 1
    while lonmin < lonmax:
        startTime = copy.deepcopy(validTime)
        for k in range(NUMBER_OF_DATES):
            gj = {
                "_id": {
                    "loc": str(float(lonmin)) + str(float(latmin)), 
                    "validTime": {"$date": str(startTime.isoformat()) + ".000+00:00"}
                }, 
                "observation": {
                    "temperature": randint(-30, 40)
                }
            }
            startTime += datetime.timedelta(hours=6)
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