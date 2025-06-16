/**
 * @file miner.c
 * @brief SOPER Proyecto Final
 *
 * @author Alejandro Ibáñez Pastrana
 * @author Lucía Pereira Menchero
 * @date 05/05/2023
 */

#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "miner.h"

/* GLOBAL VARIABLES */

int result;                      /*!< Result of the pow hash function. */
static volatile int sigusr1 = 0; /*!< SIGUSR1 signal flag. */
static volatile int sigusr2 = 0; /*!< SIGUSR2 signal flag. */
static volatile int sigalrm = 0; /*!< SIGALRM signal flag. */
static volatile int sigint = 0;  /*!< SIGINT signal flag. */

/* HANDLER FUNCTIONS */

void handler_SIGUSR1() { sigusr1 = 1; }
void handler_SIGUSR2() { sigusr2 = 1; }
void handler_SIGALRM() { sigalrm = 1; }
void handler_SIGINT() { sigint = 1; }

/**
 * @brief Find the element x that satisfies f(x) = target, in a specific interval.
 *
 * @param search_args SEARCHARGS structure with the arguments to call the thread.
 */
void *search_pow(void *search_args)
{
    int x;

    for (x = ((SEARCHARGS *)search_args)->bottom; x <= ((SEARCHARGS *)search_args)->top && result == -1 && sigusr2 == 0; x++)
    {
        if (((SEARCHARGS *)search_args)->target == pow_hash(x))
        {
            result = x;
            break;
        }
    }

    return NULL;
}

/**
 * @brief Create threads which call search_pow function in different intervals.
 *
 * @param target Target of the pow hash function.
 * @param nthreads Number of threads used to search the pow hash function.
 * @return OK (0) or in case of error ERR (-1).
 */
int multithread_search_pow(int target, int nthreads)
{
    SEARCHARGS *thread_args;
    pthread_t *threadids;

    int i = 0;
    int ret = 0;
    int st = OK;

    /* mem alloc for search interval structure and thread ids */
    thread_args = (SEARCHARGS *)malloc(nthreads * sizeof(SEARCHARGS));
    if (!thread_args)
    {
        return ERR;
    }

    threadids = (pthread_t *)malloc(nthreads * sizeof(pthread_t));
    if (!threadids)
    {
        free(thread_args);
        return ERR;
    }

    /* set search intervals */
    for (i = 0; i < nthreads; i++)
    {
        thread_args[i].target = target;
        thread_args[i].top = ceil(POW_LIMIT / (double)nthreads * (i + 1));
        if (i > 0)
        {
            thread_args[i].bottom = thread_args[i - 1].top + 1;
        }
        else
        {
            thread_args[i].bottom = 0;
        }
    }

    /* search each interval in different threads */
    result = -1;
    for (i = 0; i < nthreads && st == OK; i++)
    {
        ret = pthread_create(&threadids[i], NULL, search_pow, &thread_args[i]);
        if (ret != 0)
        {
            fprintf(stderr, "pthread_create: %s\n", strerror(ret));
            st = ERR;
        }
    }

    /* close threads */
    for (i = 0; i < nthreads && st == OK; i++)
    {
        ret = pthread_join(threadids[i], NULL);
        if (ret != 0)
        {
            fprintf(stderr, "pthread_join: %s\n", strerror(ret));
            st = ERR;
        }
    }

    /* free mem */
    free(thread_args);
    free(threadids);

    return st;
}

/**
 * @brief Registers a new miner in the system.
 *
 * @param shm_struct SHMMINER structure with the shared memory.
 * @return OK (0) or in case of error ERR (-1).
 */
int pid_register(SHMMINER *shm_struct)
{
    int i = 0;

    sem_wait(&(shm_struct->sem_data));

    if (shm_struct->n_system == MAX_MINERS)
    {
        sem_post(&(shm_struct->sem_data));
        return ERR;
    }

    /* walk through the array of miners and look for a hole */
    while (shm_struct->miners[i].pid != -1)
    {
        i++;
    }

    /* register its pid */
    shm_struct->miners[i].pid = getpid();
    shm_struct->miners[i].n_coins = 0;

    /* increase the number of miners registered */
    (shm_struct->n_system)++;

    sem_post(&(shm_struct->sem_data));

    return OK;
}

/**
 * @brief Unregisters a miner from the system.
 *
 * @param shm_struct SHMMINER structure with the shared memory.
 */
