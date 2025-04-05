#!/usr/bin/env python3
import os
import random
import string
import socket

# Function to generate a random string of lowercase letters
def random_string(length, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(length))

# Function to generate a random alphanumeric string of length 22
def random_password(length=22):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Function to check if a port is in use
def is_port_in_use(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0  # 0 means the port is in use

# Function to generate and create the .conf file
def create_conf_file(coin_name):
    # Search for the first available port starting from 40001
    port = 40001
    while is_port_in_use(port):
        port += 1

    # Randomly generate rpcuser and rpcpassword
    rpcuser = random_string(8)
    rpcpassword = random_password()

    # Prepare the directory and file path
    conf_dir = f"/root/.{coin_name}"
    conf_file = os.path.join(conf_dir, f"{coin_name}.conf")

    # Ensure the directory exists
    if not os.path.exists(conf_dir):
        os.makedirs(conf_dir)

    # Write the configuration to the .conf file
    with open(conf_file, 'w') as f:
        f.write(f"""rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcthreads=8
rpcallowip=135.181.134.100
rpcallowip=127.0.0.1
maxconnections=24
gen=0
listen=1
server=1
rpcbind=0.0.0.0
port={port}
""")
    
    print(f"{coin_name}.conf has been created at {conf_file} with port {port}")

def main():
    # Ask for the coin name
    coin_name = input("Enter the coin name: ").strip()
    create_conf_file(coin_name)

if __name__ == "__main__":
    main()
