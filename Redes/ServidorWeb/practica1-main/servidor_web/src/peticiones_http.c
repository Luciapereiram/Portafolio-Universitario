/**
 * @file peticiones_http.c
 * 
 * @author Iker Manuel Perez
 * @author Lucia Pereira
 * 
 * @brief Implementacion de la funcionalidad de http
 *
 */

#include "peticiones_http.h"
#include <time.h>

/**
 * @brief Funcion para limpiar el contenido de los buffers
 *
 * @param buf buffer
 * @param tam tamanyo del buffer
 */
void limpiar_buf(char *buf, int tam)
{
    bzero(buf, tam);
}

int handle_client(int connection_fd)
{
    /* ----- Codigo basado en el Github de la libreria picohttpparser ----- */
    char buf[MAX_BUFFER_SIZE];
    const char *method, *path;
    int parse_ret, minor_version;
    struct phr_header headers[100];
    size_t buflen = 0, prevbuflen = 0, method_len = 0, path_len = 0, num_headers = 0;
    ssize_t ret;

    while (1)
    {
        /* Leer peticion */
        limpiar_buf(buf, MAX_BUFFER_SIZE);
        while ((ret = read(connection_fd, buf + buflen, sizeof(buf) - buflen)) == -1 && errno == EINTR)
            ;

        if (ret < 0)
        {
            return -1;
        }
        else if (ret == 0)
        {
            return -2; // Cliente ha cerrado conexion
        }

        prevbuflen = buflen;
        buflen += ret;

        /* Parsear peticion */
        num_headers = sizeof(headers) / sizeof(headers[0]);
        parse_ret = phr_parse_request(buf, buflen, &method, &method_len, &path, &path_len,
                                      &minor_version, headers, &num_headers, prevbuflen);

        if (parse_ret > 0)
        {
            break; /* Parseo realizado correctamente */
        }
        else if (parse_ret == -1)
        {
            printf("[peticiones_http.c] ParseError\n");
            generate_response(0, 1, BAD_REQUEST, connection_fd, NULL);
            return -1;
        }
        /* Peticion incompleta -> continuar bucle */
        assert(parse_ret == -2);
        if (buflen == sizeof(buf))
        {
            printf("[peticiones_http.c] RequestIsTooLongError\n");
            generate_response(0, 1, BAD_REQUEST, connection_fd, NULL);
            return -1;
        }
    }
    /* --------------------------------------------------------------------- */

    /*
     *  Tras parsear la peticion, se obtiene el metodo y la ruta (no completa).
     *  Dependiendo del metodo y el fichero, se lleva a cabo una accion u otra.
     */

    char final_path[NORMAL_BUFFER], path_aux[NORMAL_BUFFER], method_str[NORMAL_BUFFER];
    char *script_name = NULL, *args_get = NULL, *args_post = NULL; // para los scripts
    int is_a_script = 0, err = 0;

    limpiar_buf(method_str, NORMAL_BUFFER);
    strncpy(method_str, method, (int)method_len);

    limpiar_buf(path_aux, NORMAL_BUFFER);
    if (get_conf_value("server_root", path_aux) == -1)
    {
        perror("[peticiones_http.c] get_conf_value");
        return -1;
    }

    strncat(path_aux, path, (int)path_len);
    strcpy(final_path, path_aux);

    /* Comprobar si la peticion implica ejecutar un script */
    if (strchr(path_aux, '?') != NULL)
    {
        is_a_script = 1;

        script_name = strtok(final_path, "?");
        if (!script_name)
        {
            perror("[peticiones_http.c] strtok");
            return -1;
        }

        args_get = strdup(strchr(path_aux, '?'));
        args_get++; // a partir de '?' son argumentos en la url
    }

    /* Peticion metodo GET */
    if (strcmp(method_str, "GET") == 0)
    {
        if (is_a_script == 1)
        {
            if (process_script_request(script_name, minor_version, connection_fd, args_get, NULL) == -1)
            {
                perror("[peticiones_http.c] process_script_request");
                err = -1;
            }

            if (args_get != NULL)
            {
                args_get--;
                free(args_get);
            }
        }
        else
        {
            if (process_GET_request(final_path, minor_version, connection_fd) == -1)
            {
                perror("[peticiones_http.c] process_GET_request");
                err = -1;
            }
        }
    }
    /* Peticion metodo POST */
    else if (strcmp(method_str, "POST") == 0)
    {
        args_post = strdup(buf + parse_ret); // a partir de la peticion como tal son argumentos en el content

        if (process_POST_request(final_path, minor_version, connection_fd, args_get, args_post) == -1)
        {
            perror("[peticiones_http.c] process_POST_request");
            err = -1;
        }

        if (args_get != NULL)
        {
            args_get--;
            free(args_get);
        }

        free(args_post);
    }
    /* Peticion metodo OPTIONS */
    else if (strcmp(method_str, "OPTIONS") == 0)
    {
        if (process_OPTIONS_request(final_path, minor_version, connection_fd) == -1)
        {
            perror("[peticiones_http.c] process_OPTIONS_request");
            err = -1;
        }
    }
    /* Verbo no admitido */
    else
    {
        if (generate_response(final_path, minor_version, BAD_REQUEST, connection_fd, NULL) == -1) // 400 Bad Request
        {
            perror("[peticiones_http.c] generate_response");
            err = -1;
        }
    }

    return err;
}