void pid_unregister(SHMMINER *shm_struct)
{
    int i;
    pid_t pid = getpid();

    sem_wait(&(shm_struct->sem_data));

    /* remove its information from the system */
    for (i = 0; i < MAX_MINERS; i++)
    {
        if (shm_struct->miners[i].pid == pid)
        {
            shm_struct->miners[i].pid = -1;
            shm_struct->miners[i].vote = NO_VOTE;
            shm_struct->miners[i].n_coins = 0;
        }
    }

    /* decrease the number of miners registered */
    (shm_struct->n_system)--;

    sem_post(&(shm_struct->sem_data));
}

/**
 * @brief Initializes the system shared memory segment.
 *
 * @param shm_struct SHMMINER shared memory structure.
 * @return OK (0) or in case of error ERR (-1).
 */
int shm_init(SHMMINER *shm_struct)
{
    int i;

    /* initialize miners info */
    for (i = 0; i < MAX_MINERS; i++)
    {
        shm_struct->miners[i].pid = -1;
        shm_struct->miners[i].vote = NO_VOTE;
        shm_struct->miners[i].n_coins = 0;
    }

    /* initialize last block info */
    shm_struct->last_block.id = -1;
    shm_struct->last_block.result = INIT_OBJECTIVE;
    shm_struct->last_block.accepted_votes = 0;
    shm_struct->last_block.total_votes = 0;

    /* initialize actual block info */
    shm_struct->actual_block.id = 0;
    shm_struct->actual_block.target = INIT_OBJECTIVE;
    for (i = 0; i < MAX_MINERS; i++)
    {
        shm_struct->actual_block.miners[i] = -1;
        shm_struct->actual_block.wallets[i] = 0;
    }

    /* initialize system info */
    shm_struct->n_system = 0;

    /* initialize semaphores */
    if (sem_init(&(shm_struct->sem_winner), 1, 1) == -1)
    {
        perror("sem_init");
        return ERR;
    }

    if (sem_init(&(shm_struct->sem_data), 1, 1) == -1)
    {
        perror("sem_init");
        sem_destroy(&(shm_struct->sem_winner));
        return ERR;
    }

    return OK;
}

/**
 * @brief Frees the resources allocated at the shared memory segment.
 *
 * @param shm_struct SHMMINER shared memory structure.
 */
void shm_destroy(SHMMINER *shm_struct)
{
    sem_destroy(&(shm_struct->sem_winner));
    sem_destroy(&(shm_struct->sem_data));
}

/**
 * @brief Code executed by the registrador process. It reads the results from the pipe and writes them to a file.
 *
 * @param fd_read File descriptor of the pipe to read from.
 */
void pregistrador(int fd_read)
{
    int fd_write;
    char filename[FILENAME_MAX];
    ssize_t nbytes = 0;
    POWRESULT info;
    int i;

    /* open the file */
    sprintf(filename, "miner_%d.log", getppid());
    fd_write = open(filename, O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR);
    if (fd_write == -1)
    {
        perror("open");
        close(fd_read);
        exit(EXIT_FAILURE);
    }

    do
    {
        /* read a block from the pipe */
        nbytes = read(fd_read, &info, sizeof(POWRESULT));
        if (nbytes == -1)
        {
            perror("read");
            close(fd_read);
            exit(EXIT_FAILURE);
        }

        if (nbytes > 0)
        {
            /* print the block in the file */
            dprintf(fd_write, "Id:       %04d\n"
                              "Winner:   %d\n"
                              "Target:   %08ld\n"
                              "Solution: %08ld ",
                    info.id, info.winner, info.target, info.result);
            if (info.accepted_votes > info.total_votes - info.accepted_votes)
            {
                dprintf(fd_write, "(validated)\n");
            }
            else
            {
                dprintf(fd_write, "(rejected)\n");
            }
            dprintf(fd_write, "Votes:    %d/%d\n", info.accepted_votes, info.total_votes);
            dprintf(fd_write, "Wallets:  ");
            for (i = 0; i < MAX_MINERS; i++)
            {
                if (info.miners[i] != -1)
                {
                    dprintf(fd_write, "%d:%02d ", info.miners[i], info.wallets[i]);
                }
            }
            dprintf(fd_write, "\n\n");
        }

        /* if 'Minero' closes the pipe, 'Registrador' exits */
    } while (nbytes != 0);

    /* shutdown the pipe */
    close(fd_read);

    exit(EXIT_SUCCESS);
}

