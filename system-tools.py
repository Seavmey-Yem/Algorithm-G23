import psutil
from datetime import datetime, timedelta

def additional_system_info():
    """Retrieve and display additional system information."""
    # Battery status
    battery = psutil.sensors_battery()
    if battery:
        battery_status = f"{battery.percent}% {'(Charging)' if battery.power_plugged else '(Not Charging)'}"
    else:
        battery_status = "Battery information not available."

    # Number of running processes
    process_count = len(psutil.pids())

    # System uptime
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    current_time = datetime.now()
    uptime = current_time - boot_time

    # Format uptime
    uptime_formatted = str(timedelta(seconds=int(uptime.total_seconds())))

    # Display the information
    print("\nAdditional System Information:")
    print(f"Battery Status: {battery_status}")
    print(f"Number of Running Processes: {process_count}")
    print(f"System Uptime: {uptime_formatted} (since {boot_time.strftime('%Y-%m-%d %H:%M:%S')})")

# Run the function
if __name__ == "__main__":
    additional_system_info()


import os
import shutil
import ctypes
from pathlib import Path

def remove_temp_files():
    """Delete temporary files from the system's TEMP directory."""
    temp_dirs = [os.getenv('TEMP'), os.getenv('TMP')]
    temp_files_deleted = 0

    for temp_dir in temp_dirs:
        if temp_dir and os.path.exists(temp_dir):
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                        temp_files_deleted += 1
                    except Exception as e:
                        print(f"Failed to delete {file_path}: {e}")
    
    print(f"Temporary files deleted: {temp_files_deleted}")

def clean_recycle_bin():
    """Empty the Recycle Bin."""
    try:
        # SHEmptyRecycleBin function from Windows Shell32.dll
        SHEmptyRecycleBin = ctypes.windll.shell32.SHEmptyRecycleBinW
        # Arguments: None, None, and Flags (0x00000001 for no confirmation dialog)
        SHEmptyRecycleBin(None, None, 0x00000001)
        print("Recycle Bin emptied successfully.")
    except Exception as e:
        print(f"Failed to empty Recycle Bin: {e}")

# Run the functions
if __name__ == "__main__":
    print("Cleaning temporary files and Recycle Bin...")
    remove_temp_files()
    clean_recycle_bin()
    print("Cleanup completed.")
