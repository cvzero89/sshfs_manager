import argparse
from sshfs import *

parser =  argparse.ArgumentParser(description='Manage SSHFS mount points')
parser.add_argument('server_name', help='Server to manage, multiple servers can be accepted separated by comma. Will load settings from .config.json.')
parser.add_argument('--sleep', help='May be required for startup crons, will only accept integers.', type=int)
args = parser.parse_args()
sleep_timer = args.sleep
servers = args.server_name.split(',')

"""
Sleep is used for crons. CRON might run earlier than the network being set up resulting in a bad ping.
If CRON is used check_apps_path() might fail, defaulting to the OSX standard paths.
"""

ping, sshfs, umount = check_apps_path()

if sleep_timer is None:
	pass
else:
	import time
	time.sleep(sleep_timer)

for server_name in servers:
	loaded_config = []
	loaded_config = load_environment(server_name)
	if ''.join(loaded_config) == 'KeyError':
		continue
	print(f'Configuration loaded for {server_name}...')
	server_name = sshFS(*loaded_config)
	if server_name.ping_server(ping) == True:
		print(f'{server_name.host} is up!')
		server_name.connect(sshfs, umount) 
	else:
		print(f'{server_name.host} is down or unreacheable!')
		exit()



