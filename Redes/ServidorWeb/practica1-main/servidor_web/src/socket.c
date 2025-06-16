/**
 * @file socket.c
 * 
 * @author Iker Manuel Perez
 * @author Lucia Pereira
 * 
 * @brief Implementacion de la funcionalidad de sockets
 *
 */

#include "socket.h"

int get_conf_struct(Config **dic)
{
    FILE *file = NULL;
    char line[MAX_LINE_LENGTH];
    int i = 0;

    if ((file = fopen("server.conf", "r")) == NULL)
    {
        perror("[socket.c] fopen");
        return -1;
    }

    bzero(line, MAX_LINE_LENGTH);

    /* Leer archivo linea por linea para guardarlo en el diccionario */
    for (i = 0; fgets(line, sizeof(line), file) != NULL;)
    {
        /* No tener en cuenta lineas vacias o comentarios */
        if (line[0] == '#' || line[0] == '\n')
        {
            continue;
        }
        else
        {
            /* Obtener la clave y el valor */
            sscanf(line, "%s = %s", dic[i]->clave, dic[i]->valor);
            i++;
        }
    }

    fclose(file);

    return 0;
}

int get_conf_value(char *key, char *value)
{
    Config **dic_conf = NULL;
    int i = 0, find_value = 0;

    dic_conf = (Config **)malloc(NUM_LINES_CONFIG * sizeof(Config *));
    if (!dic_conf)
    {
        perror("[socket.c] malloc");
        return -1;
    }

    for (i = 0; i < NUM_LINES_CONFIG; i++)
    {
        dic_conf[i] = (Config *)malloc(sizeof(Config));
        if (!(dic_conf[i]))
        {
            for (i -= 1; i >= 0; i--)
            {
                free(dic_conf[i]);
            }

            perror("[socket.c] malloc");
            free(dic_conf);
            return -1;
        }
    }

    if (get_conf_struct(dic_conf) == -1)
    {
        perror("[socket.c] get_conf_struct");
        free(dic_conf);
        return -1;
    }

    /* Buscar la clave que coincide y devolverla en la variable 'value' */
    for (i = 0; i < NUM_LINES_CONFIG; i++)
    {
        if (strcmp(dic_conf[i]->clave, key) == 0)
        {
            strcpy(value, dic_conf[i]->valor);
            find_value = 1;
            break;
        }
    }

    for (i = 0; i < NUM_LINES_CONFIG; i++)
    {
        free(dic_conf[i]);
    }

    free(dic_conf);

    /* Si no se ha encontrado, devolver -1 */
    if (find_value == 0)
    {
        return -1;
    }

    return 0;
}

int create_server_socket(int port, int max_clients)
{
    int server_fd = 0;
    struct sockaddr_in address;

    /* Crear socket para el servidor */
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("[socket.c] socket");
        return -1;
    }

    address.sin_family = AF_INET;         /* Establecer tipo de direccion de socket en IPv4 */
    address.sin_addr.s_addr = INADDR_ANY; /* Establecer direccion IP */
    address.sin_port = htons(port);       /* Establecer puerto */

    /* Asociar socket a IP y puerto correctos */
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
    {
        perror("[socket.c] bind");
        return -1;
    }

    /* Socket escuchando */
    if (listen(server_fd, max_clients) < 0)
    {
        perror("[socket.c] listen");
        return -1;
    }

    return server_fd;
}

int accept_connection(int server_fd)
{
    struct sockaddr serverStorage;
    unsigned int addr_size;
    int new_connection = 0;

    new_connection = accept(server_fd, &serverStorage, &addr_size);

    if (new_connection == -1)
    {
        perror("[sockets.c] accept");
        return -1;
    }

    return new_connection;
}

// Funcion de ejecucion para cada hilo
void *process_clients(void *server_fd)
{
    int new_connection = 0, handle_func = 0;

    /* Esperar una conexion */
    while (1)
    {
        /* Aceptar conexion (bloqueante) */
        if ((new_connection = accept_connection(*((int *)server_fd))) == -1)
        {
            perror("[socket.c] accept");
            return NULL;
        }

        /* Informar de que se ha conectado un cliente */
        printf("\nConexion aceptada\n");

        while (1)
        {
            /* Atender peticion */
            handle_func = handle_client(new_connection);
            if (handle_func == -1)
            {
                perror("[socket.c] Error al procesar peticion del cliente");
            }
            else if (handle_func == -2)
            {
                printf("[socket.c] Se ha cerrado la conexion por parte del cliente");
                break;
            }

            printf("\nPeticion recibida...\n");
        }

        /* Cerrar conexion */
        if (close_fd(new_connection) == -1)
        {
            perror("[socket.c] close_fd");
        }
    }
}

int respond(int connection_fd, char *message, int size, int flags)
{
    ssize_t bytes_sent = 0;

    if ((bytes_sent = send(connection_fd, message, size, flags)) == -1)
    {
        perror("[socket.c] send");
        return -1;
    }

    return bytes_sent;
}

int receive(int connection_fd, char *message){

    ssize_t bytes_recv;

    if ((bytes_recv = recv(connection_fd, message, MAX_BUFFER_SIZE, 0)) == -1)
    {
        perror("[socket.c] recv");
        return -1;
    }

    return bytes_recv;
}

int close_fd(int fd)
{
    return close(fd);
}
