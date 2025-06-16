from src.database import DatabaseManager, SecureDatabaseManager
from src.auth import AuthManager
from src.container import ContainerManager
from src.cloud import CloudManager
from utils.curses_ui import CursesUi
from config.settings import PASSWORD, DATABASE, ENC_DATABASE
from data.queries import DROP_CONTAINERS
import curses
import argparse
import sys
import signal
import os

"""

SecureBox - Gestor de Contraseñas Seguro

Este archivo es el punto de entrada del programa. 
Gestiona la autenticacion del usuario, interaccion 
con la base de datos cifrada y sincronizacion con la nube.

Flujo de ejecucion:
1. Solicita la contraseña y autentica al usuario.
2. Proporciona un menú de opciones para gestionar contenedores de contraseñas.
3. Para cada ejecucion descifra y cifra la base de datos.
4. Sincroniza los cambios con Google Drive (si se solicita).

"""

# Variables globales de la base de datos cifrada para gestionar
# la seguridad desde todos los metodos del main
secure_db = None
pwd = None


def signal_handler(sig, frame):
    """ Manejador de señales para SIGINT (Ctrl^C) """

    sys.exit(0)  # Finaliza el programa de manera controlada


def handle_command_line_arguments():
    """ Verifica las opciones de línea de comandos y las ejecuta. """

    parser = argparse.ArgumentParser(
        description="SecureBox - Gestor de contraseñas seguro")
    parser.add_argument('--init', action='store_true',
                        help="Inicializa la base de datos creando las tablas.")
    parser.add_argument('--clean', action='store_true',
                        help="Limpia la base de datos. Elimina todas las tablas existentes. ")
    args = parser.parse_args()

    if args.init:
        # Si se pasa --init, inicializa las bases de datos
        db = SecureDatabaseManager()
        user_db = DatabaseManager()

        # Gestor de autenticacion que crea al usuario
        auth = AuthManager(user_db)
        res = auth.create_user(PASSWORD)

        if res == 0:
            print("\nBase de datos inicializada correctamente.")
        elif res == -1:
            print("\nError en la base de datos.")
        elif res == -2:
            print("\nError. Ya existe un usuario con esos datos.")
        return True

    elif args.clean:
        # Si se pasa --clean, borra todas las tablas de ambas bases de datos
        db = SecureDatabaseManager()
        user_db = DatabaseManager()

        db.clean_db()
        user_db.clean_db()

        print("\nBase de datos limpia.")
        return True

    return False


