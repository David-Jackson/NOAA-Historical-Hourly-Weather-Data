# Scripts for NOAA Historical Hourly Weather Data

The scripts here are for processing raw data from the [NOAA Local Climatological Data (LCD)](https://www.ncdc.noaa.gov/cdo-web/datatools/lcd).

## `main.py`

This script will take all files from the `raw` folder, process and filter to relevant data, and save the save the processed data to a new file in the `data` folder. This script should be run from the repo's root directory. It is also set up to be run as a Github Action, but can be run locally as well.


## `get_ashrae_meteo_stations.js`

This collects all ASHRAE stations into a JSON object that can be saved in `stations.json`. This data is used to look up station names for the `main.py` script for file naming purposes.
