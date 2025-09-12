import psutil
import time
import csv
import os
import shutil

def get_resource_usage():
    """Get CPU, memory, and disk usage as percentages."""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        return cpu_percent, memory_percent, disk_percent
    except Exception as e:
        print(f"Error getting resource usage: {e}")
        return 0.0, 0.0, 0.0

def create_folders():
    """Create Logs and Archive folders if they don't exist."""
    logs_dir = "Logs"
    archive_dir = os.path.join(logs_dir, "Archive")
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(archive_dir, exist_ok=True)
    return logs_dir, archive_dir

def get_csv_filename():
    """Generate a CSV filename with timestamp, replacing invalid characters."""
    timestamp = time.ctime(time.time()).replace(":", "_").replace(" ", "_")
    return f"{timestamp}_log.csv"

def manage_logs(logs_dir, archive_dir):
    """Move oldest log file to Archive if more than 5 files exist."""
    log_files = [f for f in os.listdir(logs_dir) if f.endswith("_log.csv")]
    if len(log_files) > 5:
        # Get the oldest file based on modification time
        oldest_file = min(
            log_files,
            key=lambda f: os.path.getmtime(os.path.join(logs_dir, f))
        )
        src = os.path.join(logs_dir, oldest_file)
        dst = os.path.join(archive_dir, oldest_file)
        try:
            shutil.move(src, dst)
            print(f"Moved {oldest_file} to Archive")
        except Exception as e:
            print(f"Error moving {oldest_file} to Archive: {e}")

def monitor_and_log():
    """Monitor resource usage and log to CSV every 5 seconds."""
    logs_dir, archive_dir = create_folders()
    current_csv = None
    csv_writer = None
    start_time = time.time()
    
    while True:
        # Check if a new CSV file is needed (every 60 seconds)
        if current_csv is None or (time.time() - start_time) >= 60:
            # Close current CSV file if open
            if current_csv:
                current_csv.close()
            
            # Generate new CSV filename and open file
            csv_filename = get_csv_filename()
            csv_path = os.path.join(logs_dir, csv_filename)
            try:
                current_csv = open(csv_path, 'w', newline='')
                csv_writer = csv.writer(current_csv)
                csv_writer.writerow(['Timestamp', 'CPU%', 'Memory%', 'Disk%'])
                print(f"Created new log file: {csv_filename}")
            except Exception as e:
                print(f"Error creating CSV file {csv_filename}: {e}")
                return
            
            start_time = time.time()
        
        # Get resource usage
        cpu_percent, memory_percent, disk_percent = get_resource_usage()
        timestamp = time.ctime(time.time())
        
        # Write to CSV
        try:
            csv_writer.writerow([timestamp, cpu_percent, memory_percent, disk_percent])
            current_csv.flush()  # Ensure data is written immediately
        except Exception as e:
            print(f"Error writing to CSV: {e}")
        
        # Manage log files (archive if needed)
        manage_logs(logs_dir, archive_dir)
        
        # Wait 5 seconds
        time.sleep(5)

def main():
    """Run the monitoring and logging process."""
    try:
        monitor_and_log()
    except KeyboardInterrupt:
        print("Monitoring stopped by user")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()