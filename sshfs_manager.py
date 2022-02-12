import platform    ## For getting the operating system name
import subprocess  ## For executing a shell command
from dotenv import load_dotenv ## To load variables from .env
import os 
import time

time.sleep(10) ## Sleeping at login helps with Wi-Fi connecting.


## Load variables:

env_path = '/path/to/.env' ## Due to cron/wake executing the task need to use full path instead of os.getcwd().
load_dotenv(dotenv_path=env_path)
host = os.environ['host']
ssh_user = os.environ['ssh_user']
ssh_pass = os.environ['ssh_pass']
path_to_key = os.environ['path_to_key']
server_mount_point = os.environ['server_mount_point']
local_mount_point = os.environ['local_mount_point']
server_and_path = f'{ssh_user}@{host}:{server_mount_point}'
sshfs_options = f'-o IdentityFile={path_to_key}'
connect_command = ['/usr/local/bin/sshfs', server_and_path, local_mount_point, sshfs_options]

## Is host available?

def ping_dum_e(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['/sbin/ping', param, '5', host]
    retry_ping = 0
    while retry_ping <= 2:
        run_ping = subprocess.call(command) == 0

        if run_ping == True:
            retry_ping = 3
            return f'{host} is online'
        else:
            retry_ping += 1
            return f'{host} is down or unreachable'

result_ping = ping_dum_e(host)
print(result_ping)

if result_ping == f'{host} is down':
    exit()

## - Checking if the mount point already exists. Only way to check if SSHFS is still working is looking for a file:

if os.path.exists(f'{local_mount_point}/.is_mounted') == False: ## Needs you to create a file called '.is_mounted' on the server.
    print(f'File does not exist. {host} is not mounted')
    disconnect_command = ['/sbin/umount', local_mount_point]
    disconnect_string = ' '.join(disconnect_command)
    subprocess.run(disconnect_string, shell=True) ## In case connection is stale.
    print('Disconnecting, just in case')
    command_string = ' '.join(connect_command)
    subprocess.run(command_string, shell=True)
    print(f'{host} is now mounted')
else:
    print(f'File exists. {host} is mounted. Nothing to do!')
    exit()