/**
 * @brief Code executed by the minero process.
 *
 * @param SHMMINER SHMMINER shared memory structure.
 * @param set Set of signals to block.
 * @param oset Set of default signals.
 * @param fd_pipe File descriptor of the pipe to write to.
 * @param nthreads Number of threads the miner will use to calculate the POW.
 */
void pminero(SHMMINER *shm_struct, sigset_t set, sigset_t oset, int fd_pipe, int nthreads)
{
    pid_t pid = getpid();
    int i, nshortwaits, round = -1;

    sigset_t block_sigusr2, noblock_sigusr2;
    mqd_t mq;

    struct timespec ts;
    ts.tv_sec = 0;

    /* initialize sets */
    block_sigusr2 = oset;
    sigaddset(&block_sigusr2, SIGUSR2);

    noblock_sigusr2 = set;
    sigdelset(&noblock_sigusr2, SIGUSR2);

    while (1)
    {
        /* wait for next round */
        sigsuspend(&block_sigusr2);

        /* send the block to the register process */
        if (shm_struct->last_block.id >= 0 && round >= 0)
        {
            if (write(fd_pipe, &(shm_struct->last_block), sizeof(POWRESULT)) != sizeof(POWRESULT))
            {
                perror("write");
                miner_exit(shm_struct, fd_pipe, EXIT_FAILURE);
            }
        }

        round++;

        if (sigalrm || sigint)
        {
            if (sigalrm)
            {
                sigalrm = 0;
            }
            else if (sigint)
            {
                printf("Finishing by signal...\n");
                sigint = 0;
            }
            miner_exit(shm_struct, fd_pipe, EXIT_SUCCESS);
        }
        else if (sigusr1)
        {
            sigusr1 = 0;

            /* start the search (we are only supposed to receive SIGUSR2) */
            sigprocmask(SIG_SETMASK, &noblock_sigusr2, NULL);
            if (multithread_search_pow(shm_struct->actual_block.target, nthreads) == ERR)
            {
                fprintf(stderr, "ERROR: multithread_search_pow\n");
                miner_exit(shm_struct, fd_pipe, EXIT_FAILURE);
            }
            sigprocmask(SIG_BLOCK, &set, NULL);

            /* try to become the winner after getting the result */
            if (sem_trywait(&(shm_struct->sem_winner)) == -1)
            {
                if (errno != EAGAIN)
                {
                    perror("sem_trywait");
                    miner_exit(shm_struct, fd_pipe, EXIT_FAILURE);
                }
                else /* PERDEDOR PROCESS */
                {
                    if (!sigusr2)
                    {
                        sigsuspend(&noblock_sigusr2);
                    }

                    sigusr2 = 0;

                    /* start voting */
                    sem_wait(&(shm_struct->sem_data));
                    for (i = 0; i < MAX_MINERS; i++)
                    {
                        if (shm_struct->miners[i].pid == pid)
                        {
                            if (pow_hash(shm_struct->actual_block.result) == shm_struct->actual_block.target)
                            {
                                shm_struct->miners[i].vote = VOTE_YES;
                            }
                            else
                            {
                                shm_struct->miners[i].vote = VOTE_NO;
                            }
                            break;
                        }
                    }
                    sem_post(&(shm_struct->sem_data));
                }
            }
            else /* GANADOR PROCESS */
            {
                /* prepare the voting */
                sem_wait(&(shm_struct->sem_data));

                shm_struct->actual_block.winner = pid;
                shm_struct->actual_block.result = result;
                for (i = 0; i < MAX_MINERS; i++)
                {
                    if (shm_struct->miners[i].pid == pid)
                    {
                        shm_struct->miners[i].vote = VOTE_YES;
                    }
                    else
                    {
                        shm_struct->miners[i].vote = NO_VOTE;
                    }
                }

                /* send SIGUSR2 to all the voters */
                for (i = 0; i < MAX_MINERS; i++)
                {
                    if (shm_struct->miners[i].pid != pid && shm_struct->miners[i].pid != -1)
                    {
                        if (kill(shm_struct->miners[i].pid, SIGUSR2) == -1)
                        {
                            perror("kill");
                            sem_post(&(shm_struct->sem_data));
                            miner_exit(shm_struct, fd_pipe, EXIT_FAILURE);
                        }
                    }
                }
                sem_post(&(shm_struct->sem_data));

                /* wait for the votes */
                nshortwaits = 0;
                ts.tv_nsec = 5000000; /* 5ms */

                while (1)
                {
                    /* sleep for 5ms */
                    if (nanosleep(&ts, NULL) == -1)
                    {
                        perror("nanosleep");
                        miner_exit(shm_struct, fd_pipe, EXIT_FAILURE);
                    }

                    nshortwaits++;

                    /* check if all the votes are in */
                    sem_wait(&(shm_struct->sem_data));
                    for (i = 0; i < MAX_MINERS; i++)
                    {
                        if (shm_struct->miners[i].pid != -1 && shm_struct->miners[i].vote == NO_VOTE)
                        {
                            break;
                        }
                    }
                    sem_post(&(shm_struct->sem_data));

                    /* if all the votes are in, break */
                    if (i == MAX_MINERS)
                    {
                        break;
                    }
                }

                /* count the votes */
                sem_wait(&(shm_struct->sem_data));
                for (i = 0; i < MAX_MINERS; i++)
                {
                    if (shm_struct->miners[i].pid != -1)
                    {
                        shm_struct->actual_block.total_votes++;
                        if (shm_struct->miners[i].vote == VOTE_YES)
                        {
                            shm_struct->actual_block.accepted_votes++;
                        }
                    }
                    shm_struct->actual_block.miners[i] = shm_struct->miners[i].pid;
                }

                /* update the wallets */
                if (shm_struct->actual_block.accepted_votes > shm_struct->actual_block.total_votes - shm_struct->actual_block.accepted_votes)
                {
                    for (i = 0; i < MAX_MINERS; i++)
                    {
                        if (shm_struct->miners[i].pid == pid)
                        {
                            shm_struct->miners[i].n_coins++;
                            shm_struct->actual_block.wallets[i] = shm_struct->miners[i].n_coins;
                        }
                    }
                }
                sem_post(&(shm_struct->sem_data));

                /* if the monitor is open (mq exists), open the msg queue and send the block to the monitor */
                if ((mq = mq_open(MQ_NAME, O_RDWR)) == (mqd_t)-1)
                {
                    if (errno != ENOENT)
                    {
                        perror("mq_open");
                        miner_exit(shm_struct, fd_pipe, EXIT_FAILURE);
                    }
                }
                else
                {
                    if (mq_send(mq, (char *)&(shm_struct->actual_block), sizeof(POWRESULT), 0) == -1)
                    {
                        perror("mq_send");
                        mq_close(mq);
                        miner_exit(shm_struct, fd_pipe, EXIT_FAILURE);
                    }

                    mq_close(mq);
                }

                /* prepare the next round */
                shm_struct->last_block = shm_struct->actual_block;
                shm_struct->actual_block.id++;
                shm_struct->actual_block.target = shm_struct->last_block.result;
                shm_struct->actual_block.total_votes = 0;
                shm_struct->actual_block.accepted_votes = 0;

                /* sleep for 200ms */
                ts.tv_nsec = 200000000;
                if (nanosleep(&ts, NULL) == -1)
                {
                    perror("nanosleep");
                    miner_exit(shm_struct, fd_pipe, EXIT_FAILURE);
                }

                sem_post(&(shm_struct->sem_winner));

                /* send SIGUSR1 to all the miners */
                sem_wait(&(shm_struct->sem_data));
                for (i = 0; i < MAX_MINERS; i++)
                {
                    if (shm_struct->miners[i].pid != -1)
                    {
                        if (kill(shm_struct->miners[i].pid, SIGUSR1) == -1)
                        {
                            perror("kill");
                            miner_exit(shm_struct, fd_pipe, EXIT_FAILURE);
                        }
                    }
                }
                sem_post(&(shm_struct->sem_data));
            }
        }
        else
        {
            fprintf(stderr, "ERROR: Unexpected signal received\n");
            miner_exit(shm_struct, fd_pipe, EXIT_FAILURE);
        }
    }

    miner_exit(shm_struct, fd_pipe, EXIT_SUCCESS);
}

