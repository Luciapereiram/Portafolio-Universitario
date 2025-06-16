import unittest
from IoT.dummy_sensor import DummySensor
from IoT.dummy_switch import DummySwitch
import paho.mqtt.client as mqtt
from System.controller import Controller
import threading
from paho.mqtt import MQTTException
import time


class TestController(unittest.TestCase):
    """
        Conecta correctamente con el broker.
        Si no conecta con el broker da error.
        Ante un mensaje de sensor, desencadena el mecanismo para comprobar reglas.
        Ante una respuesta de RuleEngine para realizar una acción, realiza la acción sobre el dispositivo.
        Se lee correctamente la información de los dispositivos de la persistencia.
    """

    host = 'test.mosquitto.org'
    port = 1883

    def init_controller(self):
        """ Inicializa el controlador. """

        self.controller.init()

    def init_devices(self):
        """ Inicializa los dispositivos. """

        self.sen1 = DummySensor(
            id=1, interval=30, min=20, max=30, increment=1, host=self.host, port=self.port)
        self.hilo = threading.Thread(target=self.sen1.init)
        self.hilo.start()

        self.s1 = DummySwitch(id=1, host=self.host, port=self.port)
        self.hilo2 = threading.Thread(target=self.s1.init)
        self.hilo2.start()

    def test_controller(self):
        # Conexion al broker
        try:
            self.controller = Controller(self.host, self.port)
        except MQTTException as e:
            print("Error:", e)

        hilo = threading.Thread(target=self.init_controller)
        hilo.start()

        self.init_devices()

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.connect(self.host, self.port)

        client.publish(f'redes2/2311/13/discord_request',
                       payload="add_device sensor 1")
        client.publish(f'redes2/2311/13/discord_request',
                       payload="add_device switch 1")

        print("\n\nWaiting for everything to run...\n\n")
        time.sleep(5)

        client.publish(f'redes2/2311/13/discord_request',
                       payload="set_state switch 1 off")

        time.sleep(5)
        self.assertEqual(self.s1.state, 'off')

        client.publish(f'redes2/2311/13/discord_request',
                       payload="add_rule if sensor1 == 22 then switch1 = on")

        client.publish(f'redes2/2311/13/discord_request',
                       payload="set_state sensor 1 22")
        time.sleep(5)
        self.assertEqual(self.sen1.state, 22)

        time.sleep(5)
        self.assertEqual(self.s1.state, 'on')

        self.sen1.stop()
        self.s1.stop()
        self.controller.stop()


if __name__ == '__main__':
    unittest.main()
