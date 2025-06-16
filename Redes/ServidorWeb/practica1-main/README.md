# practica1

## Ejecucion de la practica
Para ejecutar el servidor, primeramente se debe compilar todo con 'make' y ejecutar **./bin/servidor**. 
De esta manera el servidor se establece en el puerto 8080.

Desde el navegador, **localhost:8080/< recurso >** 
+ < recurso > puede ser un objeto de la carpeta /media/ o si se quisiera un objeto de la carpeta /script/
+ se puede pedir directamente /index.html

Adicionalmente se puede probar a hacer peticiones con el comando 'curl' desde la terminal, sobretodo si se quiere comprobar el funcionamiento del metodo OPTIONS (ejecutar curl -X OPTIONS http://localhost:8080 -v).

Para los ficheros multimedia, se adjunta en la wiki del proyecto la carpeta comprimida "media", la cual una vez descomprimida debera ubicarse en web_P1/www/ para poder probar el servidor de manera funcional. La carpeta "scripts" y el .html estan dentro del proyecto.

Para que el servidor localice la carpeta web_P1, debe modificarse el fichero de configuracion con el path correspondiente.

