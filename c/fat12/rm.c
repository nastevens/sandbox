// Written by Lissa Avery, 1/22/2005.
// It performs the necessary instructions to completely execute the "rm" command.

#include <stdio.h>
#include <string.h>
#include "util.h"
#include "err.h"

#define SUCCESS 0
#define FAILURE 1

void printUsage();

int main (int argc, char* argv[])
{
  char *path;
  int FLC;
  int index;
  int parsePathReturn;
  struct fileinfo fileToRemove;

  init_util();

  if (argc != 2)
    {
      printf("rm: incorrect number of arguments.\n");
      printUsage();
      //fclose(stream);
      kill_util();
      exit(FAILURE);
    }

  // The file the user wants to remove is the first argument
  path = argv[1];
  parsePathReturn = parse_path(path, &FLC, &index);
  if (parsePathReturn == E_NOTEXIST)
      {
	  printf("Unable to find the specified file or directory.\n");
	  printUsage();
	  //fclose(stream);
	  kill_util();
	  exit(E_NOTEXIST);
      }
  fileToRemove = get_file_info(FLC, index);

  #ifdef DEBUG_CODE
  printf("File information has been obtained.\n");
  printf("FLC is %i, path is %s, index is %i.\n", FLC, path, index); 
  #endif

  // We can only attempt to remove files, so let's get that squared away now. 
  if (get_file_type(fileToRemove) != T_FILE)
      {
	  printf("Cannot remove non-file.\n");
	  printUsage();
	  //fclose(stream);
	  kill_util();
	  exit(FAILURE);
	  // Note: this tests fine as of 20:10 on 1/22/2005
      }

  if (unlink_entry(FLC, index) == E_CANTUNLINK)
      {
	  printf("Cannot remove file.\n");
	  //fclose(stream);
	  kill_util();
	  exit(E_CANTUNLINK);
      }

  // If we've gotten this far, then we've unlinked the file and we're ready to close up shop.

  //fclose(stream);
  kill_util();
  exit(SUCCESS);
}

void printUsage()
{
  printf("Usage: rm file\n");
}
