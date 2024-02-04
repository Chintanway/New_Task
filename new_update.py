import psutil
import speedtest
import pygetwindow as gw
import cpuinfo
import GPUtil
import platform
import requests
import json

def get_installed_software():
    return set(proc.info['name'] for proc in psutil.process_iter(['pid', 'name']))

def get_internet_speed():
    st = speedtest.Speedtest()
    return st.download() / 1_000_000, st.upload() / 1_000_000  # Convert to Mbps

def get_screen_resolution():
    active_window = gw.getActiveWindow()
    if active_window:
        return active_window.width, active_window.height
    return None

def get_cpu_info():
    cpu_info = cpuinfo.get_cpu_info()
    return cpu_info['brand_raw'], psutil.cpu_count(logical=False), psutil.cpu_count(logical=True)

def get_gpu_info():
    try:
        return GPUtil.getGPUs()[0].name
    except:
        return "N/A"

def get_ram_size():
    return psutil.virtual_memory().total / (1024 ** 3)  # Convert to GB

def get_screen_size():
    try:
        width, height = gw.getWindowsWithTitle('')[0].size
        return f"{((width * 2 + height * 2) ** 0.5):.1f} inches"
    except:
        return "N/A"

def get_network_info():
    try:
        wifi_mac_address = ':'.join(f'{int(ethernet_mac_address.split(":")[i], 16):02x}' for i in range(6) for ethernet_mac_address in psutil.net_if_addrs().get('Wi-Fi', [{}])[0].get('address', '').split(':'))
    except:
        wifi_mac_address = "N/A"

    try:
        ethernet_mac_address = ':'.join(f'{int(ethernet_mac_address.split(":")[i], 16):02x}' for i in range(6) for ethernet_mac_address in psutil.net_if_addrs().get('Ethernet', [{}])[0].get('address', '').split(':'))
    except:
        ethernet_mac_address = "N/A"

    return wifi_mac_address, ethernet_mac_address

def get_public_ip():
    try:
        return json.loads(requests.get('https://api64.ipify.org?format=json').text)['ip']
    except:
        return "N/A"

def get_windows_version():
    return platform.version()

if __name__ == "__main__":
    installed_software_list = get_installed_software()
    print("All Installed software:")
    for software in installed_software_list:
        print(f" - {software}")

    download_speed, upload_speed = get_internet_speed()
    print(f"\nInternet Speed:")
    print(f"Download Speed: {download_speed:.2f} Mbps")
    print(f"Upload Speed: {upload_speed:.2f} Mbps")

    screen_resolution = get_screen_resolution()
    print("\nScreen Resolution:")
    if screen_resolution:
        print(f"Width: {screen_resolution[0]} pixels")
        print(f"Height: {screen_resolution[1]} pixels")
    else:
        print("Unable to determine screen resolution.")

    cpu_model, num_cores, num_threads = get_cpu_info()
    print("\nCPU Model:")
    print(f"Model: {cpu_model}")
    print("\nNo of core and threads of CPU :")
    print(f"Number of Cores: {num_cores}")
    print(f"Number of Threads: {num_threads}")

    gpu_model = get_gpu_info()
    print(f"\nGPU Model: {gpu_model}")

    ram_size = get_ram_size()
    print(f"\nRAM Size: {ram_size:.2f} GB")

    screen_size = get_screen_size()
    print(f"\nScreen Size: {screen_size}")

    wifi_mac_address, ethernet_mac_address = get_network_info()
    print(f"\nWifi/Ethernet mac address:")
    print(f"Wifi mac address: {wifi_mac_address}")
    print(f"Ethernet MAC Address: {ethernet_mac_address}")

    public_ip = get_public_ip()
    print(f"\nPublic IP Address: {public_ip}")

    windows_version = get_windows_version()
    print(f"\nWindows Version: {windows_version}")
