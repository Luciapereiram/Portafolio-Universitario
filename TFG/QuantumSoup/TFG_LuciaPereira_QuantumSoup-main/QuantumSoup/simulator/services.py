from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt
import base64
from matplotlib import pyplot as plt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from qiskit.qpy import dump as qpy_dump
import io
from simulator.code_validator import validate_code
import requests
from qiskit import QuantumCircuit
from django.conf import settings

import matplotlib
matplotlib.use('Agg')  # Forzar el uso del backend 'Agg'


##############################################################
#                                                            #
#       Conexion al servidor de simulacion.                  #
#                                                            #
#       1. Recibe peticion de codigo                         #
#       2. Comprueba seguridad                               #
#       3. Genera circuito                                   #
#       4. Envia al simulador                                #
#       5. Recibe resultados                                 #
#                                                            #
##############################################################

blacklist = ["sys", "os", "subprocess", "eval", "exec"]


@api_view(['POST'])
def exec_simulation(request):

    # Extraer codigo de la peticion
    quantum_code = request.data.get('code', '')

    if not quantum_code:
        return Response({"error": "No se proporcionó código cuántico."}, status=400)

    # Validar seguridad del codigo
    validation, message = validate_code(quantum_code, blacklist)

    if validation is False:
        return Response({"error": "El código no es seguro y no puede ejecutarse."}, status=400)

    # Verificar sintaxis antes de ejecutar
    try:
        compile(quantum_code, "<string>", "exec")
    except SyntaxError as e:
        return Response({"error": f"Sintaxis inválida: {e}"}, status=400)

    # Crear circuito para enviar al simulador
    try:
        local_namespace = {}
        exec(quantum_code, {}, local_namespace)

        if 'qc' not in local_namespace:
            return Response({"error": "El código introducido no define ningún circuito cuántico (debe existir una variable llamada `qc`)."}, status=400)

        qc = local_namespace['qc']

        if not isinstance(qc, QuantumCircuit):
            return Response({"error": "La variable 'qc' no es un circuito cuántico válido."}, status=400)

        if qc.num_qubits == 0:
            return Response({
                "error": "El circuito no contiene qubits. Usa 'QuantumCircuit(n)' con al menos un qubit."
            }, status=400)
        
        # Verificar que el circuito tiene medidas
        if not any(instr[0].name == "measure" for instr in qc.data):
            return Response({
                "error": "El circuito no contiene instrucciones de medida. Añade 'qc.measure(...)' para poder obtener resultados."
            }, status=400)

        # Serializar circuito en QPY
        qpy_buffer = io.BytesIO()
        qpy_dump(qc, qpy_buffer)
        qpy_data = qpy_buffer.getvalue()

        # Enviar al simulador
        try:
            response = requests.post(settings.SIMULATOR_URL, data=qpy_data)
        except requests.ConnectionError:
            return Response({"error": "No se pudo conectar al servidor de simulación. Intenta más tarde."}, status=500)
        except requests.RequestException as e:
            return Response({"error": f"Error al comunicarse con el servidor: {e}"}, status=500)

        print(response)
        try:
            response_data = response.json()
        except ValueError:
            return Response({"error": "El servidor no devolvió una respuesta válida."}, status=500)

        print(response_data)
        # Verificar respuesta del simulador
        if response.status_code != 200:
            return Response({"error": response_data.get("error", "El servidor no ha podido procesar el circuito. Por favor, vuelve a intentarlo.")}, status=500)

        return Response(response_data)

    except NameError:
        return Response({"error": "El código contiene referencias a variables no definidas. Revisa que todas las variables estén declaradas."}, status=400)

    except ConnectionRefusedError:
        print("[ERROR] No se pudo conectar al servidor.")
        return Response({"error": "Error de conexión. No se pudo conectar al servidor de simulación."}, status=500)

    except TypeError:
        return Response({"error": "Se produjo un error de tipos en el código. Verifica los datos que estás usando."}, status=400)

    except Exception as e:
        # Manejo de cualquier otra excepcion
        print(f"[ERROR] Ocurrió un error inesperado: {e}")
        return Response({"error": f"Ocurrió un error inesperado: {e}"}, status=500)


@api_view(['POST'])
def draw_circuit_view(request):
    quantum_code = request.data.get('code', '')

    if not quantum_code:
        return Response({"error": "No se proporcionó código cuántico."}, status=400)

    validation, message = validate_code(quantum_code, blacklist)

    if not validation:
        return Response({"error": "El código no es seguro y no puede ejecutarse."}, status=400)
    
    # Verificar sintaxis antes de ejecutar
    try:
        compile(quantum_code, "<string>", "exec")
    except SyntaxError as e:
        return Response({"error": f"Sintaxis inválida: {e}"}, status=400)

    try:
        local_namespace = {}
        exec(quantum_code, {}, local_namespace)

        if 'qc' not in local_namespace:
            return Response({"error": "El código introducido no define ningún circuito cuántico (debe existir una variable llamada `qc`)."}, status=400)

        qc = local_namespace['qc']

        # Generar imagen del circuito
        img_buf = io.BytesIO()
        try:
            circuit_drawer(qc, output='mpl')
            plt.savefig(img_buf, format='png', bbox_inches='tight')
            plt.close()
        except Exception as e:
            # Captura cualquier error relacionado con la generación de la imagen
            return Response({"error": f"Error al generar la imagen del circuito: {str(e)}"}, status=500)

        img_buf.seek(0)

        img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')
        return Response({"circuit_image": img_base64})

    except SyntaxError:
        return Response({"error": "El código contiene errores de sintaxis."}, status=400)

    except NameError:
        return Response({"error": "El código usa nombres de variables no definidos."}, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
