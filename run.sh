#!/bin/bash

cd /home/marcb/Documents/Robot
source venv/bin/activate
cd CODE/
python3 app.py &

cd SHUTDOWN/
exec python3 shutdown.py &

wait

