import sys
from classes.Robot import Robot
import signal

def main(p_almacen, logs):
    """ Funcion que ejecuta el Robot """

    robot = Robot(p_almacen, logs)
    robot.init()

    print("Robot en ejecucion (Ctrl^C para salir)")

    def signal_handler(signal, frame):
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    robot.channel.start_consuming()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Ejecutar de la siguiente forma:\n\n\
              python3 launch_robot.py <p_almacen> <logs>\n\n\
              p_almacen: probabilidad de encontrar un producto (Entre 0 y 100)\n\
              logs: 0 para no imprimirlos y 1 para imprimirlos")

    elif sys.argv[1].isdigit() == False or int(sys.argv[1]) < 0 or int(sys.argv[1]) > 100:
        print("Valor de p_almacen invalido")

    elif int(sys.argv[2]) != 0 and int(sys.argv[2]) != 1:
        print("Valor de logs invalido")

    else:
        p_almacen = int(sys.argv[1])
        logs = False

        if int(sys.argv[2]) == 1:
            logs = True
    
        main(p_almacen, logs)

