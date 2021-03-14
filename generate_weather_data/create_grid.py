import decimal

def gridder():
    pos = 1
    lonmin = -180 #-180
    lonmax = 180 #180
    latmin = -90 #-90
    latmax = 90 #90
    orglatmin = latmin
    stepsize = 1
    while lonmin < lonmax:
        gj = {
        "_id": str(float(lonmin)) + str(float(latmin)),
        "geometry": {
            "type": "Point",
            "coordinates": [float(lonmin), float(latmin)]
        }
        }
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