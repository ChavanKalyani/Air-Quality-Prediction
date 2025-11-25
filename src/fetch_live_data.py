import requests
from datetime import datetime
from src.config import WAQI_TOKEN, CITY

def fetch_pm25():
    url = f"https://api.waqi.info/feed/{CITY}/?token={WAQI_TOKEN}"
    response = requests.get(url).json()

    try:
        pm25 = response["data"]["iaqi"]["pm25"]["v"]
    except:
        raise Exception("PM2.5 data unavailable from WAQI API")

    return datetime.now(), pm25
