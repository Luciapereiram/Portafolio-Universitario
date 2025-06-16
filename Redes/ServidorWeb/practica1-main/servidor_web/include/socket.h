/**
 * @file socket.h
 * 
 * @author Iker Manuel Perez
 * @author Lucia Pereira
 * 
 * @brief Fichero cabecera de la implementacion de sockets
 * 
 */

#ifndef socket_h
#define socket_h

#include "include_general.h"

#define MAX_BUFFER_SIZE 1024
#define NORMAL_BUFFER 128
#define MAX_LINE_LENGTH 100
#define NUM_LINES_CONFIG 4

/**
 * @brief Estructura para guardar clave-valor del fichero de configuracion
 */
typedef struct
{
  char clave[MAX_LINE_LENGTH];
  char valor[MAX_LINE_LENGTH];
} Config;

/**
 * @brief Funcion que devuelve un diccionario clave-valor
 * del fichero de configuracion 'server.conf'
 *
 * @return 0 si todo sale bien, -1 en caso de error
 */
int get_conf_struct(Config **dic);

/**
 * @brief Funcion que devuelve un determinado valor del
 * fichero de configuracion
 *
 * @param key clave cuyo valor se quiere obtener
 *
 * @return 0 si todo sale bien, -1 en caso de error o de no encontrar
 * la clave en el fichero de configuracion
 */
int get_conf_value(char *key, char *value);

/**
 * @brief Funcion que crea socket de servidor, lo enlaza y lo pone
 * en estado 'LISTEN'
 *
 * @param port puerto donde escucha el servidor
 * @param max_clients num maximo de clientes
 *
 * @return valor en formato string
 */
int create_server_socket(int port, int max_clients);

/**
 * @brief Funcion que acepta la conexion de un cliente
 * 
 * @param server_fd descriptor del servidor
 * 
 * @return descriptor de la nueva conexion
 */
int accept_connection(int server_fd);

/**
 * @brief Funcion que acepta conexiones de clientes 
 * (funcion handle de un hilo servidor)
 * 
 * @param server_fd descriptor del servidor
 *
 * @return 0 si todo sale bien, -1 en caso de error
 */
void *process_clients(void *server_fd);

/**
 * @brief Funcion para responder a una peticion de una determinada conexion
 *
 * @param connection_fd descriptor de la conexion
 * @param message mensaje a enviar
 * @param size tamanyo del mensaje
 * @param flags banderas
 *
 * @return 0 si todo sale bien, -1 en caso de error
 */
int respond(int connection_fd, char *message, int size, int flags);

/**
 * @brief Funcion que cierra un socket
 *
 * @param fd descriptor del socket
 *
 * @return 0 si todo sale bien, -1 en caso de error
 */
int close_fd(int fd);

#endif
