#!/bin/bash

sleep 45s;
mkdir -p ~/.config
sudo -u pi epiphany-browser -a -i --profile ~/.config http://127.0.0.1:8080/public/ --display=:0 &
sleep 15s;
xte "key F11" -x:0
xte "key F5" -x:0
