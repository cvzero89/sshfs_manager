# sshfs_manager
py script to automatically load a remote mount point over SSHFS.

Required: SSHFS, umount, ping, everything else are standard Python modules. 

A .config.json file is expected to be used on the same directory as the script. Example in the repo.

Can be set up with a @reboot cron to get it to load at startup (it is recommended to also use a sleep as cron is executed early). Ping, SSHFS and umount commands can fail to be looked if CRON environment is not set.

Hammerspoon can monitor for SystemWake to re-connect if mount point disconnects over long periods of time.


## Examples:

### Connecting to a server:

    python3 sshfs-cli.py server_1
    Configuration loaded for server_1...
    server_1 is up!
    File does not exist. server_1 is not mounted
    umount: /local/mount/point/: not currently mounted
    Disconnecting, just in case
    server_1 is now mounted

### Connecting to multiple servers and how it looks when it is already connected:

    python3 sshfs-cli.py server_1,server_2 --sleep 3
    Configuration loaded for server_1...
    server_1 is up!
    File exists. server_1 is mounted. Nothing to do!
    Configuration loaded for server_2...
    server_2 is up!
    File exists. server_2 is mounted. Nothing to do!
    
    
