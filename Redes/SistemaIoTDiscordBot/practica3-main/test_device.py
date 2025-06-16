import unittest
from IoT.dummy_switch import DummySwitch
from IoT.dummy_sensor import DummySensor
import paho.mqtt.client as mqtt
import time
import threading


class TestDevice(unittest.TestCase):
    """
        Conecta correctamente con el broker.
        Si no conecta con el broker da error.
        Probar que el sistema lee bien los parametros por linea de comandos.
        (switch) Cambia de estado ante una accion.
        (sensor) Cambia de estado en intervalos entre min y max.
    """

    host = 'test.mosquitto.org'
    port = 1883
    
    def init_devices(self):
        """ Inicializa dispositivos. """

        self.sen1 = DummySensor(
            id=1, interval=30, min=20, max=30, increment=1, host=self.host, port=self.port)
        self.hilo = threading.Thread(target=self.sen1.init)
        self.hilo.start()

        self.s1 = DummySwitch(id=1, host=self.host, port=self.port)
        self.hilo2 = threading.Thread(target=self.s1.init)
        self.hilo2.start()

    def on_message(self, client, userdata, message):
        """ Comprueba los estados del sensor1. """

        msg = str(message.payload.decode("utf-8"))
        state = msg.split(' ')[2]

        valores_state = range(20, 30)
        self.assertIn(int(state), valores_state)

    def test_device(self):

        self.init_devices()

        # SWITCH

        self.assertEqual(self.s1.id, 'switch1')

        valores_state = ['on', 'off']
        self.assertIn(self.s1.state, valores_state)

        estado_actual = self.s1.state

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.connect(self.host, self.port)
        client.on_message = self.on_message
        
        print("\n\nWaiting for everything to run...\n\n")
        
        if estado_actual == 'on':
            client.publish(f'redes2/2311/13/iot_request/{self.s1.id}/set', payload=f"off")
            time.sleep(5)
            self.assertEqual(self.s1.state, 'off')

        elif estado_actual == 'off':
            client.publish(f'redes2/2311/13/iot_request/{self.s1.id}/set', payload=f"on")
            time.sleep(5)
            self.assertEqual(self.s1.state, 'on')


        # SENSOR

        self.assertEqual(self.sen1.id, "sensor1")

        valores_state = range(20, 30)
        self.assertIn(self.sen1.state, valores_state)

        client.loop_start()
        client.subscribe(f'redes2/2311/13/iot_response/{self.sen1.id}')
        time.sleep(5)
        client.loop_stop()

        self.s1.stop()
        self.sen1.stop()


if __name__ == '__main__':
    unittest.main()
