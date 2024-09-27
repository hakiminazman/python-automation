# This script can be used to copy firmware from scp server
import myparamiko # myparamiko.py should be in the same directory with this script 
import threading
import getpass
import time

user_name = input('Please enter your username: ')
user_pwd = getpass.getpass('Enter password:')
en_pwd = getpass.getpass('Enable password:')
scp_username = input('Please enter scp username: ')
scp_pwd = getpass.getpass('Enter scp password:')
firmware = input('Please enter firmware: ')

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
    myparamiko.send_command(shell, 'copy scp://' + scp_username + ':' + scp_pwd + '@10.226.42.31/software-images/' + firmware + ' bootflash:' + ' vrf Mgmt-intf')
    print('File transfer in progress! Please wait..')
    time.sleep(750)
    myparamiko.send_command(shell, '\n')
    myparamiko.send_command(shell, 'verify /md5 bootflash:' + firmware)
    time.sleep(90)
    myparamiko.send_command(shell, '\n')
    myparamiko.send_command(shell, 'dir bootflash: | inc ' + firmware)
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

  
    file_name = f'{switch["switch_hostname"]}-copy-firmware_{hour}{minute}_{day}-{month}-{year}.txt'
    with open(file_name, 'w') as f:
        f.write(output)
    
    print(f'Task completed for {switch["switch_hostname"]}')    
    print(f'Closing connection to {switch["switch_hostname"]}')
    print('#'*50)
    myparamiko.close(client)

# creating a dictionary for each device to connect to
switch1 = {'switch_hostname':'10.226.10.7', 'switch_port': '22', 'user':user_name, 'passwd':user_pwd}


# creating a list of dictionaries (of devices)
switches = [switch1]

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