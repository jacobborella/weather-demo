#!/bin/bash
python3 insert_full_by_ref.py tmp2m.01.2021021412.daily.grb2 true | mongoimport --uri "mongodb+srv://main_user:$MDB_PSWD@cluster0.vortb.mongodb.net/weather" --drop --collection grb_grid --jsonArray
python3 insert_full_by_ref.py tmp2m.01.2021021412.daily.grb2 false | mongoimport --uri "mongodb+srv://main_user:$MDB_PSWD@cluster0.vortb.mongodb.net/weather" --drop --collection grb_data --jsonArray
