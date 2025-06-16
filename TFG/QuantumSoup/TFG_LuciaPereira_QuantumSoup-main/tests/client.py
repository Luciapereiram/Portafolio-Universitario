import requests
from qiskit import QuantumCircuit
from qiskit.qpy import dump as qpy_dump
import io


def create_quantum_circuit():
    """ Funcion que crea circuito cuantico simple. """

    qc = QuantumCircuit(2, 2)
    qc.h(0)                         # Puerta Hadamard en el primer qubit
    qc.cx(0, 1)                     # Puerta CNOT entre el primer y segundo qubit
    qc.measure([0, 1], [0, 1])      # Medir ambos qubits
    return qc


def send_quantum_circuit_to_server():
    """ Funcion que envia el circuito al servidor de simulacion. """
    
    # Crear el circuito cuántico
    qc = create_quantum_circuit()

    # Serializar el circuito en formato QPY
    qpy_buffer = io.BytesIO()
    qpy_dump(qc, qpy_buffer)
    qpy_data = qpy_buffer.getvalue()

    # URL del servidor Flask
    url = "http://localhost:8080/simulate"

    # Realizar la solicitud POST al servidor Flask
    response = requests.post(url, data=qpy_data)

    # Verificar la respuesta del servidor
    if response.status_code == 200:
        result = response.json()
        print("Resultado de la simulación:", result)
    else:
        print(f"Error al comunicar con el servidor: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    send_quantum_circuit_to_server()



## EJEMPLO CIRCUITO CUANTICO

# from qiskit import QuantumCircuit
# from math import pi

# qc = QuantumCircuit(3)
# # Poner todos los qubits en superposición
# qc.h(0)
# qc.h(1)
# qc.h(2)

# # Enredar el qubit 0 con el qubit 1, y el qubit 1 con el qubit 2
# qc.cx(0, 1)
# qc.cx(1, 2)

# # Aplicar rotaciones alrededor del eje Z
# qc.rz(pi/4, 0)
# qc.rz(pi/2, 1)
# qc.rz(pi, 2)

# # Más enredos
# qc.cx(0, 2)
# qc.cx(1, 0)

# # Medir todos los qubits
# qc.measure_all()




## EJEMPLO CODIGO MALICIOSO

# import os  # Importación no permitida
# os.system("echo Hola mundo")  # Ejecución de comandos del sistema

# def funcion_maliciosa():
#     print("Esto no es un circuito cuántico")  # Uso de funciones no permitido
# funcion_maliciosa()

