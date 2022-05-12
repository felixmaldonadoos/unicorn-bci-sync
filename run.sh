#!/bin/bash

cd ~
source ./vibe/bin/activate
echo "activated!"
cd ~
cd unicorn-bci-sync/main/
gnome-terminal -- python tcp2tobii.py
