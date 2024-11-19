# import os

# def restartPC():
#     os.system('shutdown /r /t 1')

# def shutdownPC():
#     os.system('shutdown /s /t 1')

# def main():
#     print("System Control Menu")
#     print("1. Restart PC")
#     print("2. Shutdown PC")
#     print("3. Exit")
    
#     while True:
#         choice = input("Enter your choice (1/2/3): ")

#         if choice == '1':
#             restartPC()
#         elif choice == '2':
#             shutdownPC()
#         elif choice == '3':
#             print("Exiting...")
#             break
#         else:
#             print("Invalid choice. Please enter 1, 2, or 3.")

# if __name__ == "__main__":
#     main()

# .................On tkinter.............

import os
import tkinter as tk

def restartPC():
    os.system('shutdown /r /t 1')

def shutdownPC():
    os.system('shutdown /s /t 1')

# Create the main application window
mywindow = tk.Tk()
mywindow.title("System Control Menu")
mywindow.geometry("400x300")

# Create and place the Restart button in the window
restart_button = tk.Button(mywindow, text="Restart PC", command=restartPC, width=25, height=3, bg='lightblue')
restart_button.pack(pady=10)

# Create and place the Shutdown button in the window
shutdown_button = tk.Button(mywindow, text="Shutdown PC", command=shutdownPC, width=25, height=3, bg='lightcoral')
shutdown_button.pack(pady=10)

# Start the Tkinter event loop
mywindow.mainloop()


