import os
import signal

# Get the process ID of the publisher microservice
# In a real-world scenario, you'd find the PID programmatically
publisher_pid = 12345 

print(f"Injecting failure: Sending SIGKILL to process {publisher_pid} to simulate a crash...")

try:
    # SIGKILL (signal 9) is a non-trappable signal that terminates a process immediately
    os.kill(publisher_pid, signal.SIGKILL)
    print("Microservice crash initiated.")
except ProcessLookupError:
    print(f"Process {publisher_pid} not found. The service may have already terminated.")
except Exception as e:
    print(f"An error occurred: {e}")