/**
 * @brief Exits the miner.
 *
 * @param shm_struct Pointer to the shared memory structure
 * @param fd_pipe File descriptor of the pipe
 * @param st Exit status
 */
void miner_exit(SHMMINER *shm_struct, int fd_pipe, int st)
{
    mqd_t mq;
    POWRESULT msg;

    msg.target = -1;
    msg.result = -1;

    /* close the pipe */
    if (fd_pipe != -1)
    {
        if (close(fd_pipe) == -1)
        {
            perror("close");
            st = ERR;
        }
    }

    /* wait for Registrador to finish */
    wait(NULL);

    if (shm_struct != NULL)
    {
        /* unregister its pid */
        pid_unregister(shm_struct);

        /* if it is the last miner, destroy the shared memory */
        sem_wait(&(shm_struct->sem_data));
        if (shm_struct->n_system == 0)
        {
            shm_unlink(SHM_NAME);
            shm_destroy(shm_struct);

            /* if the monitor is open (mq exists), open the msg queue and send the terminating block to the monitor */
            if ((mq = mq_open(MQ_NAME, O_RDWR)) == (mqd_t)-1)
            {
                if (errno != ENOENT)
                {
                    perror("mq_open");
                    st = ERR;
                }
            }
            else
            {
                if (mq_send(mq, (char *)&msg, sizeof(POWRESULT), 0) == -1)
                {
                    perror("mq_send");
                    mq_close(mq);
                    st = ERR;
                }

                mq_close(mq);
            }
        }
        else
        {
            sem_post(&(shm_struct->sem_data));
        }

        /* unmap the shared memory */
        if (munmap(shm_struct, sizeof(SHMMINER)) == -1)
        {
            perror("munmap");
            st = ERR;
        }
    }

    exit(st);
}

