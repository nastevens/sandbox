// Written by Lissa Avery, January 22, 2005
// This file contains the core code to execute the listing (ls) command.
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
void printHeader();
int printEntry(struct fileinfo *info);
void printDirectoryListing(struct fileinfo directoryInfo, int FLC, int index);
char * concatFileName(char *fileName, char *extension);

int main(int argc, char *argv[])
{
  int parsePathInfoReturn;
  int FLC;
  int index;
  char path[260];

  //struct shared_info *cwdInfo = NULL;
  //int cwdInfoID;

  struct fileinfo currentFileInfo;

  #ifdef DEBUG_CODE
    printf("Created variables!\n");
  #endif

  init_util();

  switch(argc)
    {
    case 1:
      // If we are given no arguments, we need to display the current working directy's listing
      // The path and FLC of the current working directory are accessible using shared memory

	get_wd(path, &FLC);

      #ifdef DEBUG_CODE
      	printf("Current directory is %s\n", &path);
      #endif

      parsePathInfoReturn = parse_path(path, &FLC, &index);
      currentFileInfo = get_file_info(FLC, index);
      printHeader();
      printDirectoryListing(currentFileInfo, FLC, index);

      break;
    case 2:
      #ifdef DEBUG_CODE
	printf("I have one variable! path: %s\n", argv[1]);
      #endif
      // If we are given a single argument, it should be the path to the directory or file whose info is
      // to be displayed by ls.

      strcpy(path, argv[1]);
      parsePathInfoReturn = parse_path(path, &FLC, &index);

      // If we weren't able to parse the path, then we need to print a usage statement and exit.
      if (parsePathInfoReturn == E_NOTEXIST)
	{
	    printf("Unable to find the given file or directory.\n");
	  printUsage();
	  //shmdt((void *)cwdInfo);
	  //shmctl(cwdInfoID, IPC_RMID, NULL);
  	  kill_util();
	  exit(E_NOTEXIST);
	}

      currentFileInfo = get_file_info(FLC, index);

      #ifdef DEBUG_CODE
          printf("We have a file.  It's name is: %s.  Its FLC is %i.\n", currentFileInfo.filename, currentFileInfo.FLC);
      #endif
      #ifdef DEBUG_CODE
      	  printf("Preparing to check file type.\n");
      #endif

      printHeader();

      if (get_file_type(currentFileInfo) == T_SUBDIR)
	 {
	   #ifdef DEBUG_CODE
	   		printf("We have a directory!  It's name is: %s\n", currentFileInfo.filename);
	   #endif
	   printDirectoryListing(currentFileInfo, FLC, index);
	 }
      else if (get_file_type(currentFileInfo) == T_FILE)
	 {
	   printEntry(&currentFileInfo);
	 }
      break;
    default:
      printf("ls: incorrect number of arguments.\n");
      printUsage();
      //shmdt((void *)cwdInfo);
      //shmctl(cwdInfoID, IPC_RMID, NULL);
      kill_util();
      exit(FAILURE);
    }

  //shmdt((void *)cwdInfo);
  //shmctl(cwdInfoID, IPC_RMID, NULL);
  kill_util();
 return SUCCESS;
}

void printHeader()
{
  printf("Name\t\tType\tFile Size\tFLC\n");
}

void printUsage()
{
  printf("Usage: ls [directory | file]\n");
}

int printEntry(struct fileinfo *info)
{
  char *fileType = " Dir";
  char *filename;
  int c;
  
  //printf("Ext: |%s|\n", info->ext);
filename = concatFileName(strdup(info->filename), strdup(info->ext));

  switch(get_file_type(*info))
    {
    case T_FILE:
      fileType = "File";
      break;
    case T_SUBDIR:
      // We need to make sure the directory name is 11 characters long for display purposes
      for (c = strlen(filename); c < 12; c++)
	  {
	      filename= strcat(filename, " ");
	  }
      fileType = " Dir";
      break;
    default:
      // We are dealing with an unknown file type.
      exit(E_CANTLIST);
    }

    #ifdef DEBUG_CODE
      printf("This entry (%s) is a file.\n", info->filename);
      //printf("File type: %s\n", fileType);
      printf("File size: %i\n", info->fsize);
      printf("File FLC: %i\n", info->FLC);
    #endif

  printf("%s\t%s\t%9i\t%3i\n", filename, fileType, info->fsize, info->FLC);
  return SUCCESS;
}

void printDirectoryListing(struct fileinfo directoryInfo, int FLC, int index)
{
  int numFilesInDirectoryEstimate = 10;
  void *reallocTemp = NULL;
  int numActualFilesInDirectory = 0;
  int forCounter;
  struct fileinfo* fileListing = (struct fileinfo*)malloc(numFilesInDirectoryEstimate * sizeof(struct fileinfo));
  numActualFilesInDirectory = get_dir_list(fileListing, numFilesInDirectoryEstimate, FLC, index);

  #ifdef DEBUG_CODE
  printf("The actual number of entries in this directory is %i\n", numActualFilesInDirectory);
  #endif

  if (numFilesInDirectoryEstimate != numActualFilesInDirectory)
    {
      reallocTemp = realloc(fileListing, numActualFilesInDirectory*sizeof(struct fileinfo));
      if (reallocTemp != NULL)
	{
	  fileListing = reallocTemp;
	  numActualFilesInDirectory = get_dir_list(fileListing, numActualFilesInDirectory, FLC, index);
	  #ifdef DEBUG_CODE
	  	printf("Reallocation has taken place.\n");
	  #endif
	}
    }
  #ifdef DEBUG_CODE
  printf("Successfully realloc'd the fileListing.\n");
  #endif
  for (forCounter = 0; forCounter < numActualFilesInDirectory; forCounter ++)
    {
      // For each file in the directory listing, print its info
      #ifdef DEBUG_CODE
      	printf("Current filename: %s\n", fileListing[forCounter].filename);
      #endif
      printEntry(&fileListing[forCounter]);
    }

  // All should be displayed.  Let's clean up and go home.
  free(fileListing);
}

/*
 */
char * concatFileName(char fileName[], char extension[])
{
  char *final = fileName;
  int currentChar = 0;
  char characterAt;
  char* exten;

  //printf("Passed ext: %s\n", extension);
  //printf("First char of ext: |%c|\n", extension [0]);
  //printf("Length of ext: %i\n", strlen(extension));
  exten = strdup(extension);
  //printf("Copied ext: |%s|\n", exten);
 
  if (final != NULL)
    {
	if (strlen(extension) > 0)
	    {
		strcat(final, ".");
		strcat(final, exten);
		//printf("Concat'd filename: |%s|\n", final);
	    }
    }

  for (currentChar = strlen(final); currentChar < 12; currentChar++)
      {
	  final = strcat(final, " ");
      }


  return final;
}
