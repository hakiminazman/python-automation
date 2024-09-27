# This script can be used to copy firmware from scp server
import myparamiko # myparamiko.py should be in the same directory with this script 
import threading
import getpass
import time

user_name = input('Please enter your username: ')
user_pwd = getpass.getpass('Enter password:')
en_pwd = getpass.getpass('Enable password:')

# this function copy_firmware of iosxe router 
# this is the target function which gets executed by each thread
def copy_firmware(switch):
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
    myparamiko.send_command(shell, 'conf t')
    myparamiko.send_command(shell, 'no boot system flash:<old firmware file here>') #remove the boot statement from old firmware 
    myparamiko.send_command(shell, 'boot system flash:<new firmware file here>') #reconfigure the new boot statement pointing to new firmware
    myparamiko.send_command(shell, 'end')
    myparamiko.send_command(shell, 'reload')
    myparamiko.send_command(shell, 'y')
    myparamiko.send_command(shell, '\n')
    
    output = myparamiko.show(shell)
    output_list = output.splitlines()
    #print(output_list)
    output_list = output_list[40:-1]
    output = '\n'.join(output_list)
    #print(output)

    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

  
    file_name = f'{switch["switch_hostname"]}-execute_{hour}{minute}_{day}-{month}-{year}.txt'
    with open(file_name, 'w') as f:
        f.write(output)
    
    print(f'Task completed for {switch["switch_hostname"]}')    
    print(f'Closing connection to {switch["switch_hostname"]}')
    print('#'*50)
    myparamiko.close(client)

# creating a dictionary for each device to connect to
switch1 = {'switch_hostname':'10.236.10.39', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}
switch2 = {'switch_hostname':'10.236.10.40', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}
switch3 = {'switch_hostname':'10.236.10.32', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}
switch4 = {'switch_hostname':'10.236.10.31', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}
switch5 = {'switch_hostname':'10.236.10.30', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}
switch6 = {'switch_hostname':'10.236.10.29', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}
switch7 = {'switch_hostname':'10.236.10.28', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}
switch8 = {'switch_hostname':'10.236.10.27', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}
switch9 = {'switch_hostname':'10.236.10.38', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}
switch10 = {'switch_hostname':'10.236.10.37', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}
switch11 = {'switch_hostname':'10.236.10.36', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}
switch12 = {'switch_hostname':'10.236.10.35', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}
switch13 = {'switch_hostname':'10.236.10.34', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}
switch14 = {'switch_hostname':'10.236.10.33', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}
switch15 = {'switch_hostname':'10.236.10.41', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}

# creating a list of dictionaries (of devices)
switches = [switch1,switch2, switch3,switch4,switch5,switch6,switch7,switch8,switch9,switch10,switch11,switch12,switch13,switch14,switch15]

# creating an empty list (it will store the threads)
threads = list()
for switch in switches:
    # creating a thread for each switch that executes the copy_firmware function
    th = threading.Thread(target=copy_firmware, args=(switch,))
    threads.append(th)  # appending the thread to the list

# starting the threads
for th in threads:
    th.start()

# waiting for the threads to finish
for th in threads:
    th.join()
