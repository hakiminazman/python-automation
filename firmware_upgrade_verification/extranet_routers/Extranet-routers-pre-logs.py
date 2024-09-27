#This script can be used to capture the pre-logs from Extranet routers (ASR-1002-HX)
from netmiko import ConnectHandler
from datetime import datetime
import time
import threading  # implements threading in Python
import getpass

# getting the current time as a timestamp
start = time.time()


# this is the target function which gets executed by each thread
def asr_pre_logs(device):
    connection = ConnectHandler(**device)
    time.sleep(2)
    print('Entering the enable mode...')
    connection.enable()
    show_cmd = ['show version',
                'show clock',
                'show license summary',
                'show processes memory platform sorted',
                'show processes cpu platform sorted',
                'show proc cpu history',
                'show ip interface brief',
                'show interface description',
                'show inventory',
                'show ntp associations',
                'show cdp neighbor',
                'show env all',
                'show platform hardware crypto-throughput level',
                'show ip bgp summary',
                'show bgp vrf FVRF-INET-IPSEC-VPN all summary',
                'show ip ospf neighbors',
                'show bfd neighbors',
                'show crypto session brief',
                'show ip route summary',
                'show running-config',
                ]
    for cmd in show_cmd:
        output = connection.send_command(cmd)
        # print(output)
        prompt = connection.find_prompt()
        hostname = prompt[0:-1]
        # print(hostname)

        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute


        filename = f'{hostname}-pre_logs_{hour}_{day}-{month}-{year}.txt'
        with open(filename, 'a+') as asr_pre_logs:
            asr_pre_logs.write('\n')
            asr_pre_logs.write(hostname + '#' + cmd)
            asr_pre_logs.write('\n')
            asr_pre_logs.write(output)
            asr_pre_logs.write('\n')

    print(f'Task completed for {hostname}')    
    print(f'Closing connection to {hostname}')
    print('#' * 50)
    connection.disconnect()


user_name = input('Please enter your username:')
user_pass = getpass.getpass('Enter the user password:')
enable_pwd = getpass.getpass('Please enter enable password:')

with open('extranet-routers.txt') as f:  ##reference the correct router file
    devices = f.read().splitlines()

# creating an empty list (it will store the threads)
threads = list()
for ip in devices:
    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': user_name,
        'password': user_pass,
        'port': 22,
        'secret': enable_pwd,  # this is the enable password
        'verbose': True  # optional, default False
    }
    # creating a thread for each router that executes the backup function
    th = threading.Thread(target=asr_pre_logs, args=(device,))
    threads.append(th)  # appending the thread to the list

# starting the threads
for th in threads:
    th.start()

# waiting for the threads to finish
for th in threads:
    th.join()

end = time.time()
print(f'Total execution time:{end - start}')
