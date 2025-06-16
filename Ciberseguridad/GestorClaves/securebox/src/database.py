import sqlite3
from config.settings import *
from data.queries import *
from src.crypto import CryptoManager


class DatabaseManager:
    """ Clase que gestiona la interaccion con la base de datos de usuarios. """

    def __init__(self, db_path=USER_DATABASE):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_db()

    def create_db(self):
        """ Crea la tabla de usuarios (base de datos que no se encripta). """

        self.execute_query(CREATE_USER_TABLE)

    def clean_db(self):
        """ Limpia la base de datos. """

        os.remove(self.db_path)

    def execute_query(self, query, params=None):
        """
        Ejecuta una determinada query (insert, update).

        Salida:
         0 Si todo va bien
        -1 Si ocurre un error en la base de datos
        -2 Si ocurre un error de integridad de datos
        -3 Si ocurre cualquier otro error

        """

        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()

        except sqlite3.OperationalError:
            return -1
        except sqlite3.IntegrityError:
            return -2
        except Exception:
            return -3

        return 0

    def fetch_one(self, query, params=None):
        """
        Devuelve la primera fila de los resultados de la query.

        Salida: Resultado de la query si todo va bien, None en caso contrario

        """

        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()

        except Exception:
            return None

    def fetch_all(self, query, params=None):
        """
        Devuelve todos los resultados de la query.

        Salida: Resultados de la query si todo va bien, None en caso contrario

        """

        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()

        except Exception:
            return None

    def close(self):
        """ Cierra la conexion a la base de datos. """

        if self.conn:
            self.conn.close()


class SecureDatabaseManager(DatabaseManager):
    """ Clase heredada de DatabaseManager que gestiona la interaccion
    con la base de datos cifrada. """

    def __init__(self, db_path=DATABASE):
        super().__init__(db_path)
        self.crypto = CryptoManager()
        self.is_encrypted = False

    def create_db(self):
        """ Crea la tabla de contenedores. """

        self.execute_query(CREATE_CONTAINER_TABLE)
    
    def clean_db(self):
        super().clean_db()
        os.remove(self.db_path + ".enc")
    
    def encrypt_db(self, input_file_path, output_file_path, password):
        """ 
        Encripta el archivo de la base de datos. 
        
        Salida:
         0 Si todo va bien
        -1 Si ocurre un error al encriptar
        -2 Si ocurre un error de fichero
        
        """
        
        try:
            # Leer el archivo de la base de datos
            with open(input_file_path, "rb") as db_file:
                db_data = db_file.read()
            
            # Encriptar los datos de la base de datos
            encrypted_db = self.crypto.encrypt(db_data, password)
            if encrypted_db is None:
                return -1
            
            # Guardar los datos encriptados en la base de datos
            with open(output_file_path, "wb") as encrypted_db_file:
                encrypted_db_file.write(encrypted_db)

            # Vaciar base de datos sin encriptar
            self.execute_query(DROP_CONTAINERS)

        except Exception:
            return -2
        
        return 0
    
    def decrypt_db(self, input_file_path, output_file_path, password):
        """ 
        Desencripta el archivo de la base de datos. 
        
        Salida:
         0 Si todo va bien
        -1 Si ocurre un error al encriptar
        -2 Si ocurre un error de fichero
        
        """

        try:
            with open(input_file_path, "rb") as encrypted_db_file:
                encrypted_data = encrypted_db_file.read()

            
            decrypted_db = self.crypto.decrypt(encrypted_data, password)
            if decrypted_db is None:
                return -2
            
            with open(output_file_path, "wb") as db_file:
                db_file.write(decrypted_db)
        
        except Exception as e:
            return e
        
        return 0