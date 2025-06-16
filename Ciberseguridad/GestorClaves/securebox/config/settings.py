import os

""" Fichero para guardar las macros del programa """

MAX_ATTEMPTS = 3
DATABASE = "data/securebox.db"
ENC_DATABASE = "data/securebox.db.enc"
USER_DATABASE = "data/user.db"
PASSWORD = os.getenv("SECUREBOX_PASSWORD")
TOKEN_PATH = os.path.join(os.getcwd(), ".credentials", "token.pickle")
CREDENTIALS_JSON_PATH = os.path.join(os.getcwd(), ".credentials", "client_secret.json")

# Alcances necesarios para subir archivos a Google Drive
SCOPES = ["https://www.googleapis.com/auth/drive.file"]