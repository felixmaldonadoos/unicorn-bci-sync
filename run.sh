#!/bin/bash

cd ~
source ./vibe/bin/activate
echo "activated!"
cd ~
cd unicorn-bci-sync/main/
python app.py
