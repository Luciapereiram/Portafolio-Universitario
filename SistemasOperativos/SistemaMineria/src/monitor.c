/**
 * @file monitor.c
 * @brief SOPER Proyecto Final
 *
 * @author Alejandro Ibáñez Pastrana
 * @author Lucía Pereira Menchero
 * @date 05/05/2023
 */
#define _POSIX_C_SOURCE 199309L

#include "monitor.h"

/* GLOBAL VARIABLES */

static volatile int sigint = 0; /*!< SIGINT signal flag */

/* HANDLER FUNCTIONS */

void handler_SIGINT() 
{ 
    printf("\n");
    sigint = 1; 
}

/**
 * @brief Initializes the shared memory
 * 
 * @param shm_struct Pointer to the shared memory structure
 * @return OK (1) if the shared memory is initialized correctly, ERR (0) otherwise
 */
int buffer_init(SHMMONITOR *shm_struct)
{
    shm_struct->head = 0;
    shm_struct->tail = 0;

    if (sem_init(&(shm_struct->sem_mutex), 1, 1) == -1)
    {
        perror("sem_init");
        return ERR;
    }
    if (sem_init(&(shm_struct->sem_empty), 1, BUFFER_DIM) == -1)
    {
        perror("sem_init");
        sem_destroy(&(shm_struct->sem_mutex));
        return ERR;
    }
    if (sem_init(&(shm_struct->sem_fill), 1, 0) == -1)
    {
        perror("sem_init");
        sem_destroy(&(shm_struct->sem_mutex));
        sem_destroy(&(shm_struct->sem_empty));
        return ERR;
    }

    return OK;
}

/**
 * @brief Destroys the semaphores of the shared memory
 * 
 * @param shm_struct Pointer to the shared memory structure
 */
void buffer_destroy(SHMMONITOR *shm_struct)
{
    sem_destroy(&(shm_struct->sem_mutex));
    sem_destroy(&(shm_struct->sem_empty));
    sem_destroy(&(shm_struct->sem_fill));
}

/**
 * @brief Pushes a message in the shared memory
 * 
 * @param shm_struct Pointer to the shared memory structure
 * @param msg Message to push
 */
void buffer_push(SHMMONITOR *shm_struct, POWRESULT msg)
{
    /* push the message in the buffer */
    sem_wait(&(shm_struct->sem_empty));
    sem_wait(&(shm_struct->sem_mutex));
    shm_struct->queue[shm_struct->head] = msg;
    shm_struct->head = (shm_struct->head + 1) % BUFFER_DIM;
    sem_post(&(shm_struct->sem_mutex));
    sem_post(&(shm_struct->sem_fill));
}

/**
 * @brief Pops a message from the shared memory
 * 
 * @param shm_struct Pointer to the shared memory structure
 * @return Message popped
 */
POWRESULT buffer_pop(SHMMONITOR *shm_struct)
{
    POWRESULT msg;

    /* pop the message from the buffer */
    sem_wait(&(shm_struct->sem_fill));
    sem_wait(&(shm_struct->sem_mutex));
    msg = shm_struct->queue[shm_struct->tail];
    shm_struct->tail = (shm_struct->tail + 1) % BUFFER_DIM;
    sem_post(&(shm_struct->sem_mutex));
    sem_post(&(shm_struct->sem_empty));

    return msg;
}

/**
 * @brief Code executed by the Comprobador process.
 * 
 * @param shm_struct Pointer to the shared memory structure
*/
void pcomprobador(SHMMONITOR *shm_struct)
{
    POWRESULT msg;
    mqd_t mq;
    struct mq_attr attr;

    int exit_status;
    int st = OK;

    sigset_t pending_signals;
    sigset_t sigintmask;

    sigemptyset(&pending_signals);
    sigemptyset(&sigintmask);
    sigaddset(&sigintmask, SIGINT);

    /* create the message queue */
    attr.mq_flags = 0;
    attr.mq_maxmsg = MQ_MAX_MSJ;
    attr.mq_msgsize = MQ_MSJ_SIZE;
    attr.mq_curmsgs = 0;

    mq = mq_open(MQ_NAME, O_CREAT | O_EXCL | O_RDONLY, S_IRUSR | S_IWUSR, &attr);
    if (mq == -1)
    {
        perror("mq_open");
        buffer_destroy(shm_struct);
        munmap(shm_struct, sizeof(SHMMONITOR));
        exit(EXIT_FAILURE);
    }

    sigprocmask(SIG_UNBLOCK, &sigintmask, NULL);

    /* start checking the results */
    while (sigint == 0)
    {
        /* receive the message */
        if (mq_receive(mq, (char *)&msg, MQ_MSJ_SIZE, NULL) == -1)
        {
            if (sigint != 1)
            {
                perror("mq_receive");
                st = ERR;
            }
            break;
        }

        if (msg.target == -1 && msg.result == -1)
            break;

        /* check if the result */
        msg.flag = pow_hash(msg.result) == msg.target;

        /* insert the result in the shared memory with the producer-consumer pattern */
        if (sigint == 0)
            buffer_push(shm_struct, msg);
    }

    /* send the completation message */
    msg.result = -1;
    msg.target = -1;
    buffer_push(shm_struct, msg);

    /* wait for the monitor to finish */
    wait(&exit_status);

    if (exit_status != EXIT_SUCCESS)
        printf("Monitor finished with errors.\n");

    /* free resources */
    mq_unlink(MQ_NAME);
    mq_close(mq);
    buffer_destroy(shm_struct);
    if (munmap(shm_struct, sizeof(SHMMONITOR)) == -1)
    {
        perror("munmap");
        st = ERR;
    }

    if (st != OK)
        exit(EXIT_FAILURE);

    exit(EXIT_SUCCESS);
}

