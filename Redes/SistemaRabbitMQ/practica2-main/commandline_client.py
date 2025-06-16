import sys
from classes.Client import Client

num_id_cola = 0

def main():
    client = Client(num_id_cola)
    client.init()

    while True:
        welcome(client)

def welcome(client):
    print("------------------------------------------")
    print("--------------- SAIMAZOOM  ---------------")
    print("------------------------------------------")
    
    while True:
        print("\n1. Registrarse")
        print("2. Iniciar Sesion")
        print("3. Salir")

        option = input("\nIngrese el numero de la accion que desea realizar: ")

        if option == "1":
            user = input("Introduce un nombre de usuario: ")
            password = input("Introduce una contrasenya: ")

            response = client.register(user, password)

            if response == "REGISTERED":
                print(f'\n--> Usuario {user} registrado con exito')
            else:
                print(f'\n--> Nombre de usuario {user} ya existe')

        elif option == "2":
            user = input("Nombre de usuario: ")
            password = input("Contrasenya: ")

            response = client.log_in(user, password)

            if response == "LOGGED-IN":
                print("\n--> Se ha iniciado sesion correctamente.")
                home(client)
            else:
                print("\n--> Usuario o contrasenya incorrectos ¿Seguro que esta registrado?")

        elif option == "3":
            print("\n¡Hasta pronto!")
            sys.exit(0)

        else: 
            print("\n--> Esa opcion no esta disponible.")


def home(client):
    while True:
        print("\n\n¡Bienvenido a Saimazoom! ¿Que desea?")
        print("\n1. Realizar pedido")
        print("2. Ver mis pedidos")
        print("3. Cancelar un pedido")
        print("4. Productos Saimazoom")
        print("5. Salir")

        option = input("\nIngrese el numero de la accion que desea realizar: ")

        if option == "1":
            print("\n-- PRODUCTOS SAIMAZOOM --")
            print("\n1. Pera")
            print("2. Mango")
            print("3. Manzana")
            print("4. Kiwi")
            print("5. Platano")
            print("6. No deseo agregar mas productos")

            order_products = []
            product = ""
            while product != "6":
                product = input("\nIngrese el numero de producto a agregar: ")
                
                if int(product) not in [1, 2, 3, 4, 5, 6]:
                    print("Ese producto no esta disponible.")

                else:
                    if int(product) != 6:
                        order_products.append(int(product))

            print("\n ---- Resumen de su pedido ---- ")
            print(f'IDs de productos agregados: {order_products}')

            response = client.make_order(order_products)

            if response == "ORDERED":
                print("Pedido realizado con exito. Consulte su estado en el menu principal.")

            else:
                print("No pudo realizarse el pedido. Intentelo de nuevo mas tarde.")

    
        elif option == "2": 

            print("\n-- MIS PEDIDOS --\n")
            res = list_orders(client)

            if res == "-1":
                print("\n--> No se pudo acceder a esta accion")

            elif res == "0":
                print("\n--> No ha realizado ningun pedido aun")

            else:
                print(res)

        elif option == "3": 
            
            res = list_orders(client)
            
            if res == "-1" or res == "0":
                print("\n--> No hay pedidos para cancelar")

            else:
                print(f'\n-- MIS PEDIDOS --\n{res}')

                order_id = input("Numero de pedido que desea cancelar: ")

                response = client.cancel_order(order_id)

                if response == "CANCELLED":
                    print("\n--> Pedido cancelado a tiempo.")

                else:
                    print("\n--> Error de cancelacion.")

        elif option == "4":
            print(client.list_products())


        elif option == "5": 

            print("\n¡Hasta pronto!")
            sys.exit(0)
            
        else: 
            print("\n--> Esa opcion no esta disponible.")

def list_orders(client):

    response = client.list_orders()
    response_txt = response.split()
    res = ""

    if len(response_txt) > 1 and response_txt[1] == "Failed":
        res = "-1"
    
    elif len(response_txt) == 1:
        res = "0"
              
    else:
        res = response.replace("LISTED\n", "")
    
    return res
    
if __name__ == "__main__":
    main()

