# sshfs_manager
py script to automatically load a remote mount point over SSHFS.


Can be set up with a @reboot cron to get it to load at startup (it is recommended to also use a sleep as cron is executed early).

Hammerspoon can monitor for SystemWake to re-connect if mount point disconnects over long periods of time.
