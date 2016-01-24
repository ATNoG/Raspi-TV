#!/bin/bash

mkdir -p ~/.config
sudo -u pi epiphany-browser -a -i --profile ~/.config http://localhost:8080/public/ --display=:0 &
sleep 15s;
xte "key F11" -x:0
xte "key F5" -x:0