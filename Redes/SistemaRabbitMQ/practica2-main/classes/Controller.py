import pika
from classes.Client import Client
from classes.OrderState import OrderState
from classes.Order import Order
from classes.Product import Product
from pickle import Pickler, Unpickler
import os

#host = 'localhost'
host = 'redes2.ii.uam.es'


class Controller:
    """ Clase representante del controlador del sistema """

    def __init__(self, logs):
        """ Constructor de la clase Controlador """

        # Para imprimir logs de las colas
        self.logs = logs
        self.client_num = 0
        self.order_num = 0
        self.clients = {}
        self.orders = []
        self.products = {1: Product(1, "pera", 3, "Deliciosa y jugosa fruta de temporada."),
                         2: Product(2, "mango", 3, "Exotica fruta tropical conocida por su explosion de sabor."),
                         3: Product(3, "manzana", 3, "Clasica y versatil para comer sola o combinar con recetas."),
                         4: Product(4, "kiwi", 3, "Fruta pequeña y vibrante, rico en vitamina C y fibra."),
                         5: Product(5, "platano", 3, "Suave y cremosa textura. Excelente fuente de potasio.")}

    def init(self):

        # Conexion al broker
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        # Declaracion colas clientes
        self.channel.queue_declare(
            queue='2311-13_client', durable=False, auto_delete=True)
        # Consumir mensajes cola clientes
        self.channel.basic_consume(
            queue='2311-13_client', on_message_callback=self.on_client_request)

        # Declaracion colas robots
        self.channel.queue_declare(
            queue='2311-13_robot', durable=False, auto_delete=True)
        self.channel.queue_declare(
            queue='2311-13_robot_callback', durable=False, auto_delete=True)
        # Consumir mensajes cola de respuestas robots
        self.channel.basic_consume(queue='2311-13_robot_callback',
                                   on_message_callback=self.on_robot_response, auto_ack=True)

        # Declaracion colas repartidores
        self.channel.queue_declare(
            queue='2311-13_dealer', durable=False, auto_delete=True)
        self.channel.queue_declare(
            queue='2311-13_dealer_callback', durable=False, auto_delete=True)
        # Consumir mensajes cola de respuestas repartidores
        self.channel.basic_consume(queue='2311-13_dealer_callback',
                                   on_message_callback=self.on_dealer_response, auto_ack=True)

    def on_client_request(self, ch, method, props, body):
        """ Funcion de manejo de las peticiones de los clientes """

        body_txt = body.decode('utf-8')
        request = body_txt.split()

        response = ""

        if self.logs == True:
            request_string = ""
            for r in request:
                request_string += f'{r} '
            print("Peticion ->", request_string)

        # Peticion de registro
        if request[0] == "REGISTER":
            client_id = self.get_clientID_by_user(request[1])

            if client_id is None:
                client = Client(self.client_num,
                                user=request[1], password=request[2])
                self.client_num += 1
                self.clients[client.id] = client
                response = f'REGISTERED {client.id} {client.user} {client.password}'

            else:
                response = "REGISTERED Failed"

        # Peticion de inicio de sesion
        elif request[0] == "LOGIN":
            client_id = self.get_clientID_by_user(request[2])
            if client_id is not None:
                client = self.clients[client_id]

                if self.clients[int(request[1])].password == request[3]:
                    response = "LOGGED-IN"

                else:
                    response = "LOGIN Failed"

        # Peticion de realizar un pedido
        elif request[0] == "ORDER":
            client_id = int(request[1])

            # Comprobar que el cliente esta registrado
            if client_id in self.clients and len(request) > 2:
                self.order(request)
                response = "ORDERED"

            else:
                response = "ORDER Failed"

        # Peticion de listar un pedido
        elif request[0] == "LIST":
            response = f'LIST Failed'
            client_id = int(request[1])

            # Comprobar que el cliente esta registrado
            if client_id in self.clients:
                response = "LISTED\n"

                for order in self.orders:
                    if order.client_id == client_id:
                        response += f'OrderID:{order.id}  - ProductsID:'

                        for p_id, amount in order.products.items():
                            response += f'|{p_id} amount:{amount}|'

                        response += f' - State:{order.state}\n'

        # Peticion de cancelar un pedido
        elif request[0] == "CANCEL":
            response = f'CANCEL Failed'
            client_id = int(request[1])

            # Comprobar que el cliente esta registrado
            if  client_id in self.clients:
                for order in self.orders:
                    if str(order.id) == request[2]:
                        if order.cancel() == True:
                            response = "CANCELLED"

        elif request[0] == "PRODUCTS":
            client_id = int(request[1])

            # Comprobar que el cliente esta registrado
            if  client_id in self.clients:
                response = "PRODUCTS\n\n"

                for product in self.products.values():
                    response += f'Product: {product.name} Stock: {product.stock}\nDescripcion: {product.description}\n\n'
            else:
                response = f'PRODUCTS Failed'

        # Enviar respuesta
        self.channel.basic_publish(exchange='',
                                   routing_key=props.reply_to,
                                   properties=pika.BasicProperties(correlation_id=props.correlation_id), body=response)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def order(self, request):
        """ Funcion que realiza el pedido de un cliente """

        # Crear pedido
        order = Order(self.order_num, int(request[1]), OrderState.IN_WAREHOUSE)
        self.order_num += 1
        self.orders.append(order)
        requested_products = []

        if self.logs == True:
            print(f'Pedido creado -> {order.id} {str(order.state)}')

        # Agregar todos los productos con sus correspondientes cantidades
        for p_id in request[2:]:
            product_id = int(p_id)

            # No hay suficiente stock de un producto = pedido incompleto
            if self.products[product_id].available() == False:
                order.state = OrderState.INCOMPLETE

                # Volver a aumentar el stock del resto de productos del pedido
                for product, amount in order.products.items():
                    self.products[product].stock += amount

                next

            else:
                # Quitar 1 al stock del producto
                self.products[product_id].stock -= 1

                if product_id in requested_products:
                    order.update_product_amount(product_id)

                else:
                    order.products[product_id] = 1
                    requested_products.append(product_id)

        # Enviar peticion de busqueda de productos a los robots
        self.find_order(order)

    def find_order(self, order):
        """ Funcion que solicita la busqueda de los productos de un pedido """

        for product, amount in order.products.items():

            self.channel.basic_publish(exchange='',
                                       routing_key='2311-13_robot',
                                       properties=pika.BasicProperties(
                                           delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
                                       body=f'FIND {order.id} {product} {amount}'
                                       )

    def on_robot_response(self, ch, method, props, body):
        """ Funcion de manejo de las respuestas de los robots """

        response = body.decode('utf-8')
        response = response.split()

        if self.logs == True:
            response_string = ""
            for r in response:
                response_string += f'{r} '
            print("Respuesta robot ->", response_string)

        for order in self.orders:
            if str(order.id) == response[1]:

                if response[0] == "FOUND":

                    # Marcar 1 producto encontrado
                    order.found_products += 1

                    if order.state != OrderState.CANCELLED:
                        # Todos los productos se han encontrado
                        if order.found_products == len(order.products):
                            order.state = OrderState.ON_CONVEYOR
                            # Mandar a repartir el pedido
                            self.distribute(order.id)

                        # Faltan productos por encontrar
                        else:
                            order.state = OrderState.IN_WAREHOUSE
                    else:
                        print(
                            f'Producto encontrado de un pedido cancelado -> {str(order.state)}')
                        # El robot no lo recoge y por tanto el stock del producto se queda igual
                else:
                    order.state = OrderState.INCOMPLETE
                    if self.logs == True:
                        print(f'Pedido incompleto -> {str(order.state)}')

                    # Volver a aumentar el stock del resto de productos del pedido
                    for product, amount in order.products.items():
                        self.products[product].stock += amount

                break

    def distribute(self, order_id):
        """ Funcion que solicita la distribucion de un pedido """

        self.channel.basic_publish(exchange='',
                                   routing_key='2311-13_dealer',
                                   properties=pika.BasicProperties(
                                       delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
                                   body=f'DISTRIBUTE {order_id}'
                                   )

    def on_dealer_response(self, ch, method, props, body):
        """ Funcion de manejo de las respuestas de los repartidores """

        response = body.decode('utf-8')
        response = response.split()

        if self.logs == True:
            response_string = ""
            for r in response:
                response_string += f'{r} '
            print("Respuesta repartidor ->", response_string)

        # Recoger pedido por id
        for o in self.orders:
            if str(o.id) == response[1]:
                order = o
                break

        if response[0] == "DELIVERED":
            order.state = OrderState.DELIVERED

        elif response[0] == 'ON-DELIVERY':
            order.state = OrderState.ON_DELIVERY

        elif response[0] == "FAILED-DELIVERY" and order.try_to_deliver > 1:
            # Volver a intentar la entrega del pedido
            if self.logs == True:
                print("\nNuevo intento de entrega\n")

            order.try_to_deliver -= 1
            self.distribute(response[2])

        else:
            order.state = OrderState.FAILED_DELIVERY

    def load(self):
        """ Funcion para cargar el estado del sistema """

        if (os.path.isfile("./data") == False):
            print("\nNo hay fichero de datos que cargar.\n")

        else:
            print("Cargando datos del fichero <data>...\n")

            file = open('data', 'rb')
            data = Unpickler(file).load()
            file.close()

            # Cargar elementos del sistema
            self.client_num = data[0]
            self.order_num = data[1]
            self.clients = data[2]
            self.orders = data[3]
            self.products = data[4]

    def save(self):
        """ Funcion para guardar el estado del sistema """

        print("\nGuardando datos del sistema...\n")

        data = [self.client_num, self.order_num, self.clients, self.orders, self.products]

        file = open('data', 'wb')
        Pickler(file).dump(data)
        file.close()

    def get_clientID_by_user(self, user):
        """ Funcion auxiliar para obtener un cliente por su nombre de usuario """

        for c in self.clients.values():
            if c.user == user:
                return c.id

        return None
