# weather-demo

The purpose of this project is to showcase how to handle large sets of weather data in MongoDB. This involves
* How to setup a machine to work with weather files
* How to ingest weather files
* How to query weather files

As hinted in the project name, this is nothing but a demo. None of the code is production ready. Most notably
* Code for ingesting weather files isn't generic and only works for specific weather files (provided as examples)
* No performance tuning has been done
* There are many different approaches to modelling weather data, of which this demo provide one approach.

With that said, the demo can definitely serve as inspiration and as a starting point for your own explorations. Have fun!

The project is organized into folders, each showcasing a specific time series as well as query:

Type | Series | Query
--- | --- | ---
[Precipitation queries](precipitation_series/) | Generic series generated in [ingest_weather_data](ingest_weather_data)  | Show how to convert from cumulated precipitation data to precipitation in time intervals.
[Temperature queries](temperature_series/) | Generic series generated in [ingest_weather_data](ingest_weather_data)  | Show how to calculate min/max/avg from temperature data in time intervals. Also show how to calculate nearest point from a location and get a weather observation from there.
[Wind series](wind_series/) | Generic series generated in [ingest_weather_data](ingest_weather_data)  | Show how to calculate wind directions based on wind speed u/v values
