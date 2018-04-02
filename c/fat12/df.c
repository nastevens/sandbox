// Written by Lissa Avery, 1/31/2005
// This command notifies the user of the amount of free space remaining on the disk
// This file accesses the functions in util.c to obtain the count of free space.

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <string.h>
#include "util.h"
#include "err.h"

#define SUCCESS 0
#define FAILURE 1
#define TOTAL_SECTORS 2847

// Method declarations
void printHeader(int blockSize);
void printEntry(long freeBlocks);

int main(int argc, char *argv[])
{
    //int parsePathInfoReturn;
    //  int FLC;
    //  int index;
    //  char path[260];

    long blocks;
    int blockSize;

   #ifdef DEBUG_CODE
    printf("Created variables!\n");
  #endif

  init_util();

  get_free_space(&blocks, &blockSize);

  printf("Number of blocks: %i.  Block size: %d.\n", blocks, blockSize);

  printHeader(blockSize);
  printEntry(blocks);  

  kill_util();
  return SUCCESS;
}

void printHeader(int blockSize)
{
    printf("%dK-blocks\t\tUsed\t\tAvailable\tUse %%\n", blockSize);
}

void printEntry(long freeBlocks)
{
    int used;
    float usedPercent;

    used = TOTAL_SECTORS - freeBlocks;
    usedPercent = used * 100.0 / TOTAL_SECTORS;
    printf("%11i\t\t%i\t%14d\t\t%5.2f\n", TOTAL_SECTORS, used, freeBlocks, usedPercent);
}
