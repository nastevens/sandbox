/* 
 * HelloWorld.c 1.0 03/14/2003 
 *
 */

#include <stdio.h>
#include <string.h>
#include "util.h"

int main(int argc, char* argv[]) {
  
  int FLC, free_FLC, root_FLC;
  int index;
  char path[260];
  int i = 0;
  int length = 0;
  int j = 0;
  int brkpt = 0;
  char dir[260];
  char file[14];
  char name[9];
  char ext[4];

  struct fileinfo parent;
  struct fileinfo info;
  char* etmp;

  init_util();

  if(argc != 2) {
    printf("Improper number of arguments to touch.");
    return -1;
  }
  if(parse_path(argv[1], &FLC, &index) == 1) {
    printf("File already exists.\n");
    return -1;
  }
  if((free_FLC = get_free_block()) < 0) {
    printf("Disk is full.\n");
    return -1;
  }

  strcpy(path, argv[1]);
  length = strlen(path);
  for(j = length-1; j >= 0; j--) {
    if(path[j] == '/') {
      brkpt = j;
      printf("%d\n", j);
      break;
    }
  }
  strncpy(dir, path, brkpt+1);
  dir[brkpt] = '\0';
  if(!strcmp(dir, "")) {
    strcpy(dir, ".");
    brkpt--;
  }
  strcpy(file, &path[brkpt+1]);  
  strcpy(name, strtok(file, "."));
  etmp = strtok(NULL, ".");
  strcpy(ext, ((etmp == NULL) ? "   " : etmp));

  if(parse_path(dir, &root_FLC, &index) != PATH_FOUND) {
    printf("Error: Directory does not exist.\n");
  } 
  
  parent = get_file_info(root_FLC, index);

  strcpy(info.filename, name);
  strcpy(info.ext, ext);
  info.attrib = '\0';
  info.FLC = free_FLC;
  info.fsize = 0;

  allocate_block(free_FLC, info, parent.FLC, &FLC, &index);

  kill_util();

}








