#ifndef LINUX_BLD
#include <windows.h>
#define sleep(x) Sleep((x)*1000)
#else
#include <unistd.h>
#endif
#include "fpsetlib.h"
#include <stdlib.h>
#include <stdio.h>
#include <fenv.h>
#include <pthread.h>

void* thread_task(void* v)
{
    printf("|Thread  |get|%#4x\n", get_fpu());

    printf("|Thread  |set|0x117f\n");
    set_fpu(0x117f);

    printf("|Thread  |get|%#4x\n", get_fpu());

    sleep(5);

    printf("|Thread  |get|%#4x\n", get_fpu());

    pthread_exit(NULL);
}

int main()
{
    int result;
    pthread_t thread;
    pthread_attr_t attr;
    void* status;

    // Make sure that threads are joinable
    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);

    printf("|Main    |get|%#4x\n", get_fpu());

    printf("|Main    |set|0x147f\n");
    set_fpu(0x147f);

    printf("|Main    |get|%#4x\n", get_fpu());

    result = pthread_create(&thread, &attr, thread_task, NULL);
    if(result)
    {
        printf("ERROR; return code from pthread_create is %d\n", result);
        exit(-1);
    }

    sleep(2);

    printf("|Main    |set|0x137f\n");
    set_fpu(0x137f);

    printf("|Main    |get|%#4x\n", get_fpu());

    //printf(">Waiting for thread to return...\n");
    pthread_attr_destroy(&attr);
    result = pthread_join(thread, &status);
    if(result)
    {
        printf("Error from pthread_join is %d\n", result);
        exit(-1);
    }
    //printf(">Joined with thread\n");
    printf("|Main    |get|%#4x\n", get_fpu());

    return EXIT_SUCCESS;
}
