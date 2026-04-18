import time
import psutil
import csv
from datetime import datetime
from pynvml import *

# Initialize GPU
nvmlInit()
handle = nvmlDeviceGetHandleByIndex(0)

def get_metrics():
    cpu = psutil.cpu_percent(interval=1)
    gpu = nvmlDeviceGetUtilizationRates(handle).gpu
    return cpu, gpu

# Create output file
filename = f"data/log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "cpu", "gpu"])

    print(f"Logging started... Saving to {filename}")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            cpu, gpu = get_metrics()
            timestamp = datetime.now().strftime("%H:%M:%S")

            writer.writerow([timestamp, cpu, gpu])
            print(f"{timestamp} | CPU: {cpu}% | GPU: {gpu}%")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nLogging stopped.")