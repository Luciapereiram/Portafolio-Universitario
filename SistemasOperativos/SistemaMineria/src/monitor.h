/**
 * @file monitor.h
 * @brief SOPER Proyecto Final
 *
 * @author Alejandro Ibáñez Pastrana
 * @author Lucía Pereira Menchero
 * @date 05/05/2023
 */

#ifndef _MONITOR_H
#define _MONITOR_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/mman.h>
#include <sys/stat.h>        
#include <fcntl.h> 

#include <sys/types.h>
#include <unistd.h>

#include <mqueue.h>
#include <semaphore.h>
#include <errno.h> 

#include "miner.h"
#include "pow.h"
#include "utils.h"

#define MONITORSHM_NAME "/shm_monitor"  /*!< Name of the shared memory */
#define BUFFER_DIM 5                    /*!< Dimension of the buffer of the shared memory */

/**
 * @brief Structure of the shared memory
 */
typedef struct _SHMMONITOR
{
  POWRESULT queue[BUFFER_DIM];  /*!< Pow results checked. */
  int head;                     /*!< Head of the queue. */
  int tail;                     /*!< Tail of the queue. */
  sem_t sem_mutex;              /*!< Semaphore mutex */
  sem_t sem_empty;              /*!< Semaphore empty */
  sem_t sem_fill;               /*!< Semaphore fill */
} SHMMONITOR;

int buffer_init(SHMMONITOR *shm_struct);
void buffer_destroy(SHMMONITOR *shm_struct);
void buffer_push(SHMMONITOR *shm_struct, POWRESULT msg);
POWRESULT buffer_pop(SHMMONITOR *shm_struct);
void pcomprobador(SHMMONITOR *shm_struct);
void pmonitor(SHMMONITOR *shm_struct);

#endif