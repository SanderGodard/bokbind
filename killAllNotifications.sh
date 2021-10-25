#!/bin/bash

#dbus-monitor "interface='org.freedesktop.Notifications'" | grep --line-buffered "member=Notify" | sed -u -e 's/.*/killall notify-osd/g' | bash
#dbus-monitor "interface='org.freedesktop.Notifications'" | grep --line-buffered "member=Notify" | sed -u -e 's/.*/killall dunst/g' | bash

killall -SIGUSR1 dunst # pause
