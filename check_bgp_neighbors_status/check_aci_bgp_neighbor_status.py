# This script can be used to verify BGP neighborship
import myparamiko # myparamiko.py should be in the same directory with this script 
import threading
import getpass
import time

user_name = input('Please enter your username: ')
user_pwd = getpass.getpass('Enter password:')

# this function check_show_bgp of router/switch
# this is the target function which gets executed by each thread
def check_show_bgp(switch):
    client = myparamiko.connect(**switch)
    time.sleep(1)
    shell = myparamiko.get_shell(client)
    time.sleep(1)
    
    myparamiko.send_command(shell, 'show bgp all summary vrf all')
    time.sleep(1)
    myparamiko.send_command(shell, '\n')
    myparamiko.send_command(shell, 'show bfd neighbors vrf all')
    time.sleep(1.5)
    myparamiko.send_command(shell, '\n')  
    output = myparamiko.show(shell)
    #print(output)
    output_list = output.splitlines()
    output = '\n'.join(output_list)

    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

  
    file_name = f'{switch["switch_hostname"]}-show_bgp_{hour}{minute}_{day}-{month}-{year}.txt'
    with open(file_name, 'w') as f:
        f.write(output)
        
    print(f'Task completed for {switch["switch_hostname"]}')    
    print(f'Closing connection to {switch["switch_hostname"]}')
    print('#'*50)
    myparamiko.close(client)

# creating a dictionary for each device to connect to
switch1 = {'switch_hostname':'10.236.10.17', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}

# creating a list of dictionaries (of devices), need to add more devices depending on the number of switches
switches = [switch1]

# creating an empty list (it will store the threads)
threads = list()
for switch in switches:
    # creating a thread for each switch that executes the check_show_bgp function
    th = threading.Thread(target=check_show_bgp, args=(switch,))
    threads.append(th)  # appending the thread to the list

# starting the threads
for th in threads:
    th.start()

# waiting for the threads to finish
for th in threads:
    th.join()