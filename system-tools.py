import tkinter as tk
from tkinter import ttk
import psutil
from datetime import datetime, timedelta
import socket
import platform
import wmi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import ctypes
from tkinter import messagebox  # Import messagebox
import subprocess
import speedtest
import pandas as pd
import os
from openpyxl import load_workbook

def get_powershell_data(command):
    
    # Helper function to run PowerShell commands and retrieve output.   
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        return result.stdout.strip() or "Unknown"
    except Exception as e:
        print(f"Error running PowerShell command: {e}")
        return "Unknown"

def get_username():
    return os.getlogin()

def get_memory():
    virtual_memory = psutil.virtual_memory()
    total_ram = int(virtual_memory.total / (1024 ** 3))
    return f"{total_ram}GB"

def get_harddisk():
    total_space = sum(psutil.disk_usage(part.mountpoint).total for part in psutil.disk_partitions())  # Total bytes
    return f"{int(total_space / (1024 ** 3))}GB"  # Convert to GB

def get_system_info(n):
    
    # Collect detailed system information matching the table structure.
    try:
        processor_info = os.popen("wmic cpu get name").read().strip()
        specification = f"{processor_info}, {get_memory()}, {get_harddisk()}"
        username = get_username()
        asset_tag = socket.gethostname()
        serial_number = get_powershell_data("(Get-WmiObject -Class Win32_BIOS).SerialNumber")
        system_model = get_powershell_data("(Get-WmiObject -Class Win32_ComputerSystem).Model")
        system_manufacturer = get_powershell_data("(Get-WmiObject -Class Win32_ComputerSystem).Manufacturer")
        remark = "Optional"

        return {
            "N": n,
            "Specification": specification,
            "Username (Hostname)": username,
            "Serial number": serial_number,
            "System Model": system_model,
            "System Manufacturer": system_manufacturer,
            "Asset Tag": asset_tag,
            "Remark": remark
        }
    except Exception as e:
        print(f"Error retrieving system information: {e}")
        return None

def save_system_info_to_excel(output_file="system_info.xlsx", num_entries=1):
    
    # Save system information to an Excel file, appending data if the file already exists.
    system_data = []
    for n in range(1, num_entries + 1):
        info = get_system_info(n)
        if info:
            system_data.append(info)

    # Convert new data to DataFrame
    new_data = pd.DataFrame(system_data)

    # Check if the file exists
    if os.path.exists(output_file):
        # Load existing data
        existing_data = pd.read_excel(output_file, sheet_name="System Info")
        # Combine new and existing data
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        # If file doesn't exist, the new data is the combined data
        combined_data = new_data

    # Write the combined data to Excel
    with pd.ExcelWriter(output_file, engine="openpyxl", mode="w") as writer:
        combined_data.to_excel(writer, index=False, sheet_name="System Info")

        # Adjust column widths
        worksheet = writer.sheets["System Info"]
        for col in worksheet.columns:
            max_length = 0
            col_letter = col[0].column_letter  # Get column letter
            for cell in col:
                try:  # Avoid issues with empty cells
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            adjusted_width = max_length + 2
            worksheet.column_dimensions[col_letter].width = adjusted_width

    print(f"System information saved to {output_file}")

if __name__ == "__main__":
    # Generate system information for the computer
    save_system_info_to_excel(output_file="system_info.xlsx", num_entries=1)

def check_speed_wifi():
    st = speedtest.Speedtest()
    st.get_best_server()  # Find the best server based on ping
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    ping = st.results.ping  # Get the ping in ms

    return f"Download: {download_speed:.2f} Mbps\nUpload: {upload_speed:.2f} Mbps\nPing: {ping} ms"
