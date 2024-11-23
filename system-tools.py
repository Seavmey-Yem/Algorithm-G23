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
# Check Wi-Fi Speed : The tool should check the current download and upload speed of the active Wi-Fi connection. 
import speedtest
import subprocess
def check_speed_wifi():
    st = speedtest.Speedtest()

    # Get best server based on ping
    st.get_best_server()

    # Perform download and upload speed tests
    download_speed = st.download() / 1_000  # Convert from bits to kilobits
    upload_speed = st.upload() / 1_000  # Convert from bits to kilobits

    # Print the results
    print("Download speed: ",download_speed, "kbps")
    print("Upload speed: ",upload_speed, "kbps")

# Run the function
check_speed_wifi()


#Show Wi-Fi Passwords: The tool should retrieve and display Wi-Fi passwords for networks the PC has connected to before.

def get_wifi_passwords():
    # Get the list of saved Wi-Fi profiles
    command = "netsh wlan show profiles"
    profiles = subprocess.check_output(command, shell=True).decode("utf-8", errors="ignore")
    # Split the profiles output into individual lines
    profiles = [i.split(":")[1][1:-1] for i in profiles.split("\n") if "All User Profile" in i]
    # Loop through each profile and try to retrieve the password
    wifi_passwords = {}
    for profile in profiles:
        try:
            # Get the details of each profile, including the password
            command = f'netsh wlan show profile name="{profile}" key=clear'
            profile_info = subprocess.check_output(command, shell=True).decode("utf-8", errors="ignore")
            # Extract the Wi-Fi password from the profile info
            password_line = [i for i in profile_info.split("\n") if "Key Content" in i]
            if password_line:
                password = password_line[0].split(":")[1][1:-1]
                wifi_passwords[profile] = password
            else:
                wifi_passwords[profile] = "None password"
        except subprocess.CalledProcessError:
            wifi_passwords[profile] = "Error retrieving password"
    # Display the Wi-Fi passwords
    if wifi_passwords:
        for network, password in wifi_passwords.items():
            print("Network: ",network,"\n""Password: ",password,"\n")
    else:
        print("No saved Wi-Fi profiles found.")
# Run the function
get_wifi_passwords()
import os
import socket
import platform
import psutil
import wmi

def restart():
    os.system('shutdown /r /t 1')

def shutdown():
    os.system('shutdown /s /t 1')

def show_resources():
    c = wmi.WMI()
    system_info = c.Win32_ComputerSystem()[0]
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    info = (
        f"System Name: {platform.node()}\n"
        f"Manufacturer: {system_info.Manufacturer}\n"
        f"Model: {system_info.Model}\n"
        f"Type: {platform.architecture()[0]}\n"
        f"RAM: {ram.total / (1024 ** 3):.2f} GB (Used: {ram.used / (1024 ** 3):.2f} GB, Free: {ram.available / (1024 ** 3):.2f} GB)\n"
        f"Disk: {disk.total / (1024 ** 3):.2f} GB (Used: {disk.used / (1024 ** 3):.2f} GB, Free: {disk.free / (1024 ** 3):.2f} GB)\n"
        f"CPU Usage: {psutil.cpu_percent(interval=1)}%"
    )
    print(info)

def show_info():
    c = wmi.WMI()
    system_info = c.Win32_ComputerSystem()[0]
    info = (
        f"Device Name: {platform.node()}\n"
        f"IP Address: {socket.gethostbyname(socket.gethostname())}\n"
        f"Processors: {platform.processor()}\n"
        f"Windows Version: {platform.version()}\n"
        f"Type: {platform.architecture()[0]}\n"
        f"RAM: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB\n"
        f"Disk: {psutil.disk_usage('/').total / (1024 ** 3):.2f} GB (Used: {psutil.disk_usage('/').used / (1024 ** 3):.2f} GB, Free: {psutil.disk_usage('/').free / (1024 ** 3):.2f} GB)\n"
        f"Manufacturer: {system_info.Manufacturer}\n"
        f"Model: {system_info.Model}"
    )
    print(info)

def main():
    print("System Resources:\n")
    show_resources()
    print("\nSystem Information:\n")
    show_info()

    while True:
        print("\nChoose an action:")
        print("1. Restart")
        print("2. Shutdown")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            restart()
        elif choice == '2':
            shutdown()
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()

