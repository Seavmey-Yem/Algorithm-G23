# import platform
# import psutil
# import wmi

# def get_device_name():
#     return platform.node()

# def get_processors():
#     return platform.processor()

# def get_window_version():
#     return platform.version()

# def get_system_type():
#     return platform.architecture()[0]

# def get_ram():
#     ram = psutil.virtual_memory()
#     return f"{ram.total / (1024 ** 3):.2f} GB"

# def get_hard_disk():
#     disk = psutil.disk_usage('/')
#     return f"Total: {disk.total / (1024 ** 3):.2f} GB, Used: {disk.used / (1024 ** 3):.2f} GB, Free: {disk.free / (1024 ** 3):.2f} GB"

# def get_system_manufacturer():
#     c = wmi.WMI()
#     for system in c.Win32_ComputerSystem():
#         return system.Manufacturer

# def get_system_model():
#     c = wmi.WMI()
#     for system in c.Win32_ComputerSystem():
#         return system.Model

# def show_info():
#     device_name = get_device_name()
#     processors = get_processors()
#     win_version = get_window_version()
#     system_type = get_system_type()
#     ram = get_ram()
#     hard_disk = get_hard_disk()
#     manufacturer = get_system_manufacturer()
#     model = get_system_model()
    
#     info = (f"Device Name: {device_name}\n"
#             f"Processors: {processors}\n"
#             f"Windows Version: {win_version}\n"
#             f"System Type: {system_type}\n"
#             f"RAM: {ram}\n"
#             f"Hard Disk: {hard_disk}\n"
#             f"System Manufacturer: {manufacturer}\n"
#             f"System Model: {model}")
    
#     print(info)

# if __name__ == "__main__":
#     show_info()

# ...................On tkinter.............
import platform, psutil, wmi, tkinter as tk
from tkinter import messagebox

def show_info():
    c = wmi.WMI()
    info = (f"Device Name: {platform.node()}\n"
            f"Processors: {platform.processor()}\n"
            f"Windows Version: {platform.version()}\n"
            f"System Type: {platform.architecture()[0]}\n"
            f"RAM: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB\n"
            f"Disk: Total: {psutil.disk_usage('/').total / (1024 ** 3):.2f} GB, Used: {psutil.disk_usage('/').used / (1024 ** 3):.2f} GB, Free: {psutil.disk_usage('/').free / (1024 ** 3):.2f} GB\n"
            f"System Manufacturer: {c.Win32_ComputerSystem()[0].Manufacturer}\n"
            f"System Model: {c.Win32_ComputerSystem()[0].Model}")
    messagebox.showinfo("System Information", info)

mywindow = tk.Tk()
mywindow.title("System Information")
mywindow.geometry("400x400")
tk.Button(mywindow, text="Get System Info", command=show_info, width=25, height=3, bg='lightblue').pack(pady=20)
mywindow.mainloop()





