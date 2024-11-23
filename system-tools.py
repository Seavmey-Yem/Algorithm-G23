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

