py_script_path = "python3 /path/to/file"

-- Executing at wake:

watcher = hs.caffeinate.watcher.new(function(eventType)    
    -- screensDidWake, systemDidWake, screensDidUnlock
    if eventType == hs.caffeinate.watcher.systemDidWake then
        hs.notify.new({title="Starting SSHFS Manager!", informativeText="Running PY script"}):send()
        command_to_run = hs.execute(py_script_path, true)
        hs.notify.new({title="SSHFS Manager", informativeText=command_to_run}):send()
    end
end
)


watcher:start()

-- Can also be assigned to a key combination:

hs.hotkey.bindSpec({ { "ctrl", "cmd", "alt"}, "m"},
    function()
        hs.notify.new({title="Starting SSHFS Manager!", informativeText="Running PY script"}):send()
        command_to_run = hs.execute(py_script_path, true)
        hs.notify.new({title="SSHFS Manager", informativeText=command_to_run}):send()
    end
)