int process_GET_request(char *path, int version, int connection_fd)
{
    FILE *file = NULL;
    HTTP_Code code = OK;

    /* Control de argumentos */
    if (!path || (version != 1 && version != 0))
    {
        perror("[peticiones_http.c] Incompatibilidad de argumentos");
        code = BAD_REQUEST;
    }

    /* Comprobar si la ruta es valida */
    file = fopen(path, "rb");
    if (!file)
    {
        perror("[peticiones_http.c 1] fopen");
        code = NOT_FOUND;
    }
    else
    {
        fclose(file);
    }

    /* Enviar respuesta en funcion del codigo */
    if (generate_response(path, version, code, connection_fd, NULL) == -1)
    {
        perror("[peticiones_http.c] generate_response");
        return -1;
    }

    return 0;
}

/**
 * @brief Funcion privada. Formatear los argumentos de un script
 *
 * @param args string con los argumentos separados por &
 * @param symbol simbolo a intercalar entre los argumentos
 */
void format_args(char *args, char symbol)
{
    char *arg = NULL;

    arg = strchr(args, '&');

    while (arg != NULL)
    {
        int index = arg - args;
        args[index] = symbol;
        arg = strchr(arg + 1, '&');
    }
}

int process_script_request(char *path, int version, int connection_fd, char *args_get, char *args_post)
{
    FILE *file = NULL;
    HTTP_Code code = OK;
    char *ext = NULL;
    char command[NORMAL_BUFFER], script[MAX_BUFFER_SIZE];

    /* Control de argumentos */
    if (!path || (version != 1 && version != 0))
    {
        perror("[peticiones_http.c] Incompatibilidad de argumentos");
        code = BAD_REQUEST;
    }

    limpiar_buf(command, NORMAL_BUFFER);
    limpiar_buf(script, MAX_BUFFER_SIZE);

    /* Comprobar si la ruta es valida */
    file = fopen(path, "rb");
    if (!file)
    {
        perror("[peticiones_http.c 1] fopen");
        code = NOT_FOUND;
    }
    else
    {
        fclose(file);
    }

    /* Recoger la extension del fichero a ejecutar */
    ext = strrchr(path, '.'); // devuelve puntero al ultimo '.' que aparezca
    if (!ext)
    {
        perror("[peticiones_http.c] strrchr");
    }
    else
    {
        ext = strdup(ext + 1);
    }

    /* En funcion de la extension, se ejecuta un comando u otro */

    if (strcmp(ext, "py") == 0) // fichero python
    {
        strcpy(command, "python3");
    }
    else if (strcmp(ext, "php") == 0) // fichero php
    {
        strcpy(command, "php");
    }
    else
    {
        perror("[peticiones_http.c] extension del script no admitido");
        code = BAD_REQUEST;
    }
    free(ext);

    // Ejemplo peticion -> GET /scripts/backend.py?var1=abcd&var2=efgh

    if (args_get != NULL && args_post != NULL) // hay argumentos GET/POST
    {
        /* Recoger los argumentos */
        format_args(args_get, ' ');

        /* Recoger los argumentos */
        format_args(args_post, '\n');

        /* Genera el string del script */
        sprintf(script, "echo '%s' | %s %s %s", args_post, command, path, args_get);

        // printf("script a ejecutar -> %s", script);
    }
    else if (args_post != NULL) // hay solo argumentos POST
    {
        /* Recoger los argumentos */
        format_args(args_post, '\n');

        /* Genera el string del script */
        sprintf(script, "echo '%s' | %s %s", args_post, command, path);

        // printf("script a ejecutar -> %s", script);
    }
    else if (args_get != NULL) // hay solo argumentos GET
    {
        /* Recoger los argumentos */
        format_args(args_get, ' ');

        /* Genera el string del script */
        sprintf(script, "%s %s %s", command, path, args_get);

        // printf("script a ejecutar -> %s", script);
    }

    if (generate_response(path, version, code, connection_fd, script) == -1)
    {
        perror("[peticiones_http.c] generate_response");
        return -1;
    }

    return 0;
}

