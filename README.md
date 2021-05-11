# bokbind
notification wrapper that handles history and blacklist, among other stuff


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

## TODO:
Add normal notification intercept script
