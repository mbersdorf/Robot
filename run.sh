#!/bin/bash

#Zum öffnen der Config-Datei
# sudo nano /etc/systemd/system/robot.service
# run.sh wird ausgeführt sobald network-online.target erreicht ist
# robot.service muss mit folgendem Befehl aktiviert werden:
# sudo systemctl enable robot.service

#Skript um das Programm (app.py) zu starten
cd /home/marcb/Documents/Robot/CODE
source venv/bin/activate
python3 app.py &

# weiteres Skript starten, das auf Shutdown wartet
# Dient zum Herunterfahren des Raspberrys (auch wenn app.py sich aufhängt)
cd SHUTDOWN/
exec python3 shutdown.py &


wait

