import paho.mqtt.client as mqtt
import random
import argparse
import sys
import signal
from IoT.dummy_generic import DummyGeneric

class DummySwitch(DummyGeneric):
    """ Clase DummySwitch, representa un interruptor fisico que puede tomar 
    valores 'ON' y 'OFF'. """

    def __init__(self, id, host, port):
        """ Constructor de la clase DummySwitch. """

        states = ['on', 'off']
        state = random.choice(states)
        self.state = state

        super().__init__(host, port, f'switch{id}')

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
            self.state = command[0]
            # Publicacion de estado cambiado
            message_to_send = f'Default {self.id} --> {self.state}'
        
        self.mqtt_client.publish(self.topic, payload=message_to_send)

    def default_message(self):
        return super().default_message()


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

    parser.add_argument('id',
                        type=int,
                        help='Identificador del sensor')

    args = parser.parse_args()

    print(f'\nArgumentos de entrada: {args}\n')

    try:
        switch = DummySwitch(args.id, args.host, args.port)
        switch.init()

    except Exception:
        print("Pruebe con otro id.")

    # Captura de señal Ctrl^Ĉ
    def signal_handler(signal, frame):
        sys.exit(0) 
    signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    main()