#!/bin/bash

# Update and install necessary packages
apt update && \
apt install -y \
    curl \
    git \
    python3 \
    python3-venv

# Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
rm get-pip.py

# Copy requirements and install dependencies
if [ -f /tmp/requirements.txt ]; then
    pip install -r /tmp/requirements.txt
fi
