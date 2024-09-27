# This script can be check show ip route and show ip bgp
import myparamiko # myparamiko.py should be in the same directory with this script 
import threading
import getpass
import time

user_name = input('Please enter your username: ')
user_pwd = getpass.getpass('Enter password:')
en_pwd = getpass.getpass('Enable password:')
ip_addr = input('Please enter ip address:')

# this function check_show_ip_route_bgp of router/switch
# this is the target function which gets executed by each thread
def check_show_ip_route_bgp(switch):
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
    myparamiko.send_command(shell, 'show ip bgp ' + ip_addr)
    myparamiko.send_command(shell, '\n')
    myparamiko.send_command(shell, 'show ip route ' + ip_addr)
    time.sleep(1)
    output = myparamiko.show(shell)
    output_list = output.splitlines()
    output = '\n'.join(output_list)
    print(output)

    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

  
    file_name = f'{switch["switch_hostname"]}-show_ip_route_bgp_{hour}{minute}_{day}-{month}-{year}.txt'
    with open(file_name, 'w') as f:
        f.write(output)
    
    print(f'Task completed for {switch["switch_hostname"]}')
    print(f'Closing connection to {switch["switch_hostname"]}')
    print('#'*50)
    myparamiko.close(client)

# creating a dictionary for each device to connect to
switch1 = {'switch_hostname':'10.226.10.7', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}  
switch2 = {'switch_hostname':'10.226.10.8', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd} 
switch3 = {'switch_hostname':'10.236.10.7', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd} 

# creating a list of dictionaries (of devices)
switches = [switch1, switch2, switch3]

# creating an empty list (it will store the threads)
threads = list()
for switch in switches:
    # creating a thread for each switch that executes the check_show_ip_route_bgp function
    th = threading.Thread(target=check_show_ip_route_bgp, args=(switch,))
    threads.append(th)  # appending the thread to the list

# starting the threads
for th in threads:
    th.start()

# waiting for the threads to finish
for th in threads:
    th.join()