/**
 * @brief Code executed by the Monitor process.
 * 
 * @param shm_struct Pointer to the shared memory structure
*/
void pmonitor(SHMMONITOR *shm_struct)
{
    POWRESULT msg;

    short st = OK;

    int i;

    while (st == OK)
    {
        /* extract the result from the shared memory with the producer-consumer pattern */
        msg = buffer_pop(shm_struct);

        if (msg.target == -1 && msg.result == -1)
            break;

        /* print the result */
        printf("Id:         %04d\n", msg.id);
        printf("Winner:     %d\n", msg.winner);
        printf("Target:     %08ld\n", msg.target);

        if (msg.flag)
            printf("Solution:   %08ld (validated)\n", msg.result);
        else
            printf("Solution:   %08ld (invalidated)\n", msg.result);

        printf("Votes:      %d/%d\n", msg.accepted_votes, msg.total_votes);
        printf("Wallets:    ");
        for (i = 0; i < MAX_MINERS; i++)
        {
            if (msg.miners[i] != -1)
            {
                printf("%d:%02d ", msg.miners[i], msg.wallets[i]);
            }
        }
        printf("\n\n");
    }

    /* free resources */
    if (munmap(shm_struct, sizeof(SHMMONITOR)) == -1)
    {
        perror("munmap");
        st = ERR;
    }

    if (st != OK)
        exit(EXIT_FAILURE);

    exit(EXIT_SUCCESS);
}

int main()
{
    int fd_shm;
    SHMMONITOR *shm_struct;
    pid_t pid;

    struct sigaction sigint_handler;
    sigset_t set;
    sigset_t oset;

    /* create signal set */
    sigemptyset(&set);
    sigaddset(&set, SIGINT);

    /* block SIGINT */
    sigprocmask(SIG_BLOCK, &set, &oset);

    /* set SIGINT handler */
    if (set_handler(&sigint_handler, SIGINT, handler_SIGINT) == ERR)
    {
        fprintf(stderr, "ERROR: setting SIGINT handler\n");
        exit(EXIT_FAILURE);
    }

    /* create the shared memory segment */
    fd_shm = shm_open(MONITORSHM_NAME, O_RDWR | O_CREAT | O_EXCL, S_IRUSR | S_IWUSR);
    if (fd_shm == -1)
    {
        perror("shm_open");
        exit(EXIT_FAILURE);
    }

    shm_unlink(MONITORSHM_NAME);

    /* resize the memory segment */
    if (ftruncate(fd_shm, sizeof(SHMMONITOR)) == -1)
    {
        perror("ftruncate");
        exit(EXIT_FAILURE);
    }

    /* mapping of the memory segment */
    shm_struct = mmap(NULL, sizeof(SHMMONITOR), PROT_READ | PROT_WRITE, MAP_SHARED, fd_shm, 0);
    close(fd_shm);
    if (shm_struct == MAP_FAILED)
    {
        perror("mmap");
        exit(EXIT_FAILURE);
    }

    /* initialice the memory segment */
    if (buffer_init(shm_struct) == ERR)
    {
        munmap(shm_struct, sizeof(SHMMONITOR));
        exit(EXIT_FAILURE);
    }

    /* create monitor process */
    pid = fork();
    if (pid == -1)
    {
        perror("fork");
        buffer_destroy(shm_struct);
        munmap(shm_struct, sizeof(SHMMONITOR));
        exit(EXIT_FAILURE);
    }
    else if (pid == 0) /* MONITOR PROCESS */
    {
        pmonitor(shm_struct);
    }
    else
    {
        pcomprobador(shm_struct);
    }

    exit(EXIT_SUCCESS);
}