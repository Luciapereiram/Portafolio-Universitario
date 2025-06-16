import paho.mqtt.client as mqtt
from System.rule_engine import RuleEngine
import os
from pickle import Pickler, Unpickler
import argparse
import sys
import signal

class Controller:
    """ Clase Controlador, quien gestiona el sistema en general. """

    def __init__(self, host="redes2.ii.uam.es", port=1883):
        """ Constructor de la clase Controlador. """

        # Conexion al broker
        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Controller")
        self.mqtt_client.connect(host=host, port=port)

        # Instanciar RuleEngine
        self.rule_engine = RuleEngine()

        # Cargar datos del sistema si hubiera
        self.load()


    def init(self):
        """ Funcion que inicializa la recepcion de mensajes en cola. """
        
        # Funcion para los mensajes MQTT recibidos
        self.mqtt_client.on_message = self.on_message

        # Suscripcion a la cola de mensajes de peticion del bot de Discord
        self.mqtt_client.subscribe("redes2/2311/13/discord_request")

        # Conexion permanente al broker
        self.mqtt_client.loop_forever()


    def on_message(self, client, userdata, message):
        """ Funcion que procesa las peticiones del bot de Discord. """

        # Recoger mensaje
        message_str = str(message.payload.decode("utf-8"))
        commands = message_str.split(' ')
        message_to_send = ""
        no_message = False

        print(f'Mensaje recibido --> {message_str}')

        if message.topic == "redes2/2311/13/discord_request":

            # Mensaje de agregar un dispositivo
            if commands[0] == "add_device":
                if self.rule_engine.add_device(f'{commands[1]}{commands[2]}', None):
                    # Suscripcion a la cola de mensajes de dicho dispositivo
                    self.mqtt_client.subscribe(f'redes2/2311/13/iot_response/{commands[1]}{commands[2]}')
                    message_to_send = "Device registered correctly."

                else:
                    message_to_send = "The device is already registered."

            # Mensaje de borrar un dispositivo
            elif commands[0] == 'remove_device':
                if self.rule_engine.remove_device(f'{commands[1]}{commands[2]}'):
                    # Anular suscripcion a la cola de mensajes de dicho dispositivo
                    self.mqtt_client.unsubscribe(f'redes2/2311/13/iot_response/{commands[1]}{commands[2]}')
                    message_to_send = "Device removed correctly."

                else:
                    message_to_send = "The device is not registered in the system."

            # Mensaje de listar dispositivos
            elif commands[0] == "list_devices":
                message_to_send = self.rule_engine.list_devices()

            # Mensaje de recoger estado de dispositivo
            elif commands[0] == "get_state":
                device = f'{commands[1]}{commands[2]}'

                if device in self.rule_engine.devices.keys():
                    # Solicitar el valor del estado del dispositivo
                    self.mqtt_client.publish(topic=f'redes2/2311/13/iot_request/{commands[1]}{commands[2]}', payload=commands[0])
                    no_message = True

                else:
                    message_to_send = "The device is not registered in the system."

            # Mensaje de establecer estado de dispositivo
            elif commands[0] == "set_state":
                device = f'{commands[1]}{commands[2]}'

                if device in self.rule_engine.devices.keys():
                    # Solicitar establecer el valor del estado del dispositivo
                    self.mqtt_client.publish(topic=f'redes2/2311/13/iot_request/{commands[1]}{commands[2]}/set', payload=commands[3])
                    no_message = True

                else:
                    message_to_send = "The device is not registered in the system."

            # Mensaje de agregar regla
            elif commands[0] == 'add_rule':
                if self.rule_engine.add_rule(message_str.split(' ', 1)[1]):
                    message_to_send = "Rule added successfully."

                else:
                    message_to_send = "The rule is already added."
            
            # Mensaje de borrar regla
            elif commands[0] == 'remove_rule':
                if self.rule_engine.remove_rule(message_str.split(' ', 1)[1]):
                    message_to_send = "Rule removed successfully."

                else:
                    message_to_send = "The rule does not exist."

            # Mensaje de listar reglas
            elif commands[0] == "list_rules":
                message_to_send = self.rule_engine.list_rules()

        elif message.topic.rsplit('/', 1)[0] == "redes2/2311/13/iot_response":
            # Mensaje por defecto o tras haber establecido un nuevo estado
            if commands[0] == "Default":
                # Cambiar estado en el registro de dispositivos IoT del sistema
                self.rule_engine.set_device_state(commands[1], commands[3])

                # Comprobar si salta alguna regla
                actions = self.rule_engine.match_rule()

                if len(actions) != 0:
                    # Solicitar establecer el valor de estado de los dispositivos determinados
                    for a in actions:
                        action = a.split(' ')
                        self.mqtt_client.publish(f'redes2/2311/13/iot_request/{action[0]}/set', action[2])
                
            message_to_send = message_str

        # Publicacion de mensaje
        if no_message == False:
            self.mqtt_client.publish(topic="redes2/2311/13/discord_response", payload=message_to_send)


    def stop(self):
        """ Funcion que desconecta al controlador de la cola. """

        self.mqtt_client.disconnect()
        self.save()


    def save(self):
        """ Funcion para persistir los datos en un fichero. """

        print("Guardando los datos del sistema en el fichero...")
        file = open('System/data', 'wb')
        Pickler(file).dump(self.rule_engine)
        file.close()


    def load(self):
        """ Funcion para cargar datos de un fichero. """
        
        if (os.path.isfile('System/data') == False):
            print("No hay fichero de datos, se creara uno nuevo.")

        else:
            print("Cargando datos del fichero...")
            file = open('System/data', 'rb')
            self.rule_engine = Unpickler(file).load()
            # Suscribirse de nuevo a las colas a las que estaba suscrito
            for device in self.rule_engine.devices.keys():
                self.mqtt_client.subscribe(f'redes2/2311/13/iot_response/{device}')
            file.close()

def main():
    """ Funcion que instancia el controlador. """

    parser = argparse.ArgumentParser(description='Conecta con el broker y los dispositivos IoT')

    parser.add_argument('--host',
                        type=str,
                        help='host, por defecto: redes2.ii.uam.es',
                        default='redes2.ii.uam.es')

    parser.add_argument('-p',
                        '--port',
                        type=int,
                        help='puerto, por defecto: 1883',
                        default=1883)

    args = parser.parse_args()

    c = Controller(args.host, args.port)

    def signal_handler(signal, frame):
        c.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    c.init()

if __name__ == '__main__':
    main()