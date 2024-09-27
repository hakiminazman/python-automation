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

iosxe_ping = ['10.236.11.254',
              ]


dest_ip = ['10.236.10.150', ##Cisco APIC Controller 3
           '10.236.10.101', ##FTD Firewall Physical  
           '10.236.10.102', ##FTD Firewall Physical  
           '10.236.10.103', ##Palo Alto Firewall Physical  
           '10.236.10.104', ##Palo Alto Firewall Physical  
           '10.236.10.61', ##NTP Server
            '10.236.10.1',
            '10.236.10.2',
            '10.236.10.3',
            '10.236.10.4',
            '10.236.10.5',
            '10.236.10.6',
            '10.236.10.7',
            '10.236.10.8',
            '10.236.10.11',
            '10.236.10.12',
            '10.236.10.13',
            '10.236.10.14',
            '10.236.10.15',
            '10.236.10.16',
            '10.236.10.17',
            '10.236.10.18',
            '10.236.10.19',
            '10.236.10.20',
            '10.236.10.21',
            '10.236.10.22',
            '10.236.10.23',
            '10.236.10.24',
            '10.236.10.25',
            '10.236.10.26',
            '10.236.10.27',
            '10.236.10.28',
            '10.236.10.29',
            '10.236.10.30',
            '10.236.10.31',
            '10.236.10.32',
            '10.236.10.33',
            '10.236.10.34',
            '10.236.10.35',
            '10.236.10.36',
            '10.236.10.37',
            '10.236.10.38',
            '10.236.10.39',
            '10.236.10.40',
            '10.236.10.41',  
            '10.236.10.58',
            '10.236.10.59',
            '10.236.10.61',
            '10.236.10.62',
            '10.236.10.63',
            '10.236.10.64',
            '10.236.10.101',  
            '10.236.10.102',  
            '10.236.10.103',  
            '10.236.10.104',  
            '10.236.10.105',  
            '10.236.10.106',  
            '10.236.10.109',  
            '10.236.10.110',  
            '10.236.10.111',  
            '10.236.10.112',  
            '10.236.10.113',  
            '10.236.10.114',  
            '10.236.10.151',  
            '10.236.10.152',  
            '10.236.10.153',  
            '10.236.11.254',  
            '10.236.13.1',    
            '10.236.13.2',    
            '10.236.13.3',    
            '10.236.13.4',    
            '10.236.13.6',    
            '10.236.13.7',    
            '10.236.13.8',    
            '10.236.13.9',    
            '10.236.13.10',    
            '10.236.13.14',    
            '10.236.13.41',    
            '10.236.13.42',    
            '10.236.13.43',    
            '10.236.13.44',    
            '10.236.13.61',    
            '10.236.13.62',    
            '10.236.13.70',    
            '10.236.13.71',    
            '10.236.13.72',    
            '10.236.13.73',              
            '10.236.13.90',    
            '10.236.13.91',    
            '10.236.13.92',    
            '10.236.13.93',    
            '10.236.13.94',    
            '10.236.13.95',    
            '10.236.13.96',    
            '10.236.13.99',    
            '10.236.13.100',  
            '10.236.13.101',  
            '10.236.13.102',  
            '10.236.13.110',  
            '10.236.13.111',  
            '10.236.13.120',  
            '10.236.13.121',  
            '10.236.13.122',  
            '10.236.13.123',  
            '10.236.13.124',  
            '10.236.13.125',  
            '10.236.13.254',    
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
        run_ping_check = iosxe_device.ping(destination=host, timeout=1)
        print(json.dumps(run_ping_check, indent=4))
    

        file_name = f'{ip_address}-run_ping_check_{hour}{minute}_{day}-{month}-{year}.txt'
        with open(file_name, 'a') as outfile:
            json.dump(run_ping_check, outfile, indent=4)

    print(f'Task completed for {ip_address}')
    print(f'Closing connection to {ip_address}')
    print('#'*50)
iosxe_device.close()
