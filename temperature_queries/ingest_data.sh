#!/bin/bash
python3 create_grid.py | mongoimport --uri "mongodb+srv://cluster0.vortb.mongodb.net/weather" --username main_user --password $MDB_PSWD --drop --collection temperature_grid --jsonArray
python3 create_weather_data.py | mongoimport --uri "mongodb+srv://cluster0.vortb.mongodb.net/weather" --username main_user --password $MDB_PSWD --drop --collection temperature_data --jsonArray


#TODO: create index on precipitation_data {'_id.loc': 1}