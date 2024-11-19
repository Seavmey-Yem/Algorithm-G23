# import platform
# import psutil
# import wmi

# # Function to get RAM information
# def get_ram_info():
#     ram = psutil.virtual_memory()
#     total_ram = ram.total / (1024 ** 3)  # Convert bytes to GB
#     used_ram = ram.used / (1024 ** 3)    # Convert bytes to GB
#     free_ram = ram.available / (1024 ** 3)  # Convert bytes to GB
#     return total_ram, used_ram, free_ram

# # Function to get disk information
# def get_disk_info():
#     disk = psutil.disk_usage('/')
#     total_disk = disk.total / (1024 ** 3)  # Convert bytes to GB
#     used_disk = disk.used / (1024 ** 3)    # Convert bytes to GB
#     free_disk = disk.free / (1024 ** 3)    # Convert bytes to GB
#     return total_disk, used_disk, free_disk

# # Function to get CPU usage
# def get_cpu_usage():
#     return psutil.cpu_percent(interval=1)

# # Function to get system name
# def get_system_name():
#     return platform.node()

# # Function to get system manufacturer
# def get_system_manufacturer():
#     c = wmi.WMI()
#     for system in c.Win32_ComputerSystem():
#         return system.Manufacturer

# # Function to get system model
# def get_system_model():
#     c = wmi.WMI()
#     for system in c.Win32_ComputerSystem():
#         return system.Model

# # Function to get system type
# def get_system_type():
#     return platform.architecture()[0]

# # Function to display system resources information
# def show_resources():
#     total_ram, used_ram, free_ram = get_ram_info()
#     total_disk, used_disk, free_disk = get_disk_info()
#     cpu_usage = get_cpu_usage()
#     system_name = get_system_name()
#     system_manufacturer = get_system_manufacturer()
#     system_model = get_system_model()
#     system_type = get_system_type()
    
#     info = (f"System Name: {system_name}\n"
#             f"System Manufacturer: {system_manufacturer}\n"
#             f"System Model: {system_model}\n"
#             f"System Type: {system_type}\n"
#             f"RAM: {total_ram:.2f} GB (Used: {used_ram:.2f} GB, Free: {free_ram:.2f} GB)\n"
#             f"Disk: {total_disk:.2f} GB (Used: {used_disk:.2f} GB, Free: {free_disk:.2f} GB)\n"
#             f"CPU Usage: {cpu_usage}%")
    
#     print(info)

# if __name__ == "__main__":
#     show_resources()

# ..........................On tkinter.........................................

# import platform
# import psutil
# import wmi
# import tkinter as tk
# from tkinter import messagebox

# # Function to get RAM information
# def get_ram_info():
#     ram = psutil.virtual_memory()
#     total_ram = ram.total / (1024 ** 3)  # Convert bytes to GB
#     used_ram = ram.used / (1024 ** 3)    # Convert bytes to GB
#     free_ram = ram.available / (1024 ** 3)  # Convert bytes to GB
#     return total_ram, used_ram, free_ram

# # Function to get disk information
# def get_disk_info():
#     disk = psutil.disk_usage('/')
#     total_disk = disk.total / (1024 ** 3)  # Convert bytes to GB
#     used_disk = disk.used / (1024 ** 3)    # Convert bytes to GB
#     free_disk = disk.free / (1024 ** 3)    # Convert bytes to GB
#     return total_disk, used_disk, free_disk

# # Function to get CPU usage
# def get_cpu_usage():
#     return psutil.cpu_percent(interval=1)

# # Function to get system name
# def get_system_name():
#     return platform.node()

# # Function to get system manufacturer
# def get_system_manufacturer():
#     c = wmi.WMI()
#     for system in c.Win32_ComputerSystem():
#         return system.Manufacturer

# # Function to get system model
# def get_system_model():
#     c = wmi.WMI()
#     for system in c.Win32_ComputerSystem():
#         return system.Model

# # Function to get system type
# def get_system_type():
#     return platform.architecture()[0]

# # Function to display system resources information in a Tkinter message box
# def show_resources():
#     total_ram, used_ram, free_ram = get_ram_info()
#     total_disk, used_disk, free_disk = get_disk_info()
#     cpu_usage = get_cpu_usage()
#     system_name = get_system_name()
#     system_manufacturer = get_system_manufacturer()
#     system_model = get_system_model()
#     system_type = get_system_type()
    
#     info = (f"System Name: {system_name}\n"
#             f"System Manufacturer: {system_manufacturer}\n"
#             f"System Model: {system_model}\n"
#             f"System Type: {system_type}\n"
#             f"RAM: {total_ram:.2f} GB (Used: {used_ram:.2f} GB, Free: {free_ram:.2f} GB)\n"
#             f"Disk: {total_disk:.2f} GB (Used: {used_disk:.2f} GB, Free: {free_disk:.2f} GB)\n"
#             f"CPU Usage: {cpu_usage}%")
    
#     messagebox.showinfo("System Resources", info)

# # Create the main application window
# mywindow = tk.Tk()
# mywindow.title("Check System Resources")
# mywindow.geometry("400x400")  # Adjusted size for more info

# # Create and place the button in the window
# resource_button = tk.Button(mywindow, text="Check System Resources", command=show_resources, width=25, height=3, bg='lightgreen')
# resource_button.pack(pady=20)

# # Start the Tkinter event loop
# mywindow.mainloop()


