/**
 * @file utils.h
 * @brief SOPER Proyecto Final
 *
 * @author Alejandro Ibáñez Pastrana
 * @author Lucía Pereira Menchero
 * @date 05/05/2023
 */

#ifndef _UTILS_H
#define _UTILS_H

#include <stdlib.h>
#include <signal.h>

#define ERR 0
#define OK 1

int set_handler(struct sigaction *sa, int signal, void (*handler)(int));

#endif