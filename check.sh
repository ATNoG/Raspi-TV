#!/usr/bin/env bash

sleep 30s;
if ! [ "$(pidof iceweasel)" ] || ! [ "$(pidof python)" ]; then
  /sbin/reboot
fi
