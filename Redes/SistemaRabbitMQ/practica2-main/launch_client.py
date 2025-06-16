from classes.Client import Client
import time

def main():
    """ Funcion que ejecuta un client """
    client = Client()
    client.init()

    print("-- Script de simulacion de acciones de un cliente --")
    # Registrarse
    response = client.register("luchi", "1234")
    print(f'\nRegistro de cliente -> Respuesta: {response}')

    # Volver a registrarse con mismo usuario
    response = client.register("luchi", "1234")
    print(f'\nRegistro de cliente con mismo usuario -> Respuesta: {response}')

    # Iniciar sesion
    response = client.log_in("luchi", "1234")
    print(f'\nInicio sesion de cliente -> Respuesta: {response}')

    # Iniciar sesion con contrasenya incorrecta
    response = client.log_in("luchi", "suuu")
    print(f'\nInicio sesion de cliente con contrasenya incorrecta -> Respuesta: {response}')

    # Hacer pedido 1
    response = client.make_order([1, 1, 2])
    print(f'\nCliente {client.user} realiza pedido 0 -> Respuesta: {response}')

    # Hacer pedido 2
    response = client.make_order([3, 1, 1])
    print(f'\nCliente {client.user} realiza pedido 1 -> Respuesta: {response}')

    # Listar productos de la aplicacion
    response = client.list_products()
    print(f'\nCliente {client.user} pide lista de productos -> Respuesta: {response}')

    # Listar pedidos
    response = client.list_orders()
    print(f'\nPedidos del cliente {client.user} -> Respuesta: {response}')

    print("(Esperar unos segundos para cancelar un pedido)")
    time.sleep(6)
    
    # Cancelar pedido
    response = client.cancel_order(0)
    print(f'Cancelar pedido 0 -> Respuesta: {response}')

    # Listar pedidos de nuevo
    response = client.list_orders()
    print(f'\nPedidos del cliente {client.user} -> {response}')

if __name__ == "__main__":
    main()
