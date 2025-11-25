import time
from src.logger import log_pm25

print("Starting real-time air quality monitor...")

while True:
    log_pm25()
    time.sleep(3600)  # fetch every hour
