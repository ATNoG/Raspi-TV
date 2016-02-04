#!/usr/bin/env bash

if ! [ "$(pidof iceweasel)" ] || ! [ "$(pidof python)" ]; then
  /sbin/reboot
fi
