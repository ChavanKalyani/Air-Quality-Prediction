import time
import subprocess
import datetime

def run_command(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True)

def daily_loop():
    print("=== Daily Automation Started ===")
    
    while True:
        print("\n--- Running Daily Forecast & Plot Update ---")
        now = datetime.datetime.now()
        print(f"Time: {now}")
        run_command("python -m src.forecast")
        run_command("python -m scripts.plot_forecast_vs_actual")

        print("✓ Daily update complete!")
        print("Sleeping for 24 hours...")
        time.sleep(86400)

if __name__ == "__main__":
    daily_loop()