int process_POST_request(char *path, int version, int connection_fd, char *args_get, char *args_post)
{
    if (process_script_request(path, version, connection_fd, args_get, args_post) == -1)
    {
        perror("[peticiones_http.c] process_script_request");
        return -1;
    }

    return 0;
}

int process_OPTIONS_request(char *path, int version, int connection_fd)
{
    char response[MAX_BUFFER_SIZE];
    char date[MAX_BUFFER_SIZE], server[NORMAL_BUFFER];
    time_t now = time(NULL);
    struct tm *t = localtime(&now);

    /* Control de argumentos */
    if ((version != 1 && version != 0))
    {
        perror("[http.c] Version no compatible\n");
        generate_response(path, 1, BAD_REQUEST, connection_fd, NULL);
        return -1;
    }

    /* Limpiar contenido de los buffers para evitar errores */
    limpiar_buf(response, MAX_BUFFER_SIZE);
    limpiar_buf(date, MAX_BUFFER_SIZE);
    limpiar_buf(server, NORMAL_BUFFER);

    /* Fecha actual */
    strftime(date, sizeof(date) - 1, "%a, %d %b %Y %X %Z", t);

    /* Nombre del servidor */
    if (get_conf_value("server_signature", server))
    {
        perror("[peticiones_http.c] get_conf_vale");
    }

    /* Generar la respuesta */
    strcat(response, "HTTP/1.1 200 OK\r\n");
    strcat(response, "Date: ");
    strcat(response, date);
    strcat(response, "\r\n");
    strcat(response, "Server: ");
    strcat(response, server);
    strcat(response, "\r\n");
    strcat(response, "Allow: GET, POST, OPTIONS\r\n");
    strcat(response, "Content-Length: 0\r\n\r\n");

    /* Enviar la respuesta */
    if (respond(connection_fd, response, strlen(response), 0) == -1)
    {
        perror("[peticiones_http.c] respond\n");
        return 1;
    }

    return 0;
}

/**
 * @brief Funcion privada. Genera en formato string el tipo de contenido del recurso
 *
 * @param file_ext extension del recurso
 * @param c_type formato correspondiente a dicha extension
 *
 * @return 0 si todo sale bien, -1 en caso de error
 */
int get_content_type(char *file_ext, char *c_type)
{
    if (strcasecmp(file_ext, "html") == 0 || strcasecmp(file_ext, "htm") == 0)
    {
        strcpy(c_type, "text/html");
    }
    else if (strcasecmp(file_ext, "txt") == 0 || strcasecmp(file_ext, "py") == 0 || strcasecmp(file_ext, "php") == 0)
    {
        strcpy(c_type, "text/plain");
    }
    else if (strcasecmp(file_ext, "jpg") == 0 || strcasecmp(file_ext, "jpeg") == 0)
    {
        strcpy(c_type, "image/jpeg");
    }
    else if (strcasecmp(file_ext, "gif") == 0)
    {
        strcpy(c_type, "image/gif");
    }
    else if (strcasecmp(file_ext, "mpeg") == 0 || strcasecmp(file_ext, "mpg") == 0)
    {
        strcpy(c_type, "video/mpeg");
    }
    else if (strcasecmp(file_ext, "doc") == 0 || strcasecmp(file_ext, "docx") == 0)
    {
        strcpy(c_type, "application/msword");
    }
    else if (strcasecmp(file_ext, "pdf") == 0)
    {
        strcpy(c_type, "application/pdf");
    }
    else
    {
        return -1;
    }

    return 0;
}

