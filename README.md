# bokbind

Notification wrapper that handles history and blacklist, among other stuff
Mute notifications function is for now reliant on you using dunst as a notification display daemon

## Installation
Run the `install.sh` script
Then just add `exec /usr/lib/bokbind/magnifyingGlass.py &` to your startup config



## Polybar module
```ini
[module/notif]
type = custom/script
inherit = section/base
interval = 10
click-left = bokbind notify
click-middle = bokbind clear
click-right = bokbind toggle
exec = bokbind amount
```

Then you just add `notif` to your modules list


## TODO (somewhat outdated):
Add normal notification intercept script
Send all notifications from script
Stop all others