def get_wifi_passwords():
    # Retrieve and display Wi-Fi passwords for networks the PC has connected to before.
    command = "netsh wlan show profiles"
    try:
        profiles = subprocess.check_output(command, shell=True).decode("utf-8", errors="ignore")
        profiles = [i.split(":")[1][1:-1] for i in profiles.split("\n") if "All User Profile" in i]
        wifi_passwords = {}
        
        for profile in profiles:
            try:
                command = f'netsh wlan show profile name="{profile}" key=clear'
                profile_info = subprocess.check_output(command, shell=True).decode("utf-8", errors="ignore")
                password_line = [i for i in profile_info.split("\n") if "Key Content" in i]

                if password_line:
                    password = password_line[0].split(":")[1][1:-1]
                    wifi_passwords[profile] = password
                else:
                    wifi_passwords[profile] = "None"
            except subprocess.CalledProcessError:
                wifi_passwords[profile] = "Error retrieving password"
        return wifi_passwords
    
    except subprocess.CalledProcessError:
        return None

if __name__ == "__main__":
    # Print Wi-Fi passwords
    print("Wi-Fi Passwords:\n")
    wifi_passwords = get_wifi_passwords()
    if wifi_passwords:
        for profile, password in wifi_passwords.items():
            print(f"{profile}: {password}")
    else:
        print("Could not retrieve Wi-Fi profiles.")

    print("\nWi-Fi Speed Test:\n")
    # print(check_speed_wifi())

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
    
    return temp_files_deleted

def clean_recycle_bin():
    # Empty the Recycle Bin.
    try:
        # SHEmptyRecycleBin function from Windows Shell32.dll
        SHEmptyRecycleBin = ctypes.windll.shell32.SHEmptyRecycleBinW
        # Arguments: None, None, and Flags (0x00000001 for no confirmation dialog)
        SHEmptyRecycleBin(None, None, 0x00000001)
        return True
    except Exception as e:
        print(f"Failed to empty Recycle Bin: {e}")
        return False
print("Cleaning temporary files and Recycle Bin...")
remove_temp_files()
clean_recycle_bin()
print("Cleanup completed.")

def get_os_details():
    # Get basic OS details using platform module
    os_name = platform.system()
    os_release = platform.release()
    os_version = platform.version()

    print(f"Operating System: {os_name}")
    print(f"OS Release: {os_release}")
    print(f"OS Version: {os_version}")
    
    # Get Windows Edition (works only on Windows)
    if os_name == "Windows":
        try:
            # Use PowerShell to get the Windows edition
            output = subprocess.check_output(
                ['powershell', '-Command', "(Get-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion').ProductName"],
                text=True
            )
            print(f"Windows Edition: {output.strip()}")
        except Exception as e:
            print(f"An error occurred while retrieving Windows edition: {e}")

if __name__ == "__main__":
    get_os_details()
    
def get_additional_system_info():
    # Retrieve additional system information.
    battery = psutil.sensors_battery()
    if battery:
        battery_status = f"{battery.percent}% {'(Charging)' if battery.power_plugged else '(Not Charging)'}"
    else:
        battery_status = "Battery information not available."

    process_count = len(psutil.pids())

    boot_time = datetime.fromtimestamp(psutil.boot_time())
    current_time = datetime.now()
    uptime = current_time - boot_time
    uptime_formatted = str(timedelta(seconds=int(uptime.total_seconds())))
    
     # Display the information
    print("\nAdditional System Information:")
    print(f"Battery Status: {battery_status}")
    print(f"Number of Running Processes: {process_count}")
    print(f"System Uptime: {uptime_formatted} (since {boot_time.strftime('%Y-%m-%d %H:%M:%S')})")

    return (
        f"Battery Status: {battery_status}\n"
        f"Number of Running Processes: {process_count}\n"
        f"System Uptime: {uptime_formatted} (since {boot_time.strftime('%Y-%m-%d %H:%M:%S')})"
    )

