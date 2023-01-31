import platform    ## - For getting the operating system name
import subprocess  ## - For executing shell commands
import os.path ## - Checking if we can already read the device.
import json ## - Configs are stored as a JSON with name .config.json on the same folder.

def load_environment(server_name): 
    config = open(f'{os.path.abspath(os.path.dirname(__file__))}/.config.json')
    try:
        loaded_config = json.load(config)
    except ValueError as error_loading:
        print(f'Error decoding JSON file!\n{error_loading}')
        exit()
    try:
        loaded_config[server_name][0]['host'], loaded_config[server_name][0]['ssh_user'], loaded_config[server_name][0]['path_to_key'],  loaded_config[server_name][0]['local_mount_point'], loaded_config[server_name][0]['server_mount_point'], loaded_config[server_name][0]['port']
    except KeyError as error:
        print(f'Key not found in .config.json: {error}.\n{server_name} will be skipped.')
        return 'KeyError'
    return loaded_config[server_name][0]['host'], loaded_config[server_name][0]['ssh_user'], loaded_config[server_name][0]['path_to_key'],  loaded_config[server_name][0]['local_mount_point'], loaded_config[server_name][0]['server_mount_point'], loaded_config[server_name][0]['port']

"""
Need to make sure which command was being used to make it truly cross-platforms. 
Does not work with CRON unless paths are specified into the code, through crontab or the profile is loaded.

"""
def check_apps_path():
    ping_check = subprocess.run('/usr/bin/which ping', shell=True, stdout=subprocess.PIPE)
    ping = ping_check.stdout.decode('utf-8').strip()
    sshfs_check = subprocess.run('/usr/bin/which sshfs', shell=True, stdout=subprocess.PIPE)
    sshfs = sshfs_check.stdout.decode('utf-8').strip() 
    umount_check = subprocess.run('/usr/bin/which umount', shell=True, stdout=subprocess.PIPE)
    umount = umount_check.stdout.decode('utf-8').strip()
    if not (ping and sshfs and umount):
        print('Could not find ping, SSHFS or umount automatically. Will assume paths...')
        ping = '/sbin/ping'
        umount = '/sbin/umount'
        sshfs = '/usr/local/bin/sshfs'
    return ping, sshfs, umount

"""
Class to set up the servers. It will require the .config.json to be valid and with the right keys set up.
sshFS.ping() could be disabled from CLI, however, I like to always check not to waste time. Should work in Windows but has not been tested yet.
sshFS.connect() checks for .is_mounted to avoid running the connection if it is already set up and runs a disconnect command in case connection is stale.

"""

class sshFS:
    def __init__(self, host=None, ssh_user=None, path_to_key=None, local_mount_point=None, server_mount_point=None, port=None):
        self.host = host
        self.ssh_user = ssh_user
        self.path_to_key = path_to_key
        self.local_mount_point = local_mount_point
        self.server_mount_point = server_mount_point
        self.port = port

    def ping_server(self, ping):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower()=='windows' else '-c'

        # Building the command. Ex: "ping -c 1 google.com"
        command = [ping, param, '5', self.host]
        retry_ping = 0
        while retry_ping <= 2:
            run_ping = subprocess.call(command, stdout=subprocess.DEVNULL) == 0

            if run_ping == True:
                retry_ping = 3
                return True
            elif run_ping == False:
                retry_ping += 1
                print(f'Retry #:{retry_ping}:')

    def connect(self, sshfs, umount):
        if os.path.exists(f'{self.local_mount_point}/.is_mounted') == False: ## - Needs you to create a file called '.is_mounted' on the server.
            print(f'File does not exist. {self.host} is not mounted')
            disconnect_command = [umount, self.local_mount_point]
            disconnect_string = ' '.join(disconnect_command)
            subprocess.run(disconnect_string, shell=True) ## - In case connection is stale.
            print('Disconnecting, just in case')
            server_and_path = f'{self.ssh_user}@{self.host}:{self.server_mount_point}'
            if self.path_to_key:
                connect_command = [sshfs, server_and_path, self.local_mount_point, '-o', f'IdentityFile={self.path_to_key}', '-p', self.port]
            else: 
                print(f'Missing key in .env_{self.host} file. Cannot connect to server.')
                exit()           
            command_string = ' '.join(connect_command)
            subprocess.run(command_string, shell=True)
            print(f'{self.host} is now mounted')
        else:
            print(f'File exists. {self.host} is mounted. Nothing to do!')




