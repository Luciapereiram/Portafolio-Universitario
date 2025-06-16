#!/bin/bash

# Define los comandos para lanzar cada actor del sistema domótico
comandos=(
    "python3 System/controller.py --host test.mosquitto.org"
    "python3 System/bridge.py --host test.mosquitto.org"
    "python3 IoT/dummy_sensor.py --host test.mosquitto.org --interval 50 1" 
    "python3 IoT/dummy_clock.py --host test.mosquitto.org --rate 50 1" 
    "python3 IoT/dummy_switch.py --host test.mosquitto.org 1" 
)

echo "Iniciando sistema domotico..."
for cmd in "${comandos[@]}"; do
    gnome-terminal -- bash -c "$cmd; exec bash" &
done

python3 test_simulator.py
echo "Sistema domotico en marcha"

