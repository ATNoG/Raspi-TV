#!/bin/bash

sleep 40s;
rm -rf ~/.mozilla/
mkdir -p ~/.config
sudo -u pi iceweasel -private http://127.0.0.1:8080/public/ --display=:0 &
sleep 15s;
xte "key F11" -x:0
sleep 5s
xte "key F5" -x:0
