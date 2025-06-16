import socket
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit.qpy import load as qpy_load
import signal
import sys
import io
import os

from flask import Flask, request, jsonify

# Establecer la variable de entorno CUDA_VISIBLE_DEVICES para usar la GPU 0
#os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Esto hará que solo la GPU 0 sea accesible

# Funcion handler para señal Ctrl^C
def signal_handler(sig, frame):
    print("\n[INFO] Cerrando el servidor...")
    sys.exit(0)  # Termina el programa

# Crear el simulador
# simulator = AerSimulator(method='statevector', device='GPU')
simulator = AerSimulator()
app = Flask(__name__)

@app.route('/simulate', methods=['POST'])
def simulate():
    """
    Endpoint para recibir un circuito cuántico en formato QPY y ejecutar la simulación.
    """
    try:
        # Obtener los datos QPY del cuerpo de la solicitud
        qpy_data = request.data
        qpy_buffer = io.BytesIO(qpy_data)

        # Deserializar el circuito
        qc = qpy_load(qpy_buffer)[0]

        # Transpilar y ejecutar
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit).result()
        counts = result.get_counts(qc)

        #hostname = socket.gethostname()
        # Devolver los resultados
        return jsonify({"result": counts})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Manejo de la señal para Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    app.run(host="0.0.0.0", port=5000)
