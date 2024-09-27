import paramiko
import time

def connect(switch_hostname, switch_port, user, passwd):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'Connecting to {switch_hostname}')
    ssh_client.connect(hostname=switch_hostname, port=switch_port, username=user, password=passwd,
                       look_for_keys=False, allow_agent=False)
    return ssh_client

def get_shell(ssh_client):
    shell = ssh_client.invoke_shell()
    return shell

def send_command(shell, command, timout=0.5):
    shell.send(command + '\n')
    time.sleep(timout)

def show(shell, n=100000):
    output = shell.recv(n)
    return output.decode()

def close(ssh_client):
    if ssh_client.get_transport().is_active() == True:
        ssh_client.close()

