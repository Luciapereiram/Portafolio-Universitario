/**
 * @file utils.c
 * @brief SOPER Proyecto Final
 *
 * @author Alejandro Ibáñez Pastrana
 * @author Lucía Pereira Menchero
 * @date 05/05/2023
 */

#define _POSIX_C_SOURCE 199309L

#include "utils.h"

/**
 * @brief Sets the handler for a signal.
 *
 * @param sa struct sigaction
 * @param signal signal to be handled
 * @param handler handler function
 */
int set_handler(struct sigaction *sa, int signal, void (*handler)(int))
{
    sa->sa_handler = handler;
    sigemptyset(&(sa->sa_mask));
    sa->sa_flags = 0;
    if (sigaction(signal, sa, NULL) < 0)
    {
        return ERR;
    }

    return OK;
}