import logging
import logging.handlers
import os
import json

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "scripts/status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

if __name__ == "__main__":

    wmo = "723100"
    
    with open('scripts/stations.json', 'r') as f:
        stations = json.load(f)

    filtered_stations = filter(lambda x: x['wmo'] == wmo, stations)

    for x in filtered_stations:
        logger.info(f'WMO {wmo}: {json.dumps(x)}')
