import enum

class OrderState(enum.Enum):
    """ Clase representante de todos los posibles estados de un pedido"""
    
    CANCELLED = 1
    DELIVERED = 2
    IN_WAREHOUSE = 3
    ON_DELIVERY = 4
    FAILED_DELIVERY = 5
    ON_CONVEYOR = 7
    INCOMPLETE = 8

    def __str__(self):
        """ Muestra el nombre del estado en formato string """
        
        return str(self.name)