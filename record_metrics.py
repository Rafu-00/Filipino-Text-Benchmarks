import subprocess
import csv
import time

# Execute the command
def run_command_with_timeout(command, timeout_seconds):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    start_time = time.time()
    while time.time() - start_time <= timeout_seconds:
        time.sleep(2)
    process.terminate()
    return process.communicate()

timeout_seconds = 1500
command = f"timeout {timeout_seconds} sudo powermetrics --samplers gpu_power,cpu_power -i 2000 | grep -E '(E-Cluster HW active frequency|P-Cluster HW active frequency|GPU Power|CPU Power|GPU HW active frequency)'"
output, error = run_command_with_timeout(command, timeout_seconds)

# Parse the output and extract values
data = []

for line in output.decode().split('\n'):
    if line.startswith("E-Cluster HW active frequency:"):
        metric = "E-Cluster HW active frequency"
        val = line.replace("E-Cluster HW active frequency:", "").strip()
    elif line.startswith("P-Cluster HW active frequency:"):
        metric = "P-Cluster HW active frequency"
        val = line.replace("P-Cluster HW active frequency:", "").strip()
    elif line.startswith("CPU Power:"):
        metric = "CPU Power"
        val = line.replace("CPU Power:", "").strip()
    elif line.startswith("GPU Power:"):
        metric = "GPU Power"
        val = line.replace("GPU Power:", "").strip()
    elif line.startswith("GPU HW active frequency:"):
        metric = "GPU HW active frequency"
        val = line.replace("GPU HW active frequency:", "").strip()
    else:
        continue # Use continue instead of break to avoid potential infinite loop

    data.append([metric, val])

# Write the data to a CSV file
with open('electra_power_metrics.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Metric', 'Value'])
    writer.writerows(data)

print("Data saved to distilbert_power_metrics.csv")