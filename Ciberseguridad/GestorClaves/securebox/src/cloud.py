from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from config.settings import TOKEN_PATH, CREDENTIALS_JSON_PATH, ENC_DATABASE, SCOPES
import os
import io
import pickle


class CloudManager:
    """ Clase que gestiona la subida y descarga de la base
    de datos a Google Drive. """

    def __init__(self, db_path=ENC_DATABASE):
        self.db_path = db_path

    def authenticate(self):
        """ 
        Autentica y devuelve un servicio de Google Drive. 

        Salida: Servicio de Google Drive si todo va bien, None en caso contrario

        """

        credentials = None

        try:
            # Si ya hay credenciales validas guardadas, cargar
            if os.path.exists(TOKEN_PATH):
                with open(TOKEN_PATH, "rb") as token:
                    credentials = pickle.load(token)

            # Se pide autenticacion en caso contrario
            if not credentials or not credentials.valid:

                if credentials and credentials.expired and credentials.refresh_token:
                    # Si existen credenciales pero han expirado, actualizar
                    credentials.refresh(Request())
                else:
                    # No existen credenciales, se crean
                    flow = InstalledAppFlow.from_client_secrets_file(
                        CREDENTIALS_JSON_PATH, SCOPES)
                    credentials = flow.run_local_server(port=0)

                # Guardar las credenciales para futura autenticacion
                with open(TOKEN_PATH, "wb") as token:
                    pickle.dump(credentials, token)

            # Crear el servicio
            service = build("drive", "v3", credentials=credentials)

            return service

        except Exception:
            return None

    def upload(self, file_path):
        """ 
        Sube un archivo a Google Drive. 

        Salida:
         0 Si todo va bien
        -1 Si ocurre un error en la API
        -2 Si no se encuentra el archivo
        -3 Si no se tienen permisos para acceder al archivo
        -4 Si ocurre cualquier otro error

        """

        try:
            service = self.authenticate()

            file_metadata = {"name": os.path.basename(file_path)}

            # 'resumable' para reanudar subidas fallidas
            media = MediaFileUpload(file_path, resumable=True)

            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id"
            ).execute()

            return 0

        except HttpError:
            return -1
        except FileNotFoundError:
            return -2
        except PermissionError:
            return -3
        except Exception:
            return -4

    def download(self, filename):
        """ 
        Busca un archivo en Google Drive y lo descarga. 

        Salida:
         0 Si todo va bien
        -1 Si ocurre un error en la API
        -2 Si no se encuentra el archivo
        -3 Si no se tienen permisos para acceder al archivo
        -4 Si ocurre cualquier otro error

        """

        try:
            service = self.authenticate()

            # Buscar archivo por nombre
            query = f"name = '{filename}' and trashed = false"
            results = service.files().list(q=query, spaces="drive",
                                           fields="files(id, name)").execute()
            files = results.get("files", [])

            # Si no se encuentra el archivo
            if not files:
                return -2

            file_id = files[0]["id"]
            request = service.files().get_media(fileId=file_id)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)

            done = False
            while not done:
                _, done = downloader.next_chunk()

            return self._replace_file(file_content.getvalue(), self.db_path)

        except HttpError:
            return -1
        except FileNotFoundError:
            return -2
        except PermissionError:
            return -3
        except Exception:
            return -4

    def _replace_file(self, data, data_path):
        """ 
        Reemplaza un fichero por otro en la ruta especificada. 

        Salida:
         0 Si todo va bien
        -1 Si no se encuentra el archivo o directorio
        -2 Si no se tienen permisos para acceder al archivo
        -3 Si ocurre cualquier otro error

        """

        try:
            with open(data_path, "wb") as f:
                f.write(data)
            return 0

        except (FileNotFoundError, IsADirectoryError):
            return -1
        except PermissionError:
            return -2
        except Exception:
            return -3
