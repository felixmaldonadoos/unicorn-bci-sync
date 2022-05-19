#!/bin/bash
gnome-terminal
cd ~
cd Documents/unicorn-bci-sync/
source venv/bin/activate
python3 main/python3 tcp2tobii.py