def main(stdscr):
    """ Funcion principal que gestiona la interaccion del usuario con el programa. """

    global secure_db
    global pwd

    # Inicializacion de los elementos
    db = SecureDatabaseManager()
    user_db = DatabaseManager()

    container_manager = ContainerManager(db)
    auth = AuthManager(user_db)

    cloud = CloudManager()

    # Inicializacion gestor UI
    ui = CursesUi(stdscr)

    # Registrar el manejador de la señal SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)
    secure_db = db
    pwd = PASSWORD

    # Si no existe, es la primera vez que entra en la aplicacion -> ENCRIPTAR
    if os.path.exists(ENC_DATABASE) == False:
        encrypted = db.encrypt_db(DATABASE, ENC_DATABASE, PASSWORD)
        if encrypted != 0:
            ui.show_message(
                "Problemas al iniciar la aplicacion de forma segura", 1)
            return

    # Pantalla limpia
    ui.clear_screen()

    ui.show_message("Bienvenido a SecureBox - Gestor de contraseñas seguro", 1)
    ui.show_message(
        "Por favor, ingrese la contraseña maestra (pulse ESC para salir)", 4)

    # Autenticacion del usuario
    while auth.attempts < 3 and auth.authenticated == False:
        if auth.attempts != 0:
            ui.clear_line(8)
            ui.show_temporal_message("Intentelo de nuevo", 5)

        password = ui.password_input(8)
        if password == False:
            return

        auth.authenticate(password)

        if auth.blocked:
            ui.clear_screen()
            ui.show_message(
                "---> Has alcanzado el maximo numero de intentos", 1)

            ui.pause_screen(3000)

            return

    options = [
        "1. Crear contenedor",
        "2. Listar contenedores",
        "3. Ver contenedor",
        "4. Editar contenedor",
        "5. Eliminar contenedor",
        "6. Subir datos a la nube",
        "7. Descargar datos de la nube",
        "8. Salir"
    ]

    while True:
        menu_option = ui.menu(options, 0)

        if menu_option == 0:
            create_container_view(ui, container_manager)
            ui.stdscr.getch()  # Espera una tecla antes de volver al menu

        elif menu_option == 1:
            list_containers_view(ui, container_manager)
            ui.stdscr.getch()  # Espera una tecla antes de volver al menu

        elif menu_option == 2:
            show_container_view(
                ui, container_manager)
            ui.stdscr.getch()  # Espera una tecla antes de volver al menu

        elif menu_option == 3:
            edit_container_view(
                ui, container_manager)
            ui.stdscr.getch()  # Espera una tecla antes de volver al menu

        elif menu_option == 4:
            remove_container_view(
                ui, container_manager)
            ui.stdscr.getch()  # Espera una tecla antes de volver al menu

        elif menu_option == 5:
            ui.clear_screen()
            upload = cloud.upload(ENC_DATABASE)
            if upload == 0:
                ui.show_message("Subida de datos completada con exito.", 2)
            elif upload == -1:
                ui.show_message("Error en la API de Google Drive.", 2)
            elif upload == -2:
                ui.show_message(
                    "Error: No se ha encontrado el archivo.", 2)
            elif upload == -3:
                ui.show_message(
                    "Error: No tienes permisos para acceder.", 2)
            elif upload == -4:
                ui.show_message("Error generico en la subida.", 2)
            stdscr.getch()  # Espera una tecla antes de volver al menu

        elif menu_option == 6:
            ui.clear_screen()

            download = cloud.download(ENC_DATABASE.removeprefix("data/"))
            if download == 0:
                ui.show_message("Descarga de datos completada con exito.", 2)
            elif download == -1:
                ui.show_message("Error en la API de Google Drive.", 2)
            elif download == -2:
                ui.show_message("Error: No se ha encontrado el archivo.", 2)
            elif download == -3:
                ui.show_message("Error: No tienes permisos para acceder.", 2)
            elif download == -4:
                ui.show_message("Error generico en la descarga.", 2)

            dec = container_manager.db.decrypt_db(ENC_DATABASE, DATABASE, pwd)
            if dec != 0:
                ui.show_message(
                    "Error de desencriptado despues de la subida. ", 2)
            stdscr.getch()  # Espera una tecla antes de volver al menu

        elif menu_option == 7:
            ui.clear_screen()
            ui.show_message("Cerrando SecureBox... ¡Hasta pronto!", 1)

            # Cerrar conexiones con las bases de datos
            db.close()
            user_db.close()

            # Pausar por 2 segundos
            ui.pause_screen(2000)

            break

        else:
            ui.show_temporal_message(
                "Opcion no valida. Intentelo de nuevo", 12)

    return


def create_container_view(ui, container_manager):
    """ Muestra la vista al crear un contenedor. """

    global pwd

    ui.clear_screen()
    ui.show_message("Nuevo contenedor", 0, ui.TextStyle.BOLD)
    ui.show_message("Nombre:", 2)
    name = ui.get_message(3)

    ui.show_message("Ingresa el contenido: ", 5)
    content = ui.get_message(6)

    ui.show_message("Introduce clave para cifrar el contenedor",
                    8, ui.TextStyle.BOLD)
    password = ui.password_input(9)

    # Desencriptar base de datos, crear contenedor y volver a encriptar
    res = container_manager.db.decrypt_db(ENC_DATABASE, DATABASE, pwd)
    if res != 0:
        ui.show_message(f"{res}", 4)

    action = container_manager.create_container(name, content, password)

    res = container_manager.db.encrypt_db(DATABASE, ENC_DATABASE, pwd)
    if res != 0:
        return res

    if action == 0:
        ui.show_temporal_message("Contenedor creado exitosamente", 12)
    elif action == -1:
        ui.show_temporal_message("Error en la base de datos", 12)
    elif action == -2:
        ui.show_temporal_message(
            "Error. Ya existe un contenedor con ese nombre", 12)
    elif action == -3:
        ui.show_temporal_message(
            "Error.", 12)


