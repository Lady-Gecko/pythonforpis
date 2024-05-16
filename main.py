import subprocess
import time

# List of scripts for each parking space
scripts = ["space1.py", "space2.py", "space3.py", "space4.py"]

# Start each script as a separate process
processes = []
for script in scripts:
    process = subprocess.Popen(["python3", script])
    processes.append(process)

try:
    # Keep the main script running to catch KeyboardInterrupt
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping all processes...")
    for process in processes:
        process.terminate()
    for process in processes:
        process.wait()
    print("All processes stopped.")
