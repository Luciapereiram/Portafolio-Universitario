import paho.mqtt.client as mqtt
import threading
# Clase generica para dispositivos IoT

class DummyGeneric:
    """ Clase DummyGeneric, una clase padre de la que heredan 
    los dispositivos IoT. """

    def __init__(self, host, port, device_name):
        """ Constructor de la clase DummyGeneric. """
        
        self.id = device_name
        
        # Agregar nuevo dispositivo al conjunto de dispositivos del sistema
        if not self.add_device():
            raise Exception("The device id is already in use.")
        
        # Topic de respuesta 
        self.topic = f'redes2/2311/13/iot_response/{self.id}'

        # Conexion al broker
        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, self.id)
        self.mqtt_client.connect(host=host, port=port)

        # Suscripcion a la cola de mensajes de peticiones del Controller asociadas a su tipo-id
        self.mqtt_client.subscribe(f'redes2/2311/13/iot_request/{self.id}')
        self.mqtt_client.subscribe(f'redes2/2311/13/iot_request/{self.id}/set')

    def init(self):
        """ Funcion que da comienzo a la recepcion de mensajes. """

        # Funcion para los mensajes MQTT recibidos
        self.mqtt_client.on_message = self.on_message

        self.detener_hilo = threading.Event()  # Bandera para detener el hilo de recepción

        # Hilos de ejecucion para enviar el mensaje por defecto
        loop = threading.Thread(target=self.default_message)
        loop.start()
        # Comenzar bucle de recepcion
        self.mqtt_client.loop_forever()

    def on_message(self, client, userdata, message):
        """ Metodo generico con implementacion particular. """
        pass
    
    def default_message(self):
        """ Metodo generico con implementacion particular. """
        pass

    def add_device(self):
        """ Funcion para agregar el reloj instanciado al sistema. """

        with open('IoT/iot_devices.txt', 'r') as fichero:
            lines = fichero.readlines()
            for device in lines:
                if self.id+"\n" == device:
                    print("Error: The device is already in use.")
                    return False 
        
        with open('IoT/iot_devices.txt', 'a') as fichero:
            fichero.write(self.id + "\n")
            print("Device registered correctly.")
            return True

    def remove_device(self):
        """ Funcion para borrar el dispositivo del sistema. """

        found = False

        with open('IoT/iot_devices.txt', 'r') as file:
            lines = file.readlines()
            for device in lines:
                if self.id == device:
                    found = True
                    break
        
        if found == False:
            print("Error: The device is not registered. ")
            return False

        # Sobreescribir fichero
        with open('IoT/iot_devices.txt', 'w') as file:
            for device in lines:
                if not device.startswith(self.id):
                    file.write(device)
        
        print("Device removed correctly.")    
        return True

    def stop(self):
        """ Desconexion del broker. """

        self.mqtt_client.disconnect()