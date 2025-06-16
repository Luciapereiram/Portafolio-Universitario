import sys
import signal
from classes.Controller import Controller

def main(logs):
    """ Funcion que ejecuta el Controlador """

    controlador = Controller(logs)
    controlador.load()
    controlador.init()

    print("Controlador en ejecucion (Ctrl^C para salir)")

    def signal_handler(signal, frame):
        controlador.save()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    print("\nAtendiendo clientes...\n")
    controlador.channel.start_consuming()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Ejecutar de la siguiente forma:\n\n\
              python3 launch_controller.py <logs> (logs: 0 para no imprimirlos y 1 para imprimirlos)")

    elif int(sys.argv[1]) != 0 and int(sys.argv[1]) != 1:
        print("Valor de logs invalido")

    else:
        logs = False

        if int(sys.argv[1]) == 1:
            logs = True

        main(logs)