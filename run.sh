#!/bin/bash

cd ~
source ./vibe/bin/activate
echo "activated!"
cd ~
cd unicon-bci-sync/
python main.py
