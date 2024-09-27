# This script can be used to capture the pre-logs from DC Edge switches
import myparamiko # myparamiko.py should be in the same directory with this script (or in sys.path)
import threading
import getpass
import time

user_name = input('Please enter your username: ')
user_pwd = getpass.getpass('Enter password:')
en_pwd = getpass.getpass('Enable password:')

# this function nx_post_logss the config of a switch
# this is the target function which gets executed by each thread
def nx_post_logs(switch):
    client = myparamiko.connect(**switch)
    time.sleep(5)
    shell = myparamiko.get_shell(client)
    time.sleep(1)
    
    myparamiko.send_command(shell, 'enable')
    time.sleep(0.5)
    myparamiko.send_command(shell, en_pwd)  # this is the enable pwd command
    time.sleep(0.5)
    myparamiko.send_command(shell, 'terminal length 0')
    myparamiko.send_command(shell, 'terminal width 511')
    myparamiko.send_command(shell, 'show version')
    myparamiko.send_command(shell, 'show environment')
    myparamiko.send_command(shell, 'show inventory all')    
    myparamiko.send_command(shell, 'show license usage')    
    myparamiko.send_command(shell, 'show boot')    
    myparamiko.send_command(shell, 'show feature')
    myparamiko.send_command(shell, 'show processes cpu history')
    myparamiko.send_command(shell, 'show interface status')    
    myparamiko.send_command(shell, 'show lldp neighbors')    
    myparamiko.send_command(shell, 'show cdp neighbors')    
    myparamiko.send_command(shell, 'show ip bgp summary')    
    myparamiko.send_command(shell, 'show isis adjacency')    
    myparamiko.send_command(shell, 'show bfd neighbors')    
    myparamiko.send_command(shell, 'show ip route summary')    
    myparamiko.send_command(shell, 'show ntp peers')    
    myparamiko.send_command(shell, 'show ntp peer-status')    
    myparamiko.send_command(shell, 'show radius-server')  
    myparamiko.send_command(shell, 'show ip ospf neighbors vrf IPN')
    myparamiko.send_command(shell, 'show ptp brief')
    myparamiko.send_command(shell, 'show bfd neighbors vrf IPN')
    myparamiko.send_command(shell, 'show ip pim neighbor vrf IPN')
    myparamiko.send_command(shell, 'show ip pim rp vrf IPN')
    myparamiko.send_command(shell, 'show ip route vrf IPN')
    myparamiko.send_command(shell, 'show ip route summary vrf IPN')    
    myparamiko.send_command(shell, 'show running-config')   
    time.sleep(1)
    
    output = myparamiko.show(shell)
    # print(output)
    output_list = output.splitlines()
    output_list = output_list[51:-1]
    #print(output_list)
    output = '\n'.join(output_list)
    # print(output)

    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

  
    file_name = f'{switch["switch_hostname"]}-post-logs_{day}-{month}-{year}.txt'
    with open(file_name, 'w') as f:
        f.write(output)        
        
    print(f'Task completed for {switch["switch_hostname"]}')    
    print(f'Closing connection to {switch["switch_hostname"]}')
    print('#'*50)
    myparamiko.close(client)

# creating a dictionary for each device to connect to
switch1 = {'switch_hostname':'rpdcecbj1b-0301-001.network.paynet.my', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}
switch2 = {'switch_hostname':'rpdcecbj1b-0302-002.network.paynet.my', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}

# creating a list of dictionaries (of devices)
switches = [switch1, switch2]

# creating an empty list (it will store the threads)
threads = list()
for switch in switches:
    # creating a thread for each switch that executes the nx_post_logs function
    th = threading.Thread(target=nx_post_logs, args=(switch,))
    threads.append(th)  # appending the thread to the list

# starting the threads
for th in threads:
    th.start()

# waiting for the threads to finish
for th in threads:
    th.join()