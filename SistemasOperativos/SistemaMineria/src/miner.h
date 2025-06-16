/**
 * @file miner.h
 * @brief SOPER Proyecto Final
 *
 * @author Alejandro Ibáñez Pastrana
 * @author Lucía Pereira Menchero
 * @date 05/05/2023
 */

#ifndef _MINER_H
#define _MINER_H

#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <pthread.h>

#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <mqueue.h>
#include <semaphore.h>

#include <signal.h>

#include <math.h> 
#include <time.h>
#include <errno.h>

#include "pow.h"
#include "utils.h"

#define MAX_SHORT_WAITS 1000 /*!< Max number of short waits */
#define INIT_OBJECTIVE 0     /*!< Initial objective of the pow hash function */
#define MAX_MINERS 100       /*!< Max number of miners in the system */
#define NO_VOTE -1           /*!< No vote value */
#define VOTE_YES 1           /*!< Yes vote value */
#define VOTE_NO 0            /*!< No vote value */

#define SHM_NAME "/shm_miner"           /*!< Name of the shared memory between miners */
#define MQ_NAME "/mq_miner"             /*!< Name of the message queue */
#define MQ_MAX_MSJ 7                    /*!< Maximum number of messages in the queue */
#define MQ_MSJ_SIZE sizeof(POWRESULT)   /*!< Size of the messages in the queue */

#pragma pack(push, 1)

/**
 * @brief Structure of the challenge block
 */
typedef struct _POWRESULT
{
  int id;                         /*!< Round id */
  pid_t winner;                   /*!< Winner id */
  long target;                    /*!< Target of the pow hash function */
  long result;                    /*!< Result of the pow hash function */
  int accepted_votes;             /*!< Number of accepted votes */
  int total_votes;                /*!< Total number of votes */
  int miners[MAX_MINERS];         /*!< Each process pid */
  int wallets[MAX_MINERS];        /*!< Each process wallet */
  int flag;                       /*!< Flag to indicate if the block is valid */
} POWRESULT;

/**
 * @brief Struct to store the information of the miners.
 */
typedef struct _MINERINFO
{
  pid_t pid;
  int vote;
  int n_coins;
} MINERINFO;

/**
 * @brief Structure of the system shared memory
 */
typedef struct _SHMMINER
{
  MINERINFO miners[MAX_MINERS];   /*!< Miners information */
  int n_system;                   /*!< Number of miners registered  */
  POWRESULT last_block;           /*!< Last challenge block resolved */
  POWRESULT actual_block;         /*!< Actual challenge block */
  sem_t sem_winner;               /*!< Winner semaphore */
  sem_t sem_data;                 /*!< Data from shared memory semaphore */
} SHMMINER;

/**
 * @brief Arguments estructure to call the threads.
 * Used to send the arguments to the threads used to
 * find the element x that satisfies f(x) = target,
 * in a specific interval.
 */
typedef struct _SEARCHARGS
{
  int bottom; /*!< Bottom of the interval. */
  int top;    /*!< Top of the interval. */
  int target; /*!< Target of the pow hash function. */
} SEARCHARGS;

#pragma pack(pop)

void *search_pow(void *search_args);
int multithread_search_pow(int target, int nthreads);
int pid_register(SHMMINER *shm_struct);
void pid_unregister(SHMMINER *shm_struct);
int shm_init(SHMMINER *shm_struct);
void shm_destroy(SHMMINER *shm_struct);
void pregistrador(int fd_read);
void pminero(SHMMINER *shm_struct, sigset_t set, sigset_t oset, int fd_pipe, int nthreads);
void miner_exit(SHMMINER *shm_struct, int fd_pipe, int st);

#endif