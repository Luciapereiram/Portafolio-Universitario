/**
 * @file servidor.c
 * 
 * @author Iker Manuel Perez
 * @author Lucia Pereira
 * 
 * @brief Implementacion de la funcionalidad del servidor web
 *
 */

#include "include_general.h"

int main()
{
    int server_fd = 0;
    int i = 0, max_clients = 0, port = 0;
    pthread_t *threads; // Array de hilos
    char port_str[NORMAL_BUFFER], max_clients_str[NORMAL_BUFFER];

    bzero(port_str, NORMAL_BUFFER);
    bzero(max_clients_str, NORMAL_BUFFER);

    if (get_conf_value("listen_port", port_str) == -1)
    {
        perror("[servidor.c] get_conf_value");
        return -1;
    }

    if (get_conf_value("max_clients", max_clients_str) == -1)
    {
        perror("[servidor.c] get_conf_value");
        return -1;
    }

    max_clients = atoi(max_clients_str);
    port = atoi(port_str);

    threads = (pthread_t *)malloc(max_clients * sizeof(pthread_t));
    if (!threads)
    {
        perror("[servidor.c] malloc");
        return -1;
    }

    /* Crear socket y poner a la escucha */
    if ((server_fd = create_server_socket(port, max_clients)) == -1)
    {
        perror("[servidor.c] create_socket");
        return -1;
    }

    printf("Escuchando en el puerto %d...\n", port);

    for (i = 0; i < max_clients; i++)
    {
        /* Creacion de hilos para atender peticiones */
        if (pthread_create(&threads[i], NULL, process_clients, &server_fd) != 0)
        {
            perror("[servidor.c] pthread_create");
            return -1;
        }
    }

    for (i = 0; i < max_clients; i++)
    {
        if (pthread_join(threads[i], NULL) != 0)
        {
            perror("[servidor.c] pthread_join");
            return -1;
        }
    }

    return 0;
}

