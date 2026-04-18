import pandas as pd
import matplotlib.pyplot as plt

# ====== UPDATE THIS FILE PATH ======
file_path = "data/log_20260418_203250.csv"

# Load data
df = pd.read_csv(file_path)

# Convert timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], format="%H:%M:%S")

# ====== BASIC STATS ======
avg_cpu = df['cpu'].mean()
avg_gpu = df['gpu'].mean()

max_cpu = df['cpu'].max()
max_gpu = df['gpu'].max()

# ====== PRINT SUMMARY ======
print("----- Performance Summary -----")
print(f"Average CPU Usage: {avg_cpu:.2f}%")
print(f"Average GPU Usage: {avg_gpu:.2f}%")
print(f"Max CPU Usage: {max_cpu}%")
print(f"Max GPU Usage: {max_gpu}%")

# ====== BOTTLENECK DETECTION ======
if avg_cpu > avg_gpu:
    print("\nInference: Possible CPU bottleneck detected.")
else:
    print("\nInference: System appears GPU-bound.")

# ====== SPIKE DETECTION ======
cpu_spikes = df[df['cpu'] > 90]
gpu_spikes = df[df['gpu'] > 90]

print(f"\nCPU spike count (>90%): {len(cpu_spikes)}")
print(f"GPU spike count (>90%): {len(gpu_spikes)}")

# ====== PLOTTING ======
plt.figure()

plt.plot(df['timestamp'], df['cpu'], label="CPU Usage")
plt.plot(df['timestamp'], df['gpu'], label="GPU Usage")

plt.xlabel("Time")
plt.ylabel("Usage (%)")
plt.title("CPU vs GPU Usage During Gameplay")

plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Save graph
plt.savefig("outputs/performance_plot.png")

# Show graph
plt.show()