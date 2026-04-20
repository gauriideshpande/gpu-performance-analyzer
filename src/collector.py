import time
import psutil
import csv
from datetime import datetime
from pynvml import *

# Initialize GPU
nvmlInit()
handle = nvmlDeviceGetHandleByIndex(0)

def get_metrics():
    cpu_total = psutil.cpu_percent(interval=1)
    cpu_per_core = psutil.cpu_percent(percpu=True)
    gpu = nvmlDeviceGetUtilizationRates(handle).gpu

    return cpu_total, cpu_per_core, gpu

# Create output file
filename = f"data/log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "cpu_total", "gpu", "cpu_cores", "fps_estimate"])

    print(f"Logging started... Saving to {filename}")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            cpu_total, cpu_per_core, gpu = get_metrics()
            timestamp = datetime.now().strftime("%H:%M:%S")

            # Simple FPS estimation (heuristic)
            fps_estimate = max(30, 120 - int(cpu_total * 0.8))

            writer.writerow([timestamp, cpu_total, gpu, cpu_per_core, fps_estimate])
            print(f"{timestamp} | CPU: {cpu_total}% | GPU: {gpu}% | FPS~: {fps_estimate}")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nLogging stopped.")