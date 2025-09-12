import subprocess
import time
import re

def get_user():
    """Run 'whoami' to get the current user."""
    try:
        # Run whoami command and capture output
        result = subprocess.run(['whoami'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error getting user: {e}"

def get_machine_name():
    """Run 'hostname' to get the machine name."""
    try:
        # Run hostname command and capture output
        result = subprocess.run(['hostname'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error getting machine name: {e}"

def get_network_info():
    """Run 'ipconfig' to get IP address, subnet mask, and default gateway."""
    try:
        # Run ipconfig command and capture output
        result = subprocess.run(['ipconfig'], capture_output=True, text=True, check=True)
        output = result.stdout
        #print(output)

        # Initialize variables
        ip_address = "Not found"
        subnet_mask = "Not found"
        default_gateway = "Not found"

        # Flag to track if we're in the Default Gateway section
        in_gateway_section = False

        # IPv4 pattern: four numbers separated by dots
        ipv4_pattern = r"\d+\.\d+\.\d+\.\d+"

        # Parse output for IPv4 Address, Subnet Mask, and Default Gateway
        for line in output.splitlines():
            line = line.strip()
            # Match IPv4 Address
            if "IPv4 Address" in line:
                match = re.search(ipv4_pattern, line)
                if match:
                    ip_address = match.group(0)
            # Match Subnet Mask
            elif "Subnet Mask" in line:
                match = re.search(ipv4_pattern, line)
                if match:
                    subnet_mask = match.group(0)
            # Check for Default Gateway section
            elif "Default Gateway" in line:
                in_gateway_section = True
                match = re.search(ipv4_pattern, line)
                if match:
                    default_gateway = match.group(0)
            # Check subsequent lines in Default Gateway section
            elif in_gateway_section and line:
                match = re.search(ipv4_pattern, line)
                if match:
                    default_gateway = match.group(0)
                    in_gateway_section = False  # Found IPv4, stop checking

        return ip_address, subnet_mask, default_gateway
    except subprocess.CalledProcessError as e:
        return f"Error getting network info: {e}", "Not found", "Not found"

def monitor_network():
    """Print network information in the specified format."""
    user = get_user()
    machine = get_machine_name()
    ip_address, subnet_mask, default_gateway = get_network_info()
    
    # Print formatted output
    print(f"The user is: {user}")
    print(f"The machine is: {machine}")
    print(f"The IP Address is: {ip_address}")
    print(f"The Subnet Mask is: {subnet_mask}")
    print(f"The Default Gateway is: {default_gateway}")
    print("-----")

def main():
    """Run the monitoring every 5 seconds."""
    #while True:
    #    monitor_network()
    #    time.sleep(5)  # Wait 5 seconds before the next run
    monitor_network()



if __name__ == "__main__":
    main()