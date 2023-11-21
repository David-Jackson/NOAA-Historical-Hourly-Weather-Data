import logging
import logging.handlers
import os
import json
import glob

import requests
import pandas as pd


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "scripts/status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
logger_console_handler = logging.StreamHandler()

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger_file_handler.setFormatter(formatter)
logger_console_handler.setFormatter(formatter)

logger.addHandler(logger_file_handler)
logger.addHandler(logger_console_handler)

def get_wmo_from_csv(data):
    stations = data.drop_duplicates('STATION')
    return stations['STATION'].to_numpy()


if __name__ == "__main__":

    wmo = "723100"
    
    with open('scripts/stations.json', 'r') as f:
        stations = json.load(f)

    for filename in glob.glob('raw/*.csv'):
        logger.info(f'Processing {filename}')

        data = pd.read_csv(filename)

        wmo_list = get_wmo_from_csv(data)

        if len(wmo_list) > 1:
            logger.warning(f'Found {len(wmo_list)} Station Numbers in {filename}, using {wmo_list[0]}')

        wmo = str(wmo_list[0])[:6] # parses WMO number from STATION (i.e. 72327013897 -> 723270) 

        filtered_stations = list(filter(lambda x: x['wmo'] == wmo, stations))

        if len(filtered_stations) > 1:
            logger.warning(f'Found {len(filtered_stations)} Stations for WMO {wmo}, using {filtered_stations[0]}')

        station = filtered_stations[0]

        location_str = station['name'] + ' - ' + ', '.join(station['parents'])

        new_filename = wmo + ' - ' + location_str

        logger.info(f'Creating new File: {new_filename}')