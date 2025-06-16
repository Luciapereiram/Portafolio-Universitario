import pika
import time
import random

#host = 'localhost'
host = 'redes2.ii.uam.es'

class Dealer:
    """ Clase representante de un repartidor del sistema """
    
    ids = 0

    def __init__(self, p_entrega, logs):
        """ Constructor de la clase Repartidor """
        
        # Para imprimir logs de las colas
        self.logs = logs

        self.id = Dealer.ids
        Dealer.ids += 1
        self.p_entrega = p_entrega

    def init(self):
        """ Funcion que inicializa las colas necesarias para Dealer """
        
        # Conexion al broker
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        # Declaracion cola para peticiones del controlador
        self.channel.queue_declare(queue='2311-13_dealer', durable=False, auto_delete=True)

        # Consumir mensajes
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='2311-13_dealer', on_message_callback=self.callback)
        
        # Declaracion cola para enviar respuestas
        self.channel.queue_declare(queue='2311-13_dealer_callback', durable=False, auto_delete=True)

    def callback(self, ch, method, props, body):
        """ Funcion que maneja las peticiones del controlador """

        request_txt = body.decode('utf-8')
        request = request_txt.split()

        if self.logs == True:
            request_string = ""
            for r in request:
                request_string += f'{r} '
            print("Peticion controlador ->", request_string)

        # Informar de que el pedido esta en reparto
        response = f'ON-DELIVERY {request[1]}'

        ch.basic_publish(exchange='',
                     routing_key="2311-13_dealer_callback",
                     properties=pika.BasicProperties(correlation_id = props.correlation_id), body=response)
        
        # Simulacion de intento de entrega
        time.sleep(random.randint(10, 20))

        random_num = random.randint(1, 100)
        if random_num in range(1, (self.p_entrega + 1)):
            response = f'DELIVERED {request[1]}'
        else:
            response = f'FAILED-DELIVERY {request[1]}'

        # Generar respuesta
        ch.basic_publish(exchange='',
                     routing_key="2311-13_dealer_callback",
                     body=response)
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
