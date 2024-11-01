import paramiko
import time
from datetime import datetime
import getpass

# Function to fetch hostname and save output
def fetch_and_save_output(ip, username, password):
    try:
        # Establish SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)

        # Start an interactive shell session
        shell = ssh.invoke_shell()
        time.sleep(1)  # Allow time to initialize shell

        # Send the "show tech-support" command
        shell.send("show tech-support\n")
        time.sleep(2)  # Short wait before reading initial output

        # Capture the output in chunks until the command finishes
        output = ""
        while True:
            # Wait a moment to allow data to accumulate
            time.sleep(2)
            
            # Read output if ready
            if shell.recv_ready():
                chunk = shell.recv(65535).decode("utf-8")
                output += chunk
                # Break the loop if the command prompt reappears (indicating the command is done)
                if chunk.endswith("#") or chunk.endswith(">"):
                    break

        # Get hostname from the output or command prompt
        shell.send("show hostname\n")
        time.sleep(1)
        hostname = shell.recv(1024).decode("utf-8").split()[-1].strip()

        # Save the output to a file with the date and hostname
        filename = f"{datetime.now().strftime('%Y%m%d')}_{hostname}_tech_support.txt"
        with open(filename, "w") as file:
            file.write(output)

        print(f"Output saved to {filename}")

        # Close the SSH session
        ssh.close()

    except Exception as e:
        print(f"Failed to retrieve tech-support from {ip}. Error: {e}")

# Main program
if __name__ == "__main__":
    # Get user input for IP addresses, username, and password
    ip_addresses = input("Enter target IP addresses (comma-separated): ").split(",")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")  # Secure password input

    # Process each IP address
    for ip in ip_addresses:
        ip = ip.strip()  # Remove any extra whitespace
        print(f"Connecting to {ip}...")
        fetch_and_save_output(ip, username, password)