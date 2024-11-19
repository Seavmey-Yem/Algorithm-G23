# Check Wi-Fi Speed : The tool should check the current download and upload speed of the active Wi-Fi connection. 
import speedtest
import math

def check_speed_wifi():
    st = speedtest.Speedtest()

    # Get best server based on ping
    st.get_best_server()

    # Perform download and upload speed tests
    download_speed = st.download() / 1_000  # Convert from bits to kilobits
    upload_speed = st.upload() / 1_000  # Convert from bits to kilobits

    # Print the results
    print("Download speed: ", math.ceil(download_speed), "kbps")
    print("Upload speed: ", math.ceil(upload_speed), "kbps")

# Run the function
check_speed_wifi()




