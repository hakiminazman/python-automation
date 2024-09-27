# This script can be used to enable BGP GSHUT and OSPF Max-Metric Feature
import myparamiko # myparamiko.py should be in the same directory with this script (or in sys.path)
import threading
import getpass
import time

user_name = input('Please enter your username: ')
user_pwd = getpass.getpass('Enter password:')
en_pwd = getpass.getpass('Enable password:')

# this function enables BGP GSHUT and OSPF Max-Metric Feature
# this is the target function which gets executed by each thread
def nx_enable_maintenance(switch):
    client = myparamiko.connect(**switch)
    time.sleep(5)
    shell = myparamiko.get_shell(client)
    time.sleep(1)
    
    myparamiko.send_command(shell, 'enable')
    time.sleep(0.5)
    myparamiko.send_command(shell, en_pwd)  # this is the enable pwd command
    time.sleep(0.5)
    myparamiko.send_command(shell, 'config t')
    myparamiko.send_command(shell, 'router bgp <>') ### Replace <> with correct ASN (NTT AS 65101, BGR AS 65201)
    myparamiko.send_command(shell, 'graceful-shutdown activate')  #Activate BGP graceful shutdown (GSHUT) feature  
    myparamiko.send_command(shell, 'exit')
    myparamiko.send_command(shell, 'router ospf IPN')    
    myparamiko.send_command(shell, 'vrf IPN')    
    myparamiko.send_command(shell, 'max-metric router-lsa external-lsa summary-lsa')    #Activate OSPF max-metric feature
    myparamiko.send_command(shell, 'end')
    myparamiko.send_command(shell, 'copy running-config startup-config')
    time.sleep(5)
    myparamiko.send_command(shell, 'terminal length 0')
    myparamiko.send_command(shell, 'show ip bgp community graceful-shutdown')    
    myparamiko.send_command(shell, 'show ip ospf')    
    time.sleep(1)
    
    output = myparamiko.show(shell)
    print(output)
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

  
    file_name = f'{switch["switch_hostname"]}-enable_maintenance_{day}-{month}-{year}.txt'
    with open(file_name, 'w') as f:
        f.write(output)
        
    print(f'Task completed for {switch["switch_hostname"]}')    
    print(f'Closing connection to {switch["switch_hostname"]}')
    print('#'*50)
    myparamiko.close(client)

# creating a dictionary for each device to connect to
switch1 = {'switch_hostname':'rpdcecbj1b-0301-001.network.paynet.my', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}

# creating a list of dictionaries (of devices)
switches = [switch1]

# creating an empty list (it will store the threads)
threads = list()
for switch in switches:
    # creating a thread for each switch that executes the nx_enable_maintenance function
    th = threading.Thread(target=nx_enable_maintenance, args=(switch,))
    threads.append(th)  # appending the thread to the list

# starting the threads
for th in threads:
    th.start()

# waiting for the threads to finish
for th in threads:
    th.join()