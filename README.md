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
 [Precipitation queries](precipitation_series/) | Precipitation data with no bucketing,  | Show how to convert from cumulated precipitation data to precipitation in time intervals.
