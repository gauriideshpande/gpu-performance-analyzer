# GPU Performance Analyzer

A lightweight tool to monitor and analyze CPU and GPU usage during real-world workloads like gaming.

## Motivation
While playing games, I noticed performance inconsistencies and wanted to understand how system resources behave under load.

This project explores CPU vs GPU utilization and identifies performance bottlenecks using real gameplay data.

## Features
- Real-time CPU and GPU monitoring
- Logging performance data to CSV
- Visualization of CPU vs GPU usage
- Automatic bottleneck detection
- Spike analysis

## Key Findings
Using gameplay data from Fortnite:

- CPU bottlenecks detected: 33 instances
- GPU bottlenecks detected: 0
- CPU usage frequently spiked to 100%
- GPU usage remained between 20–50%

### Insight
Even in GPU-intensive workloads, CPU can become the limiting factor, leading to underutilized GPU capacity.

## Tech Stack
- Python
- psutil
- pynvml
- pandas
- matplotlib

## Future Improvements
- Per-core CPU analysis
- FPS integration
- Real-time dashboard
- Multi-game comparison

## How to Run
```bash
pip install -r requirements.txt
python src/collector.py
python src/analyzer.py