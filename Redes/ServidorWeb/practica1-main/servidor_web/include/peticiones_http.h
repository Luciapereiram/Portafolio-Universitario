/**
 * @file peticiones_http.h
 * 
 * @author Iker Manuel Perez
 * @author Lucia Pereira
 * 
 * @brief Fichero cabecera de la funcionalidad de http
 * 
 */

#ifndef peticiones_http_h
#define peticiones_http_h

#include "picohttpparser.h"
#include "include_general.h"

#define NORMAL_BUFFER 128
#define MAX_BUFFER_SIZE 1024

/**
 * @brief Estructura respuesta HTTP
*/
typedef struct
{
  int version;                          /*!< Version */
  int code;                             /*!< Codigo de respuesta */
  char message[NORMAL_BUFFER];          /*!< Mensaje */
  char date[NORMAL_BUFFER];             /*!< Fecha */
  char server[NORMAL_BUFFER];           /*!< Servidor */
  char last_modified[NORMAL_BUFFER];    /*!< Fecha ultima modificacion */
  int c_length;                         /*!< Longitud de contenido */    
  char c_type[NORMAL_BUFFER];           /*!< Tipo de contenido */
} HTTP_Response;

/**
 * @brief Estructura para el script a ejecutar
*/
typedef struct
{
  char ext[NORMAL_BUFFER];              /*!< Extension del fichero */
  char command[NORMAL_BUFFER];          /*!< Comando a ejecutar */
} Script_request;

/**
 * @brief Estructura para los codigos de respuesta
*/
typedef enum enum_HTTP_Code
{
  BAD_REQUEST,
  NOT_FOUND,
  OK
} HTTP_Code;

/**
 * @brief Funcion manejo del cliente. Cada hilo del servidor ejecuta esta funcion para
 * atender a los clientes que se conecten.
 * 
 * @param connection_fd descriptor de la conexion
 * 
 * @return 0 si todo sale bien, -1 en caso de error 
*/
int handle_client(int connection_fd);

/**
 * @brief Funcion para procesar una peticion de tipo GET
 * 
 * @param path ruta del recurso a consumir
 * @param version version HTTP
 * @param connection_fd descriptor de la conexion
 * 
 * @return 0 si todo sale bien, -1 en caso de error  
 */
int process_GET_request(char *path, int version, int connection_fd);

/**
 * @brief Funcion para procesar una peticion de tipo GET con un script. 
 * El servidor debe ejecutar dicho script y proporcionar la salida de este al cliente.
 * 
 * @param path ruta del recurso a consumir
 * @param version version HTTP
 * @param connection_fd descriptor de la conexion
 * @param args_get argumentos en metodo get (desde la URL)
 * @param args_post argumentos en metodo post (desde content)
 * 
 * @return 0 si todo sale bien, -1 en caso de error  
 */
int process_script_request(char *path, int version, int connection_fd, char *args_get, char *args_post);

/**
 * @brief Funcion para procesar una peticion de tipo POST
 * 
 * @param path ruta del recurso a consumir
 * @param version version HTTP
 * @param connection_fd descriptor de la conexion
 * @param args_get argumentos en metodo get (desde la URL)
 * @param args_post argumentos en metodo post (desde content)
 * 
 * @return 0 si todo sale bien, -1 en caso de error  
 */
int process_POST_request(char *path, int version, int connection_fd, char *args_get, char *args_post);

/**
 * @brief Funcion para procesar una peticion de tipo OPTIONS
 * 
 * @param path ruta del recurso a consumir
 * @param version version HTTP
 * @param connection_fd descriptor de la conexion
 * 
 * @return 0 si todo sale bien, -1 en caso de error  
 */
int process_OPTIONS_request(char *path, int version, int connection_fd);

/**
 * @brief Funcion para generar una respuesta HTTP
 * 
 * @param path ruta del recurso a consumir
 * @param version version HTTP
 * @param code codigo de respuesta
 * @param server_fd descriptor del servidor
 * @param script script en caso de que sea una peticion para ejecucion
 * 
 * @return 0 si todo sale bien, -1 en caso de error   
 */
int generate_response(char *path, int version, HTTP_Code code, int connection_fd, char *script);

#endif