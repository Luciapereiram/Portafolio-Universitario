#!/bin/bash

# Ruta del directorio donde se encuentran los archivos
directorio="/home/lucia/TERCERO/gitlab/practica3"

# Borrar los archivos existentes
rm -f "$directorio/System/system_rules.txt" "$directorio/System/data" "$directorio/IoT/iot_devices.txt"

# Crear los archivos nuevamente
touch "$directorio/System/system_rules.txt" "$directorio/IoT/iot_devices.txt"