def create_gui():
    root = tk.Tk()
    root.title("Task Manager")
    root.geometry("800x600")

    # Tabs
    tab_control = ttk.Notebook(root)
    tab_info = ttk.Frame(tab_control)
    tab_resources = ttk.Frame(tab_control)
    tab_actions = ttk.Frame(tab_control)
    tab_additional_info = ttk.Frame(tab_control)
    tab_cleanup = ttk.Frame(tab_control)
    tab_wifi = ttk.Frame(tab_control)

    tab_control.add(tab_info, text="System Info")
    tab_control.add(tab_resources, text="Resource Usage")
    tab_control.add(tab_actions, text="Actions")
    tab_control.add(tab_additional_info, text="Additional Info")
    tab_control.pack(expand=1, fill="both")
    tab_control.add(tab_cleanup, text="Cleanup Tools")
    tab_control.add(tab_wifi, text="Wi-Fi Tools")  # Add Wi-Fi Tools tab

    # Tab 1: System Info
    info_text = tk.Text(tab_info, wrap="word", font=("Arial", 12), bg="#f0f0f0", fg="#333")
    info_text.pack(expand=1, fill="both", padx=10, pady=10)
    def refresh_info():
        info = (
            f"Device Name: {platform.node()}\n"
            f"IP Address: {socket.gethostbyname(socket.gethostname())}\n"  
            f"Processors: {platform.processor()}\n"
            f"Windows Version: {platform.version()}\n"
            f"Type: {platform.architecture()[0]}\n"
            f"RAM: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB\n"
            f"Disk: {psutil.disk_usage('/').total / (1024 ** 3):.2f} GB\n"
        )
        info_text.delete("1.0", tk.END)
        info_text.insert(tk.END, info)
        print("\nSystem Information:")
        print(info)
        print(get_os_details())
    refresh_info_button = tk.Button(tab_info, text="Refresh Info", command=refresh_info)
    refresh_info_button.pack(pady=10)
    
    # Tab 2: Graphical Resource Usage
    def update_graph(frame):
        # Get current resource usage
        cpu_percent = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        # Update Pie Charts
        ax_cpu.clear()
        ax_cpu.pie(
            [cpu_percent, 100 - cpu_percent],
            labels=['Used (%)', 'Free (%)'],
            autopct='%1.1f%%',
            colors=['#ff9999', '#99ff99'],
            startangle=90,
        )
        ax_cpu.set_title("CPU Usage")

        ax_ram.clear()
        ax_ram.pie(
            [ram.used, ram.available],
            labels=['Used (GB)', 'Free (GB)'],
            autopct='%1.1f%%',
            colors=['#66b3ff', '#ffcc99'],
            startangle=90,
        )
        ax_ram.set_title("RAM Usage")

        ax_disk.clear()
        ax_disk.pie(
            [disk.used, disk.free],
            labels=['Used (GB)', 'Free (GB)'],
            autopct='%1.1f%%',
            colors=['#ffb3e6', '#c2c2f0'],
            startangle=90,
        )
        ax_disk.set_title("Disk Usage")

    # Create Matplotlib Figures
    fig, (ax_cpu, ax_ram, ax_disk) = plt.subplots(1, 3, figsize=(10, 4))
    fig.tight_layout()

    # Embed Matplotlib Figures in Tkinter
    canvas = FigureCanvasTkAgg(fig, tab_resources)
    canvas.get_tk_widget().pack(expand=True, fill="both")

    # Animate the Graphs
    ani = animation.FuncAnimation(fig, update_graph, interval=1000)
     # Print Functions (added without changing your existing code)
    def print_cpu_usage():
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"CPU Usage:")
        print(f"  Used: {cpu_percent}%")
        print(f"  Free: {100 - cpu_percent}%")

    def print_ram_usage():
        ram = psutil.virtual_memory()
        print(f"RAM Usage:")
        print(f"  Used: {ram.used / (1024 ** 3):.2f} GB")
        print(f"  Free: {ram.available / (1024 ** 3):.2f} GB")

    def print_disk_usage():
        disk = psutil.disk_usage('/')
        print(f"Disk Usage:")
        print(f"  Used: {disk.used / (1024 ** 3):.2f} GB")
        print(f"  Free: {disk.free / (1024 ** 3):.2f} GB")

