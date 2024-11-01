from netmiko import ConnectHandler
from datetime import datetime
import getpass

# Function to connect to the device and run the command
def connect_and_run_command(ip, username, password, command):
    # Define the device parameters
    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': username,
        'password': password,
    }

    try:
        # Establish SSH connection
        connection = ConnectHandler(**device)
        
        # Get hostname of the device
        hostname = connection.send_command('show running-config | include hostname').split()[-1]

        # Run the command and get the output
        output = connection.send_command(command)

        # Generate filename with hostname and current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        filename = f"{hostname}_{current_date}.txt"

        # Save output to the file
        with open(filename, 'w') as file:
            file.write(output)

        print(f"Output saved to {filename}")

        # Disconnect the session
        connection.disconnect()

    except Exception as e:
        print(f"Failed to connect to {ip}. Error: {e}")

# Main function to get user inputs and process multiple devices
def main():
    # Get the target IP(s)
    ip_addresses = input("Enter target switch IP addresses (comma separated if multiple): ").split(',')

    # Get user access credentials
    username = input("Enter your SSH username: ")
    password = getpass.getpass("Enter your SSH password: ")

    # Get the command to execute
    command = input("Enter the command to execute (e.g., 'show run', 'show ip int br'): ")

    # Loop through each IP and run the command
    for ip in ip_addresses:
        ip = ip.strip()  # Clean up any extra spaces
        connect_and_run_command(ip, username, password, command)

if __name__ == "__main__":
    main()













# #This script can be used to capture the pre-logs from Internet routers (ASR-1002-HX)
# from netmiko import ConnectHandler
# from datetime import datetime
# import time
# import threading  # implements threading in Python
# import getpass

# # getting the current time as a timestamp
# start = time.time()


# # this is the target function which gets executed by each thread
# def asr_pre_logs(device):
#     connection = ConnectHandler(**device)
#     time.sleep(2)
#     #print('Entering the enable mode...')
#     connection.enable()
#     show_cmd = ['show version',
#                 ]
#     for cmd in show_cmd:
#         output = connection.send_command(cmd)
#         # print(output)
#         prompt = connection.find_prompt()
#         hostname = prompt[0:-1]
#         # print(hostname)

#         now = datetime.now()
#         year = now.year
#         month = now.month
#         day = now.day
#         hour = now.hour
#         minute = now.minute


#         filename = f'{hostname}-{hour}_{day}-{month}-{year}.txt'
#         with open(filename, 'a+') as asr_pre_logs:
#             asr_pre_logs.write('\n')
#             asr_pre_logs.write(hostname + '#' + cmd)
#             asr_pre_logs.write('\n')
#             asr_pre_logs.write(output)
#             asr_pre_logs.write('\n')

#     print(f'Task completed for {hostname}')    
#     print(f'Closing connection to {hostname}')
#     print('#' * 50)
#     connection.disconnect()


# user_name = input('Please enter your username:')
# user_pass = getpass.getpass('Enter the user password:')

# with open('internet-routers.txt') as f:  ##reference the correct router file
#     devices = f.read().splitlines()

# # creating an empty list (it will store the threads)
# threads = list()
# for ip in devices:
#     device = {
#         'device_type': 'cisco_ios',
#         'host': ip,
#         'username': user_name,
#         'password': user_pass,
#         'port': 22,
#         'secret': enable_pwd,  # this is the enable password
#         'timeout': 150,
#         'verbose': True  # optional, default False
#     }
#     # creating a thread for each router that executes the backup function
#     th = threading.Thread(target=asr_pre_logs, args=(device,))
#     threads.append(th)  # appending the thread to the list

# # starting the threads
# for th in threads:
#     th.start()

# # waiting for the threads to finish
# for th in threads:
#     th.join()

# end = time.time()
# print(f'Total execution time:{end - start}')
