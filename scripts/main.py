import logging
import logging.handlers
import os

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
    
    r = requests.post(
        'http://ashrae-meteo.info/v2.0/request_meteo_parametres.php', 
        json = {
            "wmo": wmo, 
            "ashrae_version": "2021", 
            "si_ip": "IP"
        },
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "pragma": "no-cache",
            "Referer": "http://ashrae-meteo.info/v2.0/",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
    )
    
    logger.info(f'WMO {wmo}: Request Status Code: {r.status_code}')
    
    if r.status_code == 200:
        data = r.json()
        place = data["place"]
        logger.info(f'WMO {wmo}: {place}')
