import discord
import paho.mqtt.client as mqtt
import threading
import asyncio
import re
import argparse
import sys
import signal

class Bridge:
    """ Clase Bridge, quien crea y maneja la conexion entre el controlador 
    y la API de Discord. """

    def __init__(self, host, port):
        """ Constructor de la clase Bridge. """

        # Token del bot de Discord
        self.token = "MTIzNDE4NzI3MzEyNjQxNjQ2NA.GZaeVO.8Ay2EbphRMwnTka92jUqwfUZ7HRwW8GO8IC43Y"

        # Conexion al broker
        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Bridge")
        self.mqtt_client.connect(host=host, port=port)

        intents = discord.Intents.default()
        intents.message_content = True
        # Instanciar cliente de discord
        self.discord_client = discord.Client(intents=intents)
        self.state = 'OFF'

        @self.discord_client.event
        async def on_ready():
            """ Funcion que inicializa el bot. """

            self.state = 'ON'
            print("Bot is ready")

        @self.discord_client.event
        async def on_message(message):
            """ Funcion para procesar los mensajes recibidos. """

            # Rechazar mensajes de si mismo
            if message.author == self.discord_client.user:
                return

            print(f'\n{message.author} -> {message.content}\n')

            # Recoger el canal
            self.channel = message.channel

            # Validar mensaje
            message_to_send = self.message_validation(message.content)

            if message.content.startswith("IoT help"):
                await self.channel.send("""
                                            Welcome to the command guide for our Discord bot! Below you will find a list of available commands that you can use to interact with the bot and control IoT devices.

                                            IoT help
                                            IoT add_rule  <rule>
                                            IoT remove_rule  <rule>
                                            IoT list_rules
                                            IoT add_device  <device_type>  <device_id>
                                            IoT remove_device  <device_type>  <device_id>
                                            IoT list_devices
                                            IoT set_state  <device_type>  <device_id>  <state>
                                            IoT get_state  <device_type>  <device_id> 
                                            """)

            elif message.content.startswith("IoT") and message_to_send != "error":
                # Enviar el mensaje MQTT al controlador
                self.mqtt_client.publish(
                    "redes2/2311/13/discord_request", message_to_send)

            else:
                await message.channel.send("Invalid command. Use 'IoT help' to see the list of commands.")


    def init(self):
        """ Funcion que inicializa la recepcion de mensajes en cola. """

        self.mqtt_client.on_message = self.on_mqtt_message

        # Suscripcion a la cola de mensajes de respuesta del Controller
        self.mqtt_client.subscribe("redes2/2311/13/discord_response")

        # Comenzar bucle de recepcion
        loop = threading.Thread(target=self.mqtt_client.loop_forever)
        loop.start()

        # Ejecucion del bot
        self.discord_client.run(self.token)


    def on_mqtt_message(self, client, userdata, message):
        """ Funcion que procesa las respuestas del Controller. """

        response = str(message.payload.decode("utf-8"))
        print("Respuesta del controlador: ", response)

        # (Se envia desde hilo externo a hilo principal)
        asyncio.run_coroutine_threadsafe(
            self.send_to_discord(response), self.discord_client.loop)


    async def send_to_discord(self, message):
        """ Funcion asincrona para enviar mensajes a Discord. """

        try:
            await self.channel.send(message)
        except Exception as e:
            print(e)


    def message_validation(self, message):
        """ Funcion que valida el formato de los mensajes recibidos del bot de Discord. """

        command = str(message).split(' ')
        message_to_send = ""

        if len(command) < 2:
            message_to_send = "error"

        # Mensaje de listar elementos
        elif command[1] == "list_devices" or command[1] == "list_rules":
            message_to_send = command[1]

        # Mensaje de agregar/eliminar dispositivo o recoger estado de dispositivo
        elif command[1] == "add_device" or command[1] == "remove_device" or command[1] == "get_state":
            # Se requieren cuatro argumentos
            if len(command) < 4:
                message_to_send = "error"

            else:
                # Comprobar que el id del dispositivo es valido
                if self.is_a_device(command[2]):
                    message_to_send = f'{command[1]} {command[2]} {command[3]}'

                else:
                    message_to_send = "error"

        # Mensaje de establecer estado de dispositivo
        elif command[1] == "set_state":
            # Se requieren cinco argumentos
            if len(command) < 5:
                message_to_send = "error"

            else:
                # Comprobar que el id del dispositivo es valido
                if self.is_a_device(command[2]):
                    if self.is_a_device_state(command[2], command[4]):
                        message_to_send = f'{command[1]} {command[2]} {command[3]} {command[4]}'

                else:
                    message_to_send = "error"

        # Mensaje de agregar/eliminar reglas
        elif command[1] == "add_rule" or command[1] == "remove_rule":
            # Comprobar que el formato de la regla es valido
            rule = str(message).split(' ', 2)[2]

            if self.is_a_valid_rule(rule):
                message_to_send = f'{command[1]} {rule}'
            
            else:
                message_to_send = "error"
            

        else:
            message_to_send = "error"

        return message_to_send


    def is_a_device(self, device_type):
        """ Funcion que comprueba si el tipo del dispositivo es valido. """

        pattern = re.compile("^(clock|sensor|switch)$")

        return pattern.match(device_type)


    def is_a_device_state(self, device_type, device_state):
        """ Funcion que comprueba si el estado del dispositivo es valido. """

        if device_type == "switch":
            pattern = re.compile("^(ON|OFF)$")
            return pattern.match(device_state)

        elif device_type == "clock":
            pattern = re.compile("^(2[0-3]|[0-1][0-9]):[0-5][0-9]:[0-5][0-9]$")
            return pattern.match(device_state)

        elif device_type == "sensor":
            pattern = re.compile("^-?\d+$")
            return pattern.match(device_state)


    def is_a_valid_rule(self, rule):
        """ Funcion que comprueba que el formato de la regla es valido. """

        pattern = re.compile("^if (clock[0-9]+ (==|!=|>|<|>=|<=|=>|=<) (2[0-3]|[0-1][0-9]):[0-5][0-9]:[0-5][0-9]|sensor[0-9]+ (==|!=|>|<|>=|<=|=>|=<) -?\d+|switch[0-9]+ (==|!=) (on|off)) ((or |and )(clock[0-9]+ (==|!=|>|<|>=|<=|=>|=<) (2[0-3]|[0-1][0-9]):[0-5][0-9]:[0-5][0-9]|sensor[0-9]+ (==|!=|>|<|>=|<=|=>|=<) -?\d+|switch[0-9]+ (==|!=) (on|off)) )*then (clock[0-9]+ = (2[0-3]|[0-1][0-9]):[0-5][0-9]:[0-5][0-9]|sensor[0-9]+ = -?\d+|switch[0-9]+ = (on|off))$")
        
        return pattern.match(rule)

        # Mensajes deben tener un formato determinado. Debe coincidir con los nombres
        # de dispositivos y nombres de parametros (ON/OFF, horas...)o con un formato de regla valido.

        # Comandos:
        # - IoT help (info para comandos)
        # - IoT add_rule <rule>
        # - IoT remove_rule <rule>
        # - IoT list_rules
        # - IoT add_device <device_id>
        # - IoT remove_device <device_id>
        # - IoT list_devices
        # - IoT get_state <device_id>
        # - IoT set_state <device_id> <state>

    def stop(self):
        """ Funcion que desconecta al controlador de la cola. """

        self.mqtt_client.disconnect()

def main():
    """ Funcion que instancia el puente de conexion con Discord. """

    parser = argparse.ArgumentParser(description='Conecta con el controlador y el bot de Discord')

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

    b = Bridge(args.host, args.port)
    
    def signal_handler(signal, frame):
        b.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    
    b.init()

if __name__ == '__main__':
    main()