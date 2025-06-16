from config.settings import MAX_ATTEMPTS
from data.queries import INSERT_USER, SELECT_USER_PASSWORD
from src.crypto import CryptoManager
import bcrypt


class AuthManager:
    """ Clase que gestiona la autenticacion del usuario y la seguridad de sus datos. """

    def __init__(self, db):
        self.db = db
        self.crypto = CryptoManager()
        self.authenticated = False
        self.max_attempts = MAX_ATTEMPTS
        self.attempts = 0
        self.blocked = False

    def create_user(self, password):
        """ Crea un nuevo usuario con la contraseña encriptada y su salt. """

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode(), salt)

        # Intentar insertar el nuevo usuario en la base de datos
        return self.db.execute_query(INSERT_USER, (password_hash, salt))

    def authenticate(self, password):
        """ Autentica al usuario verificando su contraseña con la base de datos. """

        # Verificar la contraseña con la base de datos
        password_hash = self.db.fetch_one(SELECT_USER_PASSWORD)

        # Si es correcta, desencriptar base de datos. En caso contrario,
        # aumentar numero de intentos fallidos y bloquear si fuera necesario
        if bcrypt.checkpw(password.encode(), password_hash[0]) == True:
            self.authenticated = True
            self.attempts = 0

        else:
            self.authenticated = False
            self.attempts += 1

            if self.attempts >= self.max_attempts:
                self.blocked = True