def list_containers_view(ui, container_manager):
    """ Muestra la vista al listar los contenedores. """

    global pwd

    ui.clear_screen()

    # Desencriptar la base de datos, listar contenedores y volver a encriptar
    res = container_manager.db.decrypt_db(ENC_DATABASE, DATABASE, pwd)
    if res != 0:
        return res

    containers = container_manager.get_container_list()

    res = container_manager.db.encrypt_db(DATABASE, ENC_DATABASE, pwd)
    if res != 0:
        return res

    if containers is None:
        ui.show_message("Error en la base de datos.", 1)
    elif not containers:
        ui.show_message("No se ha creado ningun contenedor aun.", 1)
    else:
        ui.show_message("CONTENEDORES:", 0, ui.TextStyle.BOLD)
        for i, c in enumerate(containers, start=2):
            ui.show_message(f"{c[0]} - {c[1]}", i)


def show_container_view(ui, container_manager):
    """ Muestra la vista al ver un contenedor. """

    global pwd

    ui.clear_screen()

    ui.show_message("Vista contenedor", 0, ui.TextStyle.BOLD)

    ui.show_message("Ingresa el ID del contenedor:", 2)
    container_id = ui.get_message(3)

    ui.show_message("Contraseña del contenedor:", 5)
    password = ui.password_input(6)

    # Desencriptar la base de datos, mostrar contenido del contenedor y volver a encriptar
    res = container_manager.db.decrypt_db(ENC_DATABASE, DATABASE, pwd)
    if res != 0:
        return res

    content = container_manager.get_container_content(
        container_id, password)

    res = container_manager.db.encrypt_db(DATABASE, ENC_DATABASE, pwd)
    if res != 0:
        return res

    ui.show_message(f"Contenido del contenedor: {content}", 8)

    return res


def edit_container_view(ui, container_manager):
    """ Muestra la vista al editar un contenedor. """

    global pwd

    ui.clear_screen()
    ui.show_message("Editar contenedor", 0, ui.TextStyle.BOLD)

    ui.show_message("Ingresa el ID del contenedor:", 2)
    container_id = ui.get_message(3)

    ui.show_message("Nuevo contenido:", 5)
    content = ui.get_message(6)

    ui.show_message("Contraseña del contenedor:", 8)
    password = ui.password_input(9)

    # Desencriptar la base de datos, editar contenido del contenedor y volver a encriptar
    res = container_manager.db.decrypt_db(ENC_DATABASE, DATABASE, pwd)
    if res != 0:
        return res

    action = container_manager.edit_container(
        container_id, password, content)

    res = container_manager.db.encrypt_db(DATABASE, ENC_DATABASE, pwd)
    if res != 0:
        return res

    if action == 0:
        ui.show_temporal_message("Contenedor editado exitosamente", 11)
    elif action == -2:
        ui.show_temporal_message(
            "Error. No se pudo editar el contenedor", 11)

    return res


def remove_container_view(ui, container_manager):
    """ Muestra la vista al eliminar un contenedor. """

    global pwd

    ui.clear_screen()

    ui.show_message("Eliminar contenedor", 0, ui.TextStyle.BOLD)

    ui.show_message("Ingresa el ID del contenedor:", 2)
    container_id = ui.get_message(3)

    ui.show_message("Contraseña del contenedor:", 5)
    password = ui.password_input(6)

    # Desencriptar la base de datos, eliminar contenedor y volver a encriptar
    res = container_manager.db.decrypt_db(ENC_DATABASE, DATABASE, pwd)
    if res != 0:
        return res

    action = container_manager.delete_container(container_id, password)

    res = container_manager.db.encrypt_db(DATABASE, ENC_DATABASE, pwd)
    if res != 0:
        return res

    if action == 0:
        ui.show_temporal_message("Contenedor eliminado exitosamente", 8)
    elif action == -2:
        ui.show_temporal_message(
            "Error. No se pudo eliminar el contenedor", 8)

    return res


if __name__ == "__main__":

    if handle_command_line_arguments() is False:
        curses.wrapper(main)
