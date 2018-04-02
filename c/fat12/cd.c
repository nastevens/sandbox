/* 
 * HelloWorld.c 1.0 03/14/2003 
 *
 */

#include <stdio.h>
#include <string.h>
#include "util.h"
#include "err.h"
#include <assert.h>
int main(int argc, char* argv[]) {
  
  char path[260];
  char abs_path[260];
  int FLC;
  int index;
  int status;
  struct fileinfo filinf;

  init_util();
  
  if(argc > 2) {
    printf("Too many arguments to cd.\n");
    exit(-1);
  }

  if(argc == 1) {
    strcpy(path, "/");
  } else {
    strcpy(path, argv[1]);
  }

   //printf("Path set to %s.\n", path);
 
  status = parse_path(path, &FLC, &index);
   //printf("Status is %d.\n",status);
  if(status < 0) {
    printf("Path not found.\n");
    exit(-1);
  }

  filinf = get_file_info(FLC, index);
  status = get_file_type(filinf);
  get_abs_path(abs_path, path);
  if(status == T_SUBDIR) {
    set_wd(abs_path, FLC);
  } else if(status == T_FILE) {
    printf("Argument to cd is not a directory.\n");
    exit(-1);
  } else {
    printf("File is of an unknown type.\n");
    exit(-1);
  }
  
  kill_util();
  
  return 1;

}


















