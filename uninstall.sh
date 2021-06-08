#!/bin/bash

sudo rm /bin/bokbind
sudo rm -rf /usr/lib/bokbind/*
sudo rmdir /usr/lib/bokbind
sudo mv /bin/notify-send-bin /bin/notify-send

echo "Success"
echo -e "You can now remove this folder with \n$ rm -rf $(pwd)*"
