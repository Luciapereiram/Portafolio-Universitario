import paho.mqtt.client as mqtt
import time
import datetime
import argparse
import sys
import signal
from IoT.dummy_generic import DummyGeneric

class DummyClock(DummyGeneric):
    """ Clase DummyClock, representa un reloj fisico que puede tomar 
    valores de hora con el formato HH:MM:SS. """

    def __init__(self, id, time, increment, rate, host, port):
        """ Constructor de la clase DummyClock. 

            Argumentos de entrada:
            - id: un entero que sirve como identificador
            - time: hora de inicio (por defecto la hora actual)
            - increment: incremento en segundos entre envios (por defecto 1)
            - rate: frecuencia de mensajes por segundo (por defecto 1) 
        """
        
        self.time = time
        self.rate = rate
        self.increment = increment
        
        super().__init__(host, port, f'clock{id}')
        
        self.mqtt_client.publish(self.topic, payload=f'Default {self.id} --> {self.time.strftime("%H:%M:%S")}')


    def on_message(self, client, userdata, message):
        """ Funcion para enviar o cambiar el estado del dispositivo, segun lo solicitado. """

        message_str = str(message.payload.decode("utf-8"))
        command = message_str.split(' ')
        message_to_send = ""

        print(f'Mensaje recibido -> {message_str}')

        if command[0] == "get_state":
            message_to_send = f'{self.id} --> Current state: {self.time.strftime("%H:%M:%S")}'

        elif message.topic == f'redes2/2311/13/iot_request/{self.id}/set':
            self.time = datetime.datetime.strptime(command[0], '%H:%M:%S')
            # Publicacion de estado cambiado
            message_to_send = f'Default {self.id} --> {self.time.strftime("%H:%M:%S")}'
        
        self.mqtt_client.publish(self.topic, payload=message_to_send)

        
    def default_message(self):
        """ Funcion que envia el mensaje por defecto del reloj cada cierto tiempo. """

        while True:
            time.sleep(self.rate)
            self.time += datetime.timedelta(seconds=self.increment)
            # Publicacion de estado cambiado
            self.mqtt_client.publish(self.topic, payload=f'Default {self.id} --> {self.time.strftime("%H:%M:%S")}')


def main():
    """ Funcion que instancia un reloj. """

    parser = argparse.ArgumentParser(description='Instancia un reloj')

    parser.add_argument('--host',
                        type=str,
                        help='Host, por defecto: redes2.ii.uam.es',
                        default='redes2.ii.uam.es')

    parser.add_argument('--port',
                        type=int,
                        help='Puerto, por defecto: 1883',
                        default=1883)

    parser.add_argument('--time',
                        type=str,
                        help=('Hora de inicio, por defecto: hora actual. '
                              'Formato: HH:MM:SS'),
                        default=datetime.datetime.now().strftime('%H:%M:%S'))

    parser.add_argument('--increment',
                        type=int,
                        help=('Incremento entre envíos en segundos, '
                              'por defecto: 1 segundo'),
                        default=1)

    parser.add_argument('--rate',
                        type=int,
                        help=('Frecuencia de envío en segundos, '
                              'por defecto: 1 mensaje'),
                        default=1)

    parser.add_argument('id',
                        type=int,
                        help='Identificador del reloj')

    args = parser.parse_args()

    print(f'\nArgumentos de entrada: {args}\n')

    try:
        fecha_dt = datetime.datetime.strptime(args.time, '%H:%M:%S')
    except ValueError:
        print("Fecha invalida, formato --> HH:MM:SS")

    try:
        clock = DummyClock(args.id, fecha_dt, args.increment, args.rate, args.host, args.port)
        clock.init()

    except Exception:
        print("Pruebe con otro id.")

    # Captura de señal Ctrl^Ĉ
    def signal_handler(signal, frame):
        sys.exit(0) 
    signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    main()