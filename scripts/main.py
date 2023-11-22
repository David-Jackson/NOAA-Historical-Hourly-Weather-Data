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

def filter_data(data):
    
    old_len = len(data.index)

    # Filter the data accordingly.
    data = data[data['REPORT_TYPE'] == 'FM-15']

    data = data[data['HourlyDryBulbTemperature'] != '']
    data = data[data['HourlyDewPointTemperature'] != '']

    # remove wierd values that end with "s" for some reason
    data = data[pd.to_numeric(data['HourlyDryBulbTemperature'], errors='coerce').notnull()]
    data = data[pd.to_numeric(data['HourlyDewPointTemperature'], errors='coerce').notnull()]

    data = data[
        [
            # 'STATION',
            'DATE',
            # 'REPORT_TYPE',
            'HourlyDewPointTemperature',
            'HourlyDryBulbTemperature', 
            'HourlyRelativeHumidity'
        ]
    ]
    new_len = len(data.index)

    print(str(old_len), "->", str(new_len))

    return data

def get_wmo_from_csv(data):
    stations = data.drop_duplicates('STATION')
    return stations['STATION'].to_numpy()

def get_date_range_from_csv(df):
    # Convert the 'DATE' column to datetime objects
    df['DATE'] = pd.to_datetime(df['DATE'])

    # Find the earliest and latest timestamps
    earliest_timestamp = df['DATE'].min()
    latest_timestamp = df['DATE'].max()
    
    # Extract the earliest and latest years
    earliest_year = earliest_timestamp.year
    latest_year = latest_timestamp.year

    # Calculate the number of years covered
    years_covered = (latest_timestamp - earliest_timestamp).days / 365.25

    return f"{years_covered:.0f}yr ({earliest_year}-{latest_year})"

if __name__ == "__main__":

    wmo = "723100"
    
    with open('scripts/stations.json', 'r') as f:
        stations = json.load(f)

    for filename in glob.glob('raw/*.csv'):
        logger.info(f'Processing {filename}')

        data = pd.read_csv(filename)

        wmo_list = get_wmo_from_csv(data)

        date_range_str = get_date_range_from_csv(data)

        data = filter_data(data)

        if len(wmo_list) > 1:
            logger.warning(f'Found {len(wmo_list)} Station Numbers in {filename}, using {wmo_list[0]}')

        wmo = str(wmo_list[0])[:6] # parses WMO number from STATION (i.e. 72327013897 -> 723270) 

        filtered_stations = list(filter(lambda x: x['wmo'] == wmo, stations))

        if len(filtered_stations) > 1:
            logger.warning(f'Found {len(filtered_stations)} Stations for WMO {wmo}, using {filtered_stations[0]}')

        station = filtered_stations[0]

        location_str = ', '.join([station['name']] + station['parents'])

        new_filename = f'{wmo} - {date_range_str} - {location_str}'

        logger.info(f'Creating new File: {new_filename}')

        data.to_csv(f'data/{new_filename}.csv', index=False)

        if os.path.exists(filename):
            os.remove(filename)
            print(f"The file {filename} has been deleted.")
        