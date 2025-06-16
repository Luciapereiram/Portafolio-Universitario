from src.crypto import CryptoManager
from data.queries import *


class ContainerManager:
    """ Clase que gestiona la interaccion con los contenedores del sistema de forma segura. """

    def __init__(self, db):
        self.db = db
        self.crypto = CryptoManager()

    def get_container_count(self):
        """ 
        Recoge el numero de contenedores creados en el sistema. 

        Salida: Numero de contenedores (count) si todo va bien, 
        -1 en caso contrario

        """

        count = self.db.fetch_one(SELECT_CONTAINER_COUNT)
        if count is None:
            return -1

        return count

    def create_container(self, name, content, password):
        """ 
        Crea un contenedor con el contenido cifrado. 

        Salida:
        None Si ocurre un error de encriptacion
         0 Si todo va bien
        -1 Si ocurre un error en la base de datos 
        -2 Si ocurre un error de integridad de datos
        -3 Si ocurre cualquier otro error

        """

        encrypted_data = self.crypto.encrypt(content.encode(), password)

        if encrypted_data is not None:
            return self.db.execute_query(INSERT_TABLE_CONTAINERS, (name, encrypted_data))

        return encrypted_data

    def get_container_list(self):
        """ 
        Devuelve una lista con todos los nombres e ids de los contenedores. 

        Salida:
         Contenedores Si todo va bien
         None         Si hay algún error 

        """
        
        return self.db.fetch_all(SELECT_CONTAINERS)

    def get_container_content(self, container_id, password):
        """ 
        Devuelve el contenido de un contenedor desencriptado. 

        Salida: Resultado de la query si todo va bien, None en caso contrario

        """

        content = self.db.fetch_one(SELECT_CONTAINER_CONTENT, (container_id,))
        if content is None:
            return None

        dec = self.crypto.decrypt(content[0], password)
        if dec == None:
            return None
        else:
            return dec.decode()

    def edit_container(self, container_id, password, new_content):
        """ 
        Edita el contenido de un contenedor. 

        Salida:
        None Si ocurre un error de encriptacion
         0 Si todo va bien
        -2 Si ocurre un error de integridad de datos


        """

        content = self.db.fetch_one(SELECT_CONTAINER_CONTENT, (container_id,))
        if content is None:
            return None

        try:
            decrypted_data = self.crypto.decrypt(content[0], password)
            if decrypted_data is None:
                return -2

            encrypted_data = self.crypto.encrypt(new_content.encode(), password)
            if encrypted_data is None:
                return -2

            return self.db.execute_query(UPDATE_CONTAINER_CONTENT, (encrypted_data, container_id))

        except Exception:
            return None

    def delete_container(self, container_id, password):
        """ 
        Elimina un contenedor de la base de datos. 

        Salida:
        None Si ocurre un error de encriptacion
         0 Si todo va bien
        -2 Si ocurre un error de integridad de datos

        """

        content = self.db.fetch_one(SELECT_CONTAINER_CONTENT, (container_id,))
        if content is None:
            return None

        try:
            decrypted_data = self.crypto.decrypt(content[0], password)
            if decrypted_data is None:
                return -2

            return self.db.execute_query(DELETE_CONTAINER, (container_id,))

        except Exception:
            return None
