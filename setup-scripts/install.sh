
#remember to open IP address on Atlas

sudo apt update
sudo apt -y install python3-pip
pip3 install numpy
export PATH=$PATH:/home/ubuntu/.local/bin
sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt-get -y install gdal-bin
sudo apt-get -y install libgdal-dev
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
pip3 install pymongo
pip3 install dnspython

#fetch some sample data
wget "https://www.ncei.noaa.gov/data/climate-forecast-system/access/operational-9-month-forecast/time-series/2021/202102/20210214/2021021412/tmp2m.01.2021021412.daily.grb2" -O "tmp2m.01.2021021412.daily.grb2"

for area in oslofjord skagerrak sorlandet west_norway n-northsea troms-finnmark nordland
do
  wget "https://api.met.no/weatherapi/gribfiles/1.1/?area=$area&content=weather" -O "meps_weatherapi_$area.grb"
done

#read in the sample data TODO: move to another place
python3 read.py meps_weatherapi_oslofjord.grb TRUE
for area in skagerrak sorlandet west_norway n-northsea troms-finnmark nordland
do
  python3 read.py "meps_weatherapi_$area.grb"
done

