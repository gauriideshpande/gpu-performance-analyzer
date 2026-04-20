import pandas as pd
import matplotlib.pyplot as plt
import ast

file_path = "data/FinalLogs.csv"

df = pd.read_csv(file_path)
df['timestamp'] = pd.to_datetime(df['timestamp'], format="%H:%M:%S")

# Fix column names
cpu_col = 'cpu_total' if 'cpu_total' in df.columns else 'cpu'

# Handle missing fps_estimate
if 'fps_estimate' not in df.columns:
    print("fps_estimate column not found. Skipping FPS analysis.")
    df['fps_estimate'] = 60

# Safe parsing cpu_cores
def safe_parse(x):
    try:
        return ast.literal_eval(x)
    except:
        return [0]

df['cpu_cores'] = df['cpu_cores'].apply(safe_parse)
df['max_core'] = df['cpu_cores'].apply(max)

# Stats
avg_cpu = df[cpu_col].mean()
avg_gpu = df['gpu'].mean()

max_cpu = df[cpu_col].max()
max_gpu = df['gpu'].max()

print("----- Performance Summary -----")
print(f"Average CPU Usage: {avg_cpu:.2f}%")
print(f"Average GPU Usage: {avg_gpu:.2f}%")

# Bottlenecks
cpu_bottleneck = df[(df[cpu_col] > 90) & (df['gpu'] < 50)]
gpu_bottleneck = df[(df['gpu'] > 90) & (df[cpu_col] < 70)]

print("\n----- Bottleneck Detection -----")
print(f"CPU Bottleneck moments: {len(cpu_bottleneck)}")
print(f"GPU Bottleneck moments: {len(gpu_bottleneck)}")

# Single-core
single_core_bottleneck = df[df['max_core'] > 90]
print(f"\nSingle-core bottleneck moments: {len(single_core_bottleneck)}")

# FPS
fps_drops = df[df['fps_estimate'] < 50]
print(f"FPS drop moments: {len(fps_drops)}")

correlated = df[(df['max_core'] > 90) & (df['fps_estimate'] < 50)]
print(f"CPU spike + FPS drop correlation: {len(correlated)}")

# Plot
plt.figure()
plt.plot(df['timestamp'], df[cpu_col], label="CPU Usage")
plt.plot(df['timestamp'], df['gpu'], label="GPU Usage")

plt.scatter(cpu_bottleneck['timestamp'], cpu_bottleneck[cpu_col], label="CPU Bottleneck")
plt.axhline(y=90, linestyle='--', label='CPU Threshold')

plt.legend()
plt.tight_layout()
plt.show()