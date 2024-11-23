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

