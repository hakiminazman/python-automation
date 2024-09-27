import json
from napalm import get_network_driver
import time
from datetime import datetime
import getpass
from netmiko import ConnectHandler

user_name = input('Please enter your username: ')
user_pwd = getpass.getpass('Enter password:')
en_pwd = getpass.getpass('Enable password:')

optional_args = {}
optional_args['secret'] = en_pwd

iosxe_intf = ['10.236.10.8',
              '10.236.10.7',
              ]

nxos_intf = ['10.236.10.3',
             ]

now = datetime.now()
year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute

for ip_address in iosxe_intf:
    print("Connecting to " + str(ip_address))
    driver = get_network_driver('ios')
    iosxe_device = driver(ip_address, user_name, user_pwd, optional_args=optional_args)
    time.sleep(2)
    iosxe_device.open()
    run_get_interfaces_counters = iosxe_device.get_interfaces_counters()
    print(json.dumps(run_get_interfaces_counters, sort_keys=True, indent=4))
    file_name = f'{ip_address}-get_interfaces_counters_{hour}{minute}_{day}-{month}-{year}.txt'
    with open(file_name, 'a') as outfile:
        json.dump(run_get_interfaces_counters, outfile, indent=4)
            
    print(f'Task completed for {ip_address}')
    print(f'Closing connection to {ip_address}')
    print('#'*50)
iosxe_device.close()

for ip_address in nxos_intf:
    print ("Connecting to " + str(ip_address))
    driver = get_network_driver('nxos_ssh')
    nxos_device = driver(ip_address, user_name, user_pwd, optional_args=optional_args, timeout=60)
    time.sleep(2)
    nxos_device.open()
    run_get_interfaces_counters = nxos_device.get_interfaces_counters()
    print (json.dumps(run_get_interfaces_counters, sort_keys=True, indent=4))
    file_name = f'{ip_address}-get_interfaces_counters_{hour}{minute}_{day}-{month}-{year}.txt'
    with open(file_name, 'a') as outfile:
        json.dump(run_get_interfaces_counters, outfile, indent=4)

    print(f'Task completed for {ip_address}')
    print(f'Closing connection to {ip_address}')            
    print('#'*50)        
nxos_device.close()
