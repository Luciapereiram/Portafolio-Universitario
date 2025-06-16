from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Obtener el nombre del contenedor (o el hostname)
        hostname = socket.gethostname()

        # Imprimir "Hola mundo!" en la consola
        print("Hola mundo!")
        
        # Responder al cliente con un mensaje básico
        self.send_response(200)  # Código de respuesta HTTP 200 OK
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(f'Hola desde el servidor HTTP! Servido por: {hostname}'.encode())

# Configuración del servidor
HOST = '0.0.0.0'
PORT = 8000

# Crear y ejecutar el servidor
httpd = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
print(f"Servidor ejecutándose en http://{HOST}:{PORT}")
httpd.serve_forever()
