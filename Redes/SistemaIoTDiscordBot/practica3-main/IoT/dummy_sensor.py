import paho.mqtt.client as mqtt
import random
import time
import argparse
import sys
import signal
from IoT.dummy_generic import DummyGeneric

class DummySensor(DummyGeneric):
    """ Clase DummySensor, representa un sensor fisico que puede tomar 
    valores numericos entre un minimo y maximo. """

    def __init__(self, id, interval, min, max, increment, host, port):
        """ Constructor de la clase DummySensor. """

        self.interval = interval
        self.min = min
        self.max = max
        self.increment = increment
        self.state = random.randint(self.min, self.max)

        super().__init__(host, port, f'sensor{id}')

        self.mqtt_client.publish(self.topic, payload=f'Default {self.id} --> {self.state}')
            


    def on_message(self, client, userdata, message):
        """ Funcion para enviar o cambiar el estado del dispositivo, segun lo solicitado. """

        message_str = str(message.payload.decode("utf-8"))
        command = message_str.split(' ')
        message_to_send = ""

        print(f'Mensaje recibido -> {message_str}')
        
        if command[0] == "get_state":
            message_to_send = f'{self.id} --> Current state: {self.state}'

        elif message.topic == f'redes2/2311/13/iot_request/{self.id}/set':
            new_state = int(command[0])
            if new_state < self.min or new_state > self.max:
                message_to_send = f'{self.id} --> New state must be smaller than {self.min} and greater than {self.max}'
            else:
                self.state = new_state
                # Publicacion de estado cambiado
                message_to_send = f'Default {self.id} --> {self.state}'
        
        self.mqtt_client.publish(self.topic, payload=message_to_send)


    def default_message(self):
        """ Funcion que envia el mensaje por defecto del reloj cada cierto tiempo. """

        while True:
            time.sleep(self.interval)

            # Sumar el incremento y si se pasa del valor maximo, 
            # volver al valor minimo y seguir sumando
            new_state = self.state
            new_state += self.increment

            if new_state > self.max:
                self.state = self.min + (new_state - self.max)

            else:
                self.state = new_state
            
            # Publicacion de estado cambiado
            self.mqtt_client.publish(self.topic, payload=f'Default {self.id} --> {self.state}')


def main():
    """ Ejecutable que instancia un sensor y envia cambios de estado 
    cada cierto tiempo. """

    parser = argparse.ArgumentParser(description='Instancia un sensor')

    parser.add_argument('--host',
                        type=str,
                        help='Host, por defecto: redes2.ii.uam.es',
                        default='redes2.ii.uam.es')

    parser.add_argument('--port',
                        type=int,
                        help='Puerto, por defecto: 1883',
                        default=1883)

    parser.add_argument('--interval',
                        type=int,
                        help=('Tiempo entre envios, por defecto: 1 seg'),
                        default=1)

    parser.add_argument('--min',
                        type=int,
                        help=('Valor minimo de temperatura, por defecto: 20º'),
                        default=20)

    parser.add_argument('--max',
                        type=int,
                        help=('Valor maximo de temperatura, por defecto: 30º'),
                        default=30)
    
    parser.add_argument('--increment',
                        type=int,
                        help=('Incremento entre min y max, por defecto: 1'),
                        default=1)

    parser.add_argument('id',
                        type=int,
                        help='Identificador del sensor')

    args = parser.parse_args()

    print(f'\nArgumentos de entrada: {args}\n')

    try:
        sensor = DummySensor(args.id, args.interval, args.min, args.max, args.increment, args.host, args.port)
        sensor.init()

    except Exception:
        print("Pruebe con otro id.")

    # Captura de señal Ctrl^Ĉ
    def signal_handler(signal, frame):
        sys.exit(0) 
    signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    main()