int main(int argc, char *argv[])
{
    int n_seconds, n_threads;
    pid_t pid;
    int fd_shm;
    int i;
    int st = OK;
    struct stat statbuf;
    SHMMINER *shm_struct = NULL;

    struct timespec ts;

    /* signal handlers */
    struct sigaction sigusr1_handler;
    struct sigaction sigusr2_handler;
    struct sigaction sigalrm_handler;
    struct sigaction sigint_handler;

    /* signal block */
    sigset_t set, oset;

    /*
     * fd_pipe is the pipe where 'Minero' process will write fd_pipe[1]
     * and where 'Registrador' process will read fd_pipe1[0].
     * fd_pipe[0] will be closed in 'Minero' process and fd_pipe[1] will
     * be closed in 'Registrador' process.
     */
    int fd_pipe[2];

    ts.tv_sec = 0;
    ts.tv_nsec = 300000000; /* 3ms */

    sigemptyset(&set);
    sigemptyset(&oset);

    sigaddset(&set, SIGUSR1);
    sigaddset(&set, SIGUSR2);
    sigaddset(&set, SIGALRM);
    sigaddset(&set, SIGINT);

    /* block signals */
    if (sigprocmask(SIG_BLOCK, &set, &oset) < 0)
    {
        perror("sigprocmask");
        exit(EXIT_FAILURE);
    }

    /* set handlers */
    if (set_handler(&sigusr1_handler, SIGUSR1, handler_SIGUSR1) == ERR)
    {
        fprintf(stderr, "set_handler: error setting handler for SIGUSR1");
        exit(EXIT_FAILURE);
    }

    if (set_handler(&sigusr2_handler, SIGUSR2, handler_SIGUSR2) == ERR)
    {
        fprintf(stderr, "set_handler: error setting handler for SIGUSR2");
        exit(EXIT_FAILURE);
    }

    if (set_handler(&sigalrm_handler, SIGALRM, handler_SIGALRM) == ERR)
    {
        fprintf(stderr, "set_handler: error setting handler for SIGALRM");
        exit(EXIT_FAILURE);
    }

    if (set_handler(&sigint_handler, SIGINT, handler_SIGINT) == ERR)
    {
        fprintf(stderr, "set_handler: error setting handler for SIGALRM");
        exit(EXIT_FAILURE);
    }

    /* arg control */
    if (argc != 3)
    {
        printf("ERROR: invalid arguments!\n"
               "Use: ./miner <N_SECONDS> <N_THREADS>\n");
        exit(EXIT_FAILURE);
    }
    else
    {
        n_seconds = atoi(argv[1]);
        n_threads = atoi(argv[2]);
        if (n_seconds < 0 || n_threads < 1)
        {
            printf("ERROR: invalid arguments!\n"
                   "Use: ./miner <N_SECONDS> <N_THREADS>\n");
            exit(EXIT_FAILURE);
        }
    }

    /* open pipe */
    if (pipe(fd_pipe) == -1)
    {
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    /* Minero create Registrador process */
    pid = fork();
    if (pid == -1)
    {
        perror("fork");
        exit(EXIT_FAILURE);
    }
    else if (pid == 0) /* REGISTRADOR PROCESS */
    {
        /* close write end of the pipe */
        close(fd_pipe[1]);
        pregistrador(fd_pipe[0]);
    }
    else
    {
        /* close read end of the pipe */
        close(fd_pipe[0]);

        /* create the shared memory segment */
        fd_shm = shm_open(SHM_NAME, O_RDWR | O_CREAT | O_EXCL, S_IRUSR | S_IWUSR);

        /* if the shared memory segment already exists this process is not the first minero, otherwise it is */
        if (fd_shm == -1)
        {
            if (errno == EEXIST) /* NOT FIRST MINER PROCESS */
            {
                /* open shared memory */
                fd_shm = shm_open(SHM_NAME, O_RDWR, 0);
                if (fd_shm == -1)
                {
                    perror("shm_open");
                    miner_exit(NULL, fd_pipe[1], EXIT_FAILURE);
                }

                /* check if the memory segment has already been resized */
                do
                {
                    /* wait for 3ms */
                    if (nanosleep(&ts, NULL) == -1)
                    {
                        perror("nanosleep");
                        close(fd_shm);
                        miner_exit(NULL, fd_pipe[1], EXIT_FAILURE);
                    }

                    /* get shared memory information again */
                    if (fstat(fd_shm, &statbuf) == -1)
                    {
                        perror("fstat");
                        close(fd_shm);
                        miner_exit(NULL, fd_pipe[1], EXIT_FAILURE);
                    }

                } while (statbuf.st_size != sizeof(SHMMINER));

                /* mapping of the memory segment */
                shm_struct = mmap(NULL, sizeof(SHMMINER), PROT_READ | PROT_WRITE, MAP_SHARED, fd_shm, 0);
                close(fd_shm);
                if (shm_struct == MAP_FAILED)
                {
                    perror("mmap");
                    shm_unlink(SHM_NAME);
                    miner_exit(NULL, fd_pipe[1], EXIT_FAILURE);
                }

                /* check if the last semaphore is initialized */
                while (sem_getvalue(&(shm_struct->sem_data), &st) == -1)
                {
                    /* wait for 3ms */
                    if (nanosleep(&ts, NULL) == -1)
                    {
                        perror("nanosleep");
                        miner_exit(shm_struct, fd_pipe[1], EXIT_FAILURE);
                    }
                }

                /* system register */
                if (pid_register(shm_struct) == ERR)
                {
                    miner_exit(shm_struct, fd_pipe[1], EXIT_SUCCESS);
                }

                /* set alarm */
                alarm(n_seconds);

                /* start mining */
                pminero(shm_struct, set, oset, fd_pipe[1], n_threads);
            }
            else
            {
                perror("shm_open");
                miner_exit(NULL, fd_pipe[1], EXIT_FAILURE);
            }
        }
        else /* FIRST MINER PROCESS */
        {
            /* resize the memory segment */
            if (ftruncate(fd_shm, sizeof(SHMMINER)) == -1)
            {
                perror("ftruncate");
                shm_unlink(SHM_NAME);
                miner_exit(NULL, fd_pipe[1], EXIT_FAILURE);
            }

            /* mapping of the memory segment */
            shm_struct = mmap(NULL, sizeof(SHMMINER), PROT_READ | PROT_WRITE, MAP_SHARED, fd_shm, 0);
            close(fd_shm);
            if (shm_struct == MAP_FAILED)
            {
                perror("mmap");
                shm_unlink(SHM_NAME);
                miner_exit(NULL, fd_pipe[1], EXIT_FAILURE);
            }

            /* inititialize the system shared memory */
            if (shm_init(shm_struct) == ERR)
            {
                fprintf(stderr, "ERROR: shm_init\n");
                munmap(shm_struct, sizeof(SHMMINER));
                shm_unlink(SHM_NAME);
                miner_exit(NULL, fd_pipe[1], EXIT_FAILURE);
            }

            /* pid register */
            if (pid_register(shm_struct) == ERR)
            {
                miner_exit(shm_struct, fd_pipe[1], EXIT_SUCCESS);
            }

            alarm(n_seconds);

            /* send SIGUSR1 signal to the other miner processes */
            sem_wait(&(shm_struct->sem_data));
            for (i = 0; i < MAX_MINERS; i++)
            {
                if (shm_struct->miners[i].pid != -1)
                {
                    if (kill(shm_struct->miners[i].pid, SIGUSR1) == -1)
                    {
                        perror("kill");
                        sem_post(&(shm_struct->sem_data));
                        miner_exit(shm_struct, fd_pipe[1], EXIT_FAILURE);
                    }
                }
            }
            sem_post(&(shm_struct->sem_data));

            /* start mining */
            pminero(shm_struct, set, oset, fd_pipe[1], n_threads);
        }
    }

    exit(EXIT_SUCCESS);
}
