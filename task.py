
import psutil
import speedtest
import pygetwindow as gw
import cpuinfo
import GPUtil
import platform
import requests
import json

def get_installed_software():
    installed_software = []
    for proc in psutil.process_iter(['pid', 'name']):
        installed_software.append(proc.info['name'])
    return set(installed_software)


def get_internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    return download_speed, upload_speed


def get_screen_resolution():
    active_window = gw.getActiveWindow()
    screen_resolution = None
    if active_window is not None:
        screen_resolution = active_window.width, active_window.height
    return screen_resolution


def get_cpu_info():
    cpu_info = cpuinfo.get_cpu_info()
    cpu_model = cpu_info['brand_raw']
    num_cores = psutil.cpu_count(logical=False)
    num_threads = psutil.cpu_count(logical=True)
    return cpu_model, num_cores, num_threads


def get_gpu_info():
    try:
        gpu = GPUtil.getGPUs()[0]
        gpu_model = gpu.name
    except:
        gpu_model = "N/A"
    return gpu_model


def get_ram_size():
    ram_size = psutil.virtual_memory().total / (1024 ** 3)  # Convert to GB
    return ram_size


def get_screen_size():
    # Assuming the screen size based on common display types
    # This might not be accurate for all systems
    screen_size = "N/A"
    try:
        width, height = gw.getWindowsWithTitle('')[0].size
        diagonal_size = (width * 2 + height * 2) ** 0.5
        screen_size = f"{diagonal_size:.1f} inches"
    except:
        pass
    return screen_size


def get_network_info():
    try:
        wifi_mac_address = ':'.join(['{:02x}'.format((int(ethernet_mac_address.split(':')))) for ethernet_mac_address in psutil.net_if_addrs()['Wi-Fi'][0].address.split(':')])
    except:
        wifi_mac_address = "N/A"

    try:
        ethernet_mac_address = ':'.join(['{:02x}'.format((int(ethernet_mac_address.split(':')))) for ethernet_mac_address in psutil.net_if_addrs()['Ethernet'][0].address.split(':')])
    except:
        ethernet_mac_address = "N/A"

    return wifi_mac_address, ethernet_mac_address


def get_public_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        public_ip = json.loads(response.text)['ip']
    except:
        public_ip = "N/A"
    return public_ip


def get_windows_version():
    windows_version = platform.version()
    return windows_version


if __name__ == "__main__":
    # Installed software list
    installed_software_list = get_installed_software()
    print("All Installed software:")
    for software in installed_software_list:
        print(f" - {software}")

    # Internet speed
    download_speed, upload_speed = get_internet_speed()
    print(f"\nInternet Speed:")
    print(f"Download Speed: {download_speed:.2f} Mbps")
    print(f"Upload Speed: {upload_speed:.2f} Mbps")

    # Screen resolution
    screen_resolution = get_screen_resolution()
    print("\nScreen Resolution:")
    if screen_resolution:
        print(f"Width: {screen_resolution[0]} pixels")
        print(f"Height: {screen_resolution[1]} pixels")
    else:
        print("Unable to determine screen resolution.")

    # CPU details
    cpu_model, num_cores, num_threads = get_cpu_info()
    print("\nCPU Model:")
    print(f"Model: {cpu_model}")
    print()
    print('No of core and threads of CPU :')
    print(f"Number of Cores: {num_cores}")
    print(f"Number of Threads: {num_threads}")

    # GPU details
    gpu_model = get_gpu_info()
    print(f"\nGPU Model: {gpu_model}")

    # RAM size
    ram_size = get_ram_size()
    print(f"\nRAM Size: {ram_size:.2f} GB")

    # Screen size
    screen_size = get_screen_size()
    print(f"\nScreen Size: {screen_size}")
    print()

    # Network details
    wifi_mac_address, ethernet_mac_address = get_network_info()
    print(f"Wifi/Ethernet mac address:")
    print(f"Wifi mac address: {wifi_mac_address}")
    print(f"Ethernet MAC Address: {ethernet_mac_address}")

    # Public IP address
    public_ip = get_public_ip()
    print(f"\nPublic IP Address: {public_ip}")

    # Windows version
    windows_version = get_windows_version()
    print(f"\nWindows Version: {windows_version}")