/**
 * @brief Funcion privada. Genera en formato string la respuesta HTPP
 *
 * @return 0 si todo sale bien, -1 en caso de error
 */
int create_response_str(HTTP_Response *rp, char *response)
{
    char content[MAX_BUFFER_SIZE], aux[MAX_BUFFER_SIZE];

    if (!rp)
    {
        return -1;
    }

    limpiar_buf(aux, MAX_BUFFER_SIZE);
    limpiar_buf(content, MAX_BUFFER_SIZE);

    sprintf(aux, "HTTP/1.%d %d %s\r\n", rp->version, rp->code, rp->message);
    strcat(response, aux);

    sprintf(aux, "Date: %s\r\n", rp->date);
    strcat(response, aux);

    sprintf(aux, "Server: %s\r\n", rp->server);
    strcat(response, aux);

    /* En caso de ocurrir algun error */
    if (rp->code == 400 || rp->code == 404)
    {
        sprintf(aux, "Content-Type: text/html; charset=UTF-8\r\n");
        strcat(response, aux);

        sprintf(content, "<!DOCTYPE html>\n<html>\n<head>\n<title>Error %d - %s</title>\n</head>\n<body>\n<h1>Error %d - %s</h1>\n</body>\n</html>\n", rp->code, rp->message, rp->code, rp->message);
        rp->c_length = strlen(content);

        sprintf(aux, "Content-Length: %d\r\n\r\n", rp->c_length);
        strcat(response, aux);

        strcat(response, content); // datos

        return 1;
    }

    /* Si todo va bien, se genera respuesta de codigo 200 */
    sprintf(aux, "Last-Modified: %s\r\n", rp->last_modified);
    strcat(response, aux);

    sprintf(aux, "Content-Type: %s\r\n", rp->c_type);
    strcat(response, aux);

    sprintf(aux, "Content-Length: %d\r\n\r\n", rp->c_length);
    strcat(response, aux);

    return 0;
}

