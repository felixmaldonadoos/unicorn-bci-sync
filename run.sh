#!/bin/bash

cd ~
source ./vibe/bin/activate
echo "activated!"
cd ~
python unicorn-bci-sync/main/app.py
