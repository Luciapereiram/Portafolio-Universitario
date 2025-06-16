import pika
import time
import random

#host = 'localhost'
host = 'redes2.ii.uam.es'

class Robot:
    """ Clase representante de un robot del sistema """
    
    ids = 0

    def __init__(self, p_almacen, logs):
        """ Constructor de la clase Robot """

        # Para imprimir logs de las colas
        self.logs = logs

        self.id = Robot.ids
        Robot.ids += 1
        self.p_almacen = p_almacen

    def init(self):
        """ Funcion que inicializa las colas necesarias para Robot """
        
        # Conexion al broker
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        # Declaracion cola para peticiones del controlador
        self.channel.queue_declare(queue='2311-13_robot', durable=False, auto_delete=True)

        # Consumir mensajes
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='2311-13_robot', on_message_callback=self.callback)
        
        # Declaracion cola para enviar respuestas
        self.channel.queue_declare(queue='2311-13_robot_callback', durable=False, auto_delete=True)


    def callback(self, ch, method, props, body):
        """ Funcion que maneja las peticiones del controlador """

        request_txt = body.decode('utf-8')
        request = request_txt.split()

        if self.logs == True:
            request_string = ""
            for r in request:
                request_string += f'{r} '
            print("Peticion controlador ->", request_string)

        # Simulacion de busqueda del producto en almacen
        time.sleep(random.randint(5, 10))

        random_num = random.randint(1, 100)
        if random_num in range(1, (self.p_almacen + 1)):
            response = f'FOUND {request[1]} {request[2]} {request[3]}'
        else:
            response = f'NOT-FOUND {request[1]}'

        # Generar respuesta
        ch.basic_publish(exchange='',
                     routing_key="2311-13_robot_callback",
                     body=response)
        
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __str__(self):
        return f""