int generate_response(char *path, int version, HTTP_Code code, int connection_fd, char *script)
{
    char response[MAX_BUFFER_SIZE], line[NORMAL_BUFFER], script_content[MAX_BUFFER_SIZE];
    HTTP_Response *response_values = NULL;
    time_t now = time(NULL);
    struct tm *tm = localtime(&now);
    struct stat state;
    FILE *file = NULL, *pipe = NULL;
    char aux[MAX_BUFFER_SIZE], *ext = NULL;
    int ret = 0, bytes_read = 0, flag = 0, response_func = 0;

    response_values = (HTTP_Response *)malloc(sizeof(HTTP_Response));
    if (!response_values)
    {
        perror("[peticiones_http.c] malloc");
        return -1;
    }

    /* Limpiar todos los buffers para evitar errores en el contenido */
    limpiar_buf(response_values->c_type, NORMAL_BUFFER);
    limpiar_buf(response_values->date, NORMAL_BUFFER);
    limpiar_buf(response_values->last_modified, NORMAL_BUFFER);
    limpiar_buf(response_values->message, NORMAL_BUFFER);
    limpiar_buf(response_values->server, NORMAL_BUFFER);
    limpiar_buf(response, MAX_BUFFER_SIZE);
    limpiar_buf(aux, MAX_BUFFER_SIZE);

    /* Ir recogiendo cada uno de los datos de la respuesta HTTP y
     *  y guardarlos en los campos correspondientes de la estructura
     */

    /* Version */
    response_values->version = version;

    /* Comprobar codigo de respuesta */
    if (code == BAD_REQUEST)
    {
        response_values->code = 400;
        strcpy(response_values->message, "Bad Request");
        ret = -1;
    }
    else if (code == NOT_FOUND)
    {
        response_values->code = 404;
        strcpy(response_values->message, "Not found");
    }
    else if (code == OK)
    {
        response_values->code = 200;
        strcpy(response_values->message, "OK");
    }

    /* Fecha actual */
    strftime(response_values->date, sizeof(response_values->date) - 1, "%a, %d %b %Y %X %Z", tm);
    // printf("Time is: [%s]\n", response_values->date);

    /* Nombre del servidor */
    if (get_conf_value("server_signature", aux) == -1)
    {
        perror("[peticiones_http.c] get_conf_value");
        ret = -1;
    }
    strcpy(response_values->server, aux);

    /* Datos del recurso solicitado */
    if (ret != -1)
    {
        /* Fecha ultima modificacion */
        if (stat(path, &state) == -1)
        {
            perror("[peticiones_http.c] stat");
        }
        else
        {
            strftime(response_values->last_modified, sizeof(response_values->last_modified) - 1, "%a, %d %b %Y %X %Z", localtime(&state.st_mtime));
        }

        /* Longitud */
        if (!script)
        {
            file = fopen(path, "rb");
            if (!file)
            {
                perror("[peticiones_http.c 2] fopen");
            }
            else
            {
                fseek(file, 0, SEEK_END);
                response_values->c_length = ftell(file);
                fclose(file);
            }
        }
        else
        {
            pipe = popen(script, "r");
            if (!pipe)
            {
                printf("[peticiones_http.c] popen");
                free(response_values);
                return -1;
            }

            limpiar_buf(script_content, MAX_BUFFER_SIZE);

            while (fgets(line, sizeof(line), pipe) != NULL)
            {
                strcat(script_content, line);
                limpiar_buf(line, NORMAL_BUFFER);
            }
            pclose(pipe);

            response_values->c_length = strlen(script_content);
        }

        /* Tipo de contenido */
        ext = strrchr(path, '.'); // devuelve puntero al ultimo '.' que aparezca
        if (!ext)
        {
            perror("[peticiones_http.c] strrchr");
        }
        else
        {
            ext = strdup(ext + 1);
            if (get_content_type(ext, response_values->c_type) == -1)
            {
                perror("[peticiones_http.c] get_content_type");
            }

            free(ext);
        }
    }

    /* Generar respuesta */
    if ((response_func = create_response_str(response_values, response)) == -1)
    {
        perror("[peticiones_http.c] create_response_str");
    }

    /* Respuesta de error */
    if (response_func == 1)
    {
        /* Enviar cabecera de la respuesta */
        if (respond(connection_fd, response, strlen(response), flag) == -1)
        {
            perror("[peticiones_http.c] respond");
            free(response_values);
            return -1;
        }

        free(response_values);
        return 0;
    }

    /* Respuesta de ok */

    /* Enviar cabecera de la respuesta */
    if (respond(connection_fd, response, strlen(response), MSG_MORE) == -1)
    {
        perror("[peticiones_http.c] respond");
        free(response_values);
        return -1;
    }

    /* Enviar cuerpo de la respuesta */
    if (!script)
    {
        file = fopen(path, "rb");
        if (!file)
        {
            perror("[peticiones_http.c 3] fopen");
            free(response_values);
            return -1;
        }

        flag = MSG_MORE;
        limpiar_buf(response, MAX_BUFFER_SIZE);
        while (!feof(file))
        {
            bytes_read = fread(response, 1, sizeof(response), file);

            /* Final del fichero */
            if (feof(file))
            {
                flag = 0;
            }

            if (respond(connection_fd, response, bytes_read, flag) == -1)
            {
                perror("[peticiones_http.c] respond");
                free(response_values);
                fclose(file);
                return -1;
            }
        }

        fclose(file);
    }
    else
    {
        strcat(script_content, "\r\n");

        if (respond(connection_fd, script_content, strlen(script_content), flag) == -1)
        {
            perror("[peticiones_http.c] respond");
            free(response_values);
            return -1;
        }
    }

    free(response_values);

    return 0;
}
