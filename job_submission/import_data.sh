#!/bin/bash

chmod +x venv_setup.sh
./venv_setup.sh

cd /home/ubuntu/
source /home/ubuntu/venv/bin/activate

time python3 /home/ubuntu/scripts/import.py

deactivate