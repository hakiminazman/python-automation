import json
from napalm import get_network_driver
import time
from datetime import datetime
import getpass
from netmiko import ConnectHandler

# ping(destination, source='', ttl=255, timeout=2, size=100, count=5, vrf='', source_interface='')
# Executes ping on the device and returns a dictionary with the result
# 
# Parameters:	
# destination – Host or IP Address of the destination
# source (optional) – Source address of echo request
# ttl (optional) – Maximum number of hops
# timeout (optional) – Maximum seconds to wait after sending final packet
# size (optional) – Size of request (bytes)
# count (optional) – Number of ping request to send
# vrf (optional) – Use a specific VRF to execute the ping
# source_interface (optional) – Use an IP from a source interface as source address of echo request

user_name = input('Please enter your username: ')
user_pwd = getpass.getpass('Enter password:')
en_pwd = getpass.getpass('Enable password:')

optional_args = {}
optional_args['secret'] = en_pwd

iosxe_ping = ['10.236.10.8',
              '10.236.10.7',
              ]

nxos_ping = ['10.236.10.3',
             ]

dest_ip = ['10.226.1.1',
           '10.226.1.2',
           '10.226.1.3',
           '10.226.10.1',
           '10.226.15.1',  
           '10.236.15.1',
           '10.226.32.1',  
           '10.236.32.1',
           '10.226.48.1',
           ]

now = datetime.now()
year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute

for ip_address in iosxe_ping:
    print("Connecting to " + str(ip_address))
    driver = get_network_driver('ios')
    iosxe_device = driver(ip_address, user_name, user_pwd, optional_args=optional_args)
    time.sleep(2)
    iosxe_device.open()
    for host in dest_ip:
        run_ping_check = iosxe_device.ping(destination=host, timeout=1, source_interface='loopback0')
        print(json.dumps(run_ping_check, indent=4))
    

        file_name = f'{ip_address}-run_ping_check_{hour}{minute}_{day}-{month}-{year}.txt'
        with open(file_name, 'a') as outfile:
            json.dump(run_ping_check, outfile, indent=4)

    print(f'Task completed for {ip_address}')
    print(f'Closing connection to {ip_address}')
    print('#'*50)
iosxe_device.close()

for ip_address in nxos_ping:
    print ("Connecting to " + str(ip_address))
    driver = get_network_driver('nxos_ssh')
    nxos_device = driver(ip_address, user_name, user_pwd, optional_args=optional_args, timeout=60)
    time.sleep(2)
    nxos_device.open()
    for host in dest_ip:
        run_ping_check = nxos_device.ping(destination=host)
        print (json.dumps(run_ping_check, indent=4))
        
        
        file_name = f'{ip_address}-run_ping_check_{hour}{minute}_{day}-{month}-{year}.txt'
        with open(file_name, 'a') as outfile:
            json.dump(run_ping_check, outfile, indent=4)

    print(f'Task completed for {ip_address}')
    print(f'Closing connection to {ip_address}')            
    print('#'*50)        
nxos_device.close()