# Example of using the print functions (you can remove this part)
    if __name__ == "__main__":
        print("\nSystem Resource:")
        print_cpu_usage()
        print_ram_usage()
        print_disk_usage()
    
    # Tab 3: Actions
    def restart_system():
        os.system("shutdown /r /t 1")

    def shutdown_system():
        os.system("shutdown /s /t 1")

    restart_button = tk.Button(tab_actions, text="Restart", command=restart_system, bg="orange", fg="#fff", font=("Arial", 14))
    restart_button.pack(pady=20, ipadx=20)

    shutdown_button = tk.Button(tab_actions, text="Shutdown", command=shutdown_system, bg="#f00", fg="#fff", font=("Arial", 14))
    shutdown_button.pack(pady=20, ipadx=20)

    # Tab 4: Additional Info
    additional_info_text = tk.Text(tab_additional_info, wrap="word", font=("Arial", 12), bg="#f0f0f0", fg="#333")
    additional_info_text.pack(expand=1, fill="both", padx=10, pady=10)

    def refresh_additional_info():
        additional_info = get_additional_system_info()
        additional_info_text.delete("1.0", tk.END)
        additional_info_text.insert(tk.END, additional_info)

    refresh_additional_info_button = tk.Button(tab_additional_info, text="Refresh Info", command=refresh_additional_info)
    refresh_additional_info_button.pack(pady=10)

    # Initialize with current info
    refresh_info()
    refresh_additional_info()

     # Tab 5: Cleanup Tools
    def perform_temp_cleanup():
        deleted_files = remove_temp_files()
        messagebox.showinfo("Cleanup Complete", f"Temporary files deleted: {deleted_files}")

    def perform_recycle_bin_cleanup():
        success = clean_recycle_bin()
        if success:
            messagebox.showinfo("Cleanup Complete", "Recycle Bin emptied successfully!")
        else:
            messagebox.showerror("Error", "Failed to empty Recycle Bin.")

    cleanup_label = tk.Label(tab_cleanup, text="Cleanup Tools", font=("Arial", 14, "bold"))
    cleanup_label.pack(pady=10)

    temp_cleanup_button = tk.Button(
        tab_cleanup, text="Delete Temporary Files", command=perform_temp_cleanup, bg="#4CAF50", fg="white", font=("Arial", 12)
    )
    temp_cleanup_button.pack(pady=10, ipadx=20)

    recycle_bin_cleanup_button = tk.Button(
        tab_cleanup, text="Empty Recycle Bin", command=perform_recycle_bin_cleanup, bg="#f44336", fg="white", font=("Arial", 12)
    )
    recycle_bin_cleanup_button.pack(pady=10, ipadx=20)

    # Tab 6: Wi-Fi Tools
    wifi_label = tk.Label(tab_wifi, text="Wi-Fi Tools", font=("Arial", 14, "bold"))
    wifi_label.pack(pady=10)

    # Speed Test
    def speed_test_action():
        result = check_speed_wifi()
        messagebox.showinfo("Wi-Fi Speed Test", result)

    speed_test_button = tk.Button(
        tab_wifi, text="Check Wi-Fi Speed", command=speed_test_action, bg="#4CAF50", fg="white", font=("Arial", 12)
    )
    speed_test_button.pack(pady=10, ipadx=20)
   
    # Wi-Fi Passwords
    def show_wifi_passwords():
        passwords = get_wifi_passwords()
        if passwords:
            password_info = "\n".join([f"{network}: {password}" for network, password in passwords.items()])
        else:
            password_info = "No saved Wi-Fi profiles found or error retrieving passwords."
        messagebox.showinfo("Saved Wi-Fi Passwords", password_info)

    wifi_password_button = tk.Button(
        tab_wifi, text="Show Wi-Fi Passwords", command=show_wifi_passwords, bg="#f44336", fg="white", font=("Arial", 12)
    )
    wifi_password_button.pack(pady=10, ipadx=20) 
    root.mainloop()
    
# Run the application
if __name__ == "__main__":
    create_gui()
