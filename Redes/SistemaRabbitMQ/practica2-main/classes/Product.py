import pika

class Product:
    """ Clase representante de un producto """

    def __init__(self, id, name, stock, description):
        """ Constructor de la clase Producto """

        self.id = id
        self.name = name
        self.stock = stock
        self.description = description

    def available(self):
        if self.stock > 0:
            return True
        return False