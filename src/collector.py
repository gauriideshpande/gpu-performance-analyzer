import time
import psutil
from pynvml import *

# Initialize GPU access
nvmlInit()
handle = nvmlDeviceGetHandleByIndex(0)

def get_metrics():
    cpu = psutil.cpu_percent(interval=1)
    gpu = nvmlDeviceGetUtilizationRates(handle).gpu
    return cpu, gpu

if __name__ == "__main__":
    print("Starting system monitor... (Press Ctrl+C to stop)\n")

    try:
        while True:
            cpu, gpu = get_metrics()
            print(f"CPU: {cpu}% | GPU: {gpu}%")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopped monitoring.")