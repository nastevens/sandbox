// Written by Lissa Avery, 1/22/2005
// Performs the operations necessary to remove an empty directory from a FAT12 file system.
// It accesses the utility functions in util.c to get file and directory information

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

// Method declarations
void printUsage();

int main(int argc, char *argv[])
{
    int parsePathInfoReturn;
    int FLC;
    int index;

    struct fileinfo directoryToRemove;
    struct fileinfo *tempDirectoryListing = (struct fileinfo*)malloc(10*sizeof(struct fileinfo));


    init_util();

    // If we don't have exactly one argument (the directory) we need to exit, since someone evidently doesn't
    // know how to correctly delete a directory.
    if (argc != 2)
	{
	    printf("rmdir: incorrect number of arguments.\n");
	    printUsage();
	    //	    fclose(stream);
	    kill_util();
	    exit(FAILURE);
	}

    parsePathInfoReturn = parse_path(argv[1], &FLC, &index);
    if (parsePathInfoReturn == E_NOTEXIST)
	{
	    printf("Unable to find the specified file or directory.\n");
	    printUsage();
	    //fclose(stream);
	    kill_util();
	    exit(E_NOTEXIST);
	}

    directoryToRemove = get_file_info(FLC, index);

    #ifdef DEBUG_CODE
    printf("Directory information has been obtained.\n");
    #endif

    if (get_file_type(directoryToRemove) != T_SUBDIR)
    {
	printf("This command can only remove a directory.\n");
	printUsage();
	//fclose(stream);
	kill_util();
	exit(FAILURE);
    }

    // We can only delete empty directories, so we need to verify that only the "." and ".." entries
    // exist in each directory.
    if (get_dir_list(tempDirectoryListing, 3, FLC, index) != 2)
	{
	    printf("This command can only remove an empty directory.\n");
	    printUsage();
	    //fclose(stream);
	    kill_util();
	    exit(FAILURE);
	}

    // If we've gotten this far, we're good to go on unlinking the directory entry
    if (unlink_entry(FLC, index) == E_CANTUNLINK)
	{
	    printf("Unable to remove directory.\n");
	    //fclose(stream);
	    kill_util();
	    exit(E_CANTUNLINK);
	}
    //    fclose(stream);
    kill_util();
    exit(SUCCESS);
}

void printUsage()
{
    printf("Usage: rmdir directory\n");
}
