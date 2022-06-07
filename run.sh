#!/bin/bash

cd ~
source ./vibe/bin/activate
echo "activated!"
cd ~
cd unicorn-bci-sync/main/
gnome-terminal -- sudo python3 tcp2tobii.py
