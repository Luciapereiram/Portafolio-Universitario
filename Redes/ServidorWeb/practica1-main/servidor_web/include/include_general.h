/**
 * @file include_general.h
 * 
 * @author Iker Manuel Perez
 * @author Lucia Pereira
 * 
 * @brief Fichero cabecera general, donde se incluyen todas las bibliotecas 
 * y declaraciones necesarias para el funcionamiento del servidor
 * 
 */
#ifndef include_general_h
#define include_general_h

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <pthread.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>
#include <assert.h>
#include <time.h>

#include "socket.h"
#include "peticiones_http.h"

#define CHAR_SIZE 30

#endif