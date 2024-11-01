from netmiko import ConnectHandler
from datetime import datetime
import getpass

# Function to connect to the device and run the commands
def connect_and_run_commands(ip, username, password, commands):
    # Define the device parameters with an increased timeout
    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': username,
        'password': password,
        'timeout': 60,  # Set the overall operation timeout to 60 seconds
    }

    try:
        # Establish SSH connection
        connection = ConnectHandler(**device)

        # Get hostname of the device (reliable command to get the hostname)
        hostname = connection.find_prompt().strip('#')

        # Generate filename with hostname and current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        filename = f"{hostname}_{current_date}.txt"

        # Open the file to write the command outputs
        with open(filename, 'w') as file:
            for command in commands:
                # Run each command and get the output
                output = connection.send_command(command)
                
                # Write the command and its output to the file
                file.write(f"\n\nCommand: {command}\n")
                file.write(f"{output}\n")
        
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

    # Get up to 5 commands from the user
    commands = []
    print("Enter up to 5 Cisco commands (press Enter to skip the remaining commands):")
    for i in range(5):
        command = input(f"Command {i+1}: ")
        if command.strip():  # Only add non-empty commands
            commands.append(command)
        else:
            break  # Stop if the user doesn't provide a command

    if not commands:
        print("No commands provided. Exiting...")
        return

    # Loop through each IP and run the commands
    for ip in ip_addresses:
        ip = ip.strip()  # Clean up any extra spaces
        connect_and_run_commands(ip, username, password, commands)

if __name__ == "__main__":
    main()
