# QuantumSimulator
### Plataforma web que integra un simulador cuántico

## Entorno de desarrollo

### Aplicacion Web

Entorno virtual:

$- python -m venv mi_entorno

$- source mi_entorno/bin/activate

$- pip install -r requirements.txt


Lanzar aplicacion:

$- cd QuantumSoup

$- python manage.py runserver

(Acceder a http://localhost:8000)



### SERVIDOR DE SIMULACIÓN (2 opciones)

Ordenador de la UAM con GPU -> conexión SSH con un usuario con acceso

$- ssh -L 5000:localhost:5000 usuario@maquinaUAM

$- source qenv/bin/activate

$- gunicorn -w 3 -b 0.0.0.0:5000 server:app


Local sin GPU -> contenedores Docker

$- ./run_local.sh

(Acceder a http://localhost:8080


