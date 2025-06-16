import pika
import uuid

#host = 'localhost'
host = 'redes2.ii.uam.es'


class Client:
    """ Clase representante de un cliente del sistema """

    ids = 0

    def __init__(self, id=0, user="", password=""):
        """ Constructor de la clase Cliente """

        self.id = id
        self.user = user
        self.password = password
        self.orders = []

    def __str__(self):
        return f"{self.id} {self.user} {self.password}"

    def init(self):
        """ Funcion que inicializa las colas necesarias para un Cliente """

        # Conexion al broker
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        # Declaracion cola para recibir mensajes del controlador
        queue_name = "2311-13_client_callback_" + str(self.id)

        result = self.channel.queue_declare(
            queue=queue_name, exclusive=True, durable=False, auto_delete=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response,
                                   auto_ack=True)

    def on_response(self, ch, method, props, body):
        """ Funcion que maneja las respuestas del controlador """

        if self.corr_id == props.correlation_id:
            body_txt = body.decode('utf-8')
            response_txt = body_txt.split()

            self.response = response_txt[0]

            # Casos especiales a tratar de las respuestas

            # Caso de error -> mostrar mensaje entero
            if len(response_txt) > 1 and response_txt[1] == "Failed":
                self.response = body_txt

            # Caso de exito y listado de pedidos/productos -> mostrar mensaje entero
            elif response_txt[0] == "LISTED" or response_txt[0] == "PRODUCTS":
                self.response = body_txt

            # Caso de exito y registro -> guardar usuario y contrasenya
            elif response_txt[0] == "REGISTERED":
                self.id = int(response_txt[1])
                self.user = response_txt[2]
                self.password = response_txt[3]

    def register(self, user, password):
        """ Funcion que registra un cliente en el servidor """

        message = f'REGISTER {user} {password}'
        return self.send_message(message=message)

    def log_in(self, user, password):
        """ Funcion que inicia sesion del cliente """

        message = f'LOGIN {self.id} {user} {password}'
        return self.send_message(message=message)

    def make_order(self, products=[]):
        """ Funcion que realiza un pedido del cliente """

        items = ""
        for p in products:
            items += f'{p} '

        message = f'ORDER {self.id} {items}'
        return self.send_message(message=message)

    def cancel_order(self, order_id):
        """ Funcion que cancela un pedido del cliente """

        message = f'CANCEL {self.id} {order_id}'
        return self.send_message(message=message)

    def list_orders(self):
        """ Funcion que lista los pedidos del cliente  """

        message = f'LIST {self.id}'
        return self.send_message(message=message)

    def list_products(self):
        """ Funcion que lista los productos para comprar """

        message = f'PRODUCTS {self.id}'
        return self.send_message(message=message)

    def send_message(self, message):
        """ Funcion para enviar mensaje a la cola client """

        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(exchange='',
                                   routing_key='2311-13_client',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=message
                                   )

        while self.response is None:
            self.connection.process_data_events(time_limit=None)

        return self.response
