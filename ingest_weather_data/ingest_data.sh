#!/bin/bash
python3 create_grid.py | mongoimport --uri "mongodb+srv://cluster0.vortb.mongodb.net/weather" --username main_user --password $MDB_PSWD --drop --collection weather_grid --jsonArray
python3 create_weather_data.py | mongoimport --uri "mongodb+srv://cluster0.vortb.mongodb.net/weather" --username main_user --password $MDB_PSWD --drop --collection weather_data --jsonArray

cat add_metadata.mdb | mongo "mongodb+srv://cluster0.vortb.mongodb.net/weather" --username main_user --password $MDB_PSWD
#TODO: create index on precipitation_data {'_id.loc': 1}