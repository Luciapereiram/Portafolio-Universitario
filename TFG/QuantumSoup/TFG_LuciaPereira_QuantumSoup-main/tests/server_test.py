import unittest
import requests
import json
import os
import subprocess
import time
import webbrowser
import signal
import sys


class RemoteQuantumSimulationTest(unittest.TestCase):
    QPY_FILE = "circuito.qpy"
    RESULT_FILE = "resultado.json"
    URL = "http://localhost:8080/simulate"
    server_process = None

    @classmethod
    def setup_server(cls):
        """ Inicia el servidor HTTP y maneja la señal de Ctrl^C. """

        print(f"Servidor iniciado en {cls.URL}")

        # Configura el manejo de la señal Ctrl^C (SIGINT)
        signal.signal(signal.SIGINT, cls.handle_signal)

    @classmethod
    def handle_signal(cls, signum, frame):
        """ Maneja la señal Ctrl^C para detener el servidor correctamente. """

        print("\nTest finalizado.")
        sys.exit(0)

    def test_remote_simulation(self):
        """ Ejecuta la simulacion cuantica en el servidor remoto y guarda los resultados. """

        # Verifica que el archivo QPY existe
        self.assertTrue(os.path.exists(self.QPY_FILE),
                        f"Archivo {self.QPY_FILE} no encontrado.")

        with open(self.QPY_FILE, "rb") as f:
            qpy_data = f.read()

        headers = {"Content-Type": "application/octet-stream"}

        try:
            response = requests.post(self.URL, data=qpy_data, headers=headers)
        except requests.exceptions.ConnectionError:
            self.skipTest("No se pudo conectar al servidor.")
            return

        # Verifica que el servidor responde correctamente
        self.assertEqual(response.status_code, 200,
                         f"Error en el servidor: {response.status_code}\n{response.text}")

        try:
            json_data = response.json()
        except json.JSONDecodeError:
            self.fail("La respuesta del servidor no es un JSON válido.")

        # Verifica que la clave 'result' esta en la respuesta
        self.assertIn("result", json_data,
                      "La respuesta no contiene la clave 'result'.")

        # Guarda el resultado
        with open(self.RESULT_FILE, "w") as f:
            json.dump(json_data, f, indent=4)

        print(f"Simulación exitosa. Resultado guardado en {self.RESULT_FILE}")

    @classmethod
    def tearDownClass(cls):
        """ (Despues de los tests) Inicia el servidor web y abre index.html en el navegador. """

        # Lanza index.html en el navegador
        cls.server_process = subprocess.Popen(
            ["python3", "-m", "http.server", "5000"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        time.sleep(2)

        # Abre index.html en el navegador
        webbrowser.open("http://localhost:5000/index.html")

        # Servidor corriendo hasta que el usuario interrumpa (Ctrl+C)
        input("Presiona Enter para detener el test...")
        cls.handle_signal(None, None)


if __name__ == "__main__":
    unittest.main()
