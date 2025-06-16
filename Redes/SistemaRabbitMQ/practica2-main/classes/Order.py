import pika
from classes.OrderState import OrderState


class Order:
    """ Clase representante de un pedido """

    def __init__(self, id, client_id, state: OrderState):
        """ Constructor de la clase Producto """

        self.id = id
        self.client_id = client_id
        self.state = state
        self.products = {}
        self.try_to_deliver = 3
        self.found_products = 0

    def update_product_amount(self, product_id):
        """ Funcion que actualiza la cantidad de un producto del pedido """
        
        self.products[product_id] += 1

    def cancel(self) -> bool:
        """ Funcion que cancela un pedido """

        if self.state == OrderState.IN_WAREHOUSE:
            self.state = OrderState.CANCELLED
            return True

        return False
