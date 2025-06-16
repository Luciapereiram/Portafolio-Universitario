from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os
import base64


class CryptoManager:
    """ Clase que gestiona la encriptacion de datos. """

    def generate_key(self, password, salt):
        """ 
        Deriva una clave para la autenticacion a partir de una contraseña. 

        Uso de Scrypt para derivacion de clave:
            - salt: valor aleatorio
            - length: tam clave derivada (32B = 256b)
            - n: num de iteraciones
            - r: num de bloques de memoria
            - p: num de hilos en paralelo

        """

        kdf = Scrypt(salt, length=32, n=2**14, r=8, p=1)
        b_key = kdf.derive(password.encode())
        return base64.urlsafe_b64encode(b_key)

    def encrypt(self, plaintext, password, salt=None):
        """ 
        Encripta un mensaje en texto claro utilizando Fernet. 

        Salida: Datos cifrados si todo va bien, None en caso contrario

        """

        if salt is None:
            # Genera un salt aleatorio de 16B si no se proporciona
            salt = os.urandom(16)

        try:
            # Crear un objeto Fernet con la clave
            fernet = Fernet(self.generate_key(password, salt))

            # Encriptar el texto plano
            encrypted_data = fernet.encrypt(plaintext)

            return salt + encrypted_data  # Concatenar el salt con los datos cifrados

        except Exception:
            return None

    def decrypt(self, encrypted_data, password):
        """ 
        Desencripta datos encriptados usando la misma contraseña. 

        Salida: Datos descifrados si todo va bien, None en caso contrario

        """

        # Extraer el salt de los primeros 16 bytes
        salt = encrypted_data[:16]
        ciphertext = encrypted_data[16:]    # Extraer los datos cifrados

        try:
            # Crear un objeto Fernet con la clave
            key = self.generate_key(password, salt)
            fernet = Fernet(key)

            # Desencriptar los datos
            decrypted_data = fernet.decrypt(ciphertext)

            return decrypted_data

        except Exception:
            return None