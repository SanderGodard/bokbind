#!/bin/bash
sudo mkdir /usr/lib/bokbind/
sudo cp -r * /usr/lib/bokbind/.
cd /usr/lib/bokbind/

sudo ln -s $(pwd)/bokbind.py /bin/bokbind
sudo mv /bin/notify-send /bin/notify-send-bin
sudo cp /bin/notify-send-bin notify-send.bak
sudo cp notify-send-replacement /bin/notify-send

echo "Success"
echo -e "Add \nexec $(pwd)/magnifyingGlass.py &\n to your computer startup file"
cd -
