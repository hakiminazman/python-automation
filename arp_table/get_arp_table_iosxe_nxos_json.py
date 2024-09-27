import json
from napalm import get_network_driver
import time
from datetime import datetime
import getpass
from netmiko import ConnectHandler

# get_arp_table(vrf='')
# Returns a list of dictionaries having the following set of keys:
# interface (string)
# mac (string)
# ip (string)
# age (float)

user_name = input('Please enter your username: ')
user_pwd = getpass.getpass('Enter password:')
en_pwd = getpass.getpass('Enable password:')

optional_args = {}
optional_args['secret'] = en_pwd

iosxe_arp = ['10.236.10.8',
              '10.236.10.7',
              ]

nxos_arp = ['10.236.10.3',
             ]

now = datetime.now()
year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute

for ip_address in iosxe_arp:
    print("Connecting to " + str(ip_address))
    driver = get_network_driver('ios')
    iosxe_device = driver(ip_address, user_name, user_pwd, optional_args=optional_args)
    time.sleep(2)
    iosxe_device.open()
    run_get_arp_table = iosxe_device.get_arp_table(vrf='')
    print(json.dumps(run_get_arp_table, indent=4))
    file_name = f'{ip_address}-get_arp_table_{hour}{minute}_{day}-{month}-{year}.txt'
    with open(file_name, 'a') as outfile:
        json.dump(run_get_arp_table, outfile, indent=4)
            
    print(f'Task completed for {ip_address}')
    print(f'Closing connection to {ip_address}')
    print('#'*50)
iosxe_device.close()

for ip_address in nxos_arp:
    print ("Connecting to " + str(ip_address))
    driver = get_network_driver('nxos_ssh')
    nxos_device = driver(ip_address, user_name, user_pwd, optional_args=optional_args, timeout=60)
    time.sleep(2)
    nxos_device.open()
    run_get_arp_table = nxos_device.get_arp_table(vrf='')
    print (json.dumps(run_get_arp_table, indent=4))
    file_name = f'{ip_address}-get_arp_table_{hour}{minute}_{day}-{month}-{year}.txt'
    with open(file_name, 'a') as outfile:
        json.dump(run_get_arp_table, outfile, indent=4)

    print(f'Task completed for {ip_address}')
    print(f'Closing connection to {ip_address}')            
    print('#'*50)        
nxos_device.close()
