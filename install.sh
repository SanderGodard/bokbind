#!/bin/bash
sudo mkdir /usr/lib/bokbind/
sudo cp * /usr/lib/bokbind/.
sudo cd /usr/lib/bokbind/

sudo ln -s bokbind.py /bin/bokbind
sudo mv /bin/notify-send /bin/notify-send-bin
sudo cp /bin/notify-send-bin notify-send.bak
sudo cp notify-send-replacement /bin/notify-send

echo -e "Add \n$(pwd)/readnotif &\n to your computer startup file"
