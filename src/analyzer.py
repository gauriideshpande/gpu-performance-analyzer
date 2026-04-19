import pandas as pd
import matplotlib.pyplot as plt

file_path = "data/log_20260418_203250.csv"

# Load data
df = pd.read_csv(file_path)
df['timestamp'] = pd.to_datetime(df['timestamp'], format="%H:%M:%S")

# ====== BASIC STATS ======
avg_cpu = df['cpu'].mean()
avg_gpu = df['gpu'].mean()

max_cpu = df['cpu'].max()
max_gpu = df['gpu'].max()

print("----- Performance Summary -----")
print(f"Average CPU Usage: {avg_cpu:.2f}%")
print(f"Average GPU Usage: {avg_gpu:.2f}%")
print(f"Max CPU Usage: {max_cpu}%")
print(f"Max GPU Usage: {max_gpu}%")

# ====== BOTTLENECK DETECTION ======
cpu_bottleneck = df[(df['cpu'] > 90) & (df['gpu'] < 50)]
gpu_bottleneck = df[(df['gpu'] > 90) & (df['cpu'] < 70)]

print("\n----- Bottleneck Detection -----")
print(f"CPU Bottleneck moments: {len(cpu_bottleneck)}")
print(f"GPU Bottleneck moments: {len(gpu_bottleneck)}")

total_points = len(df)

cpu_ratio = (len(cpu_bottleneck) / total_points) * 100
gpu_ratio = (len(gpu_bottleneck) / total_points) * 100

print(f"\nCPU Bottleneck %: {cpu_ratio:.2f}%")
print(f"GPU Bottleneck %: {gpu_ratio:.2f}%")

# ====== IDLE DETECTION ======
idle = df[(df['cpu'] < 20) & (df['gpu'] < 20)]
print(f"Idle moments: {len(idle)}")

# ====== INTERPRETATION ======
if len(cpu_bottleneck) > len(gpu_bottleneck):
    print("\nInference: System is primarily CPU-bound.")
elif len(gpu_bottleneck) > len(cpu_bottleneck):
    print("\nInference: System is primarily GPU-bound.")
else:
    print("\nInference: Mixed workload.")

# ====== PLOTTING ======
plt.figure()

# Main lines
plt.plot(df['timestamp'], df['cpu'], label="CPU Usage")
plt.plot(df['timestamp'], df['gpu'], label="GPU Usage")

# Highlight CPU bottlenecks
plt.scatter(cpu_bottleneck['timestamp'], cpu_bottleneck['cpu'],
            label="CPU Bottleneck", marker='o')

# Highlight GPU bottlenecks
plt.scatter(gpu_bottleneck['timestamp'], gpu_bottleneck['gpu'],
            label="GPU Bottleneck", marker='x')

# Threshold line
plt.axhline(y=90, linestyle='--', label='CPU Threshold (90%)')

plt.xlabel("Time")
plt.ylabel("Usage (%)")
plt.title("CPU vs GPU Usage with Bottleneck Detection")

plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("outputs/performance_with_detection.png")

plt.show()