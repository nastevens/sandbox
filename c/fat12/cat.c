#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "util.h"
#include "err.h"


int main(int argc, char **argv) {
  int FLC; 
  int index;
  struct fileinfo info;
  int type;
  char buffer[128]; 
  int max = 128;
  int num_bytes = 128;
  int success_fail;
  int error = -1;

  init_util();
    

  if(argc != 2) {
    printf("Please specify one file.\n");
    return error;   /*indicates an error in # of arguments*/
  } 
  else {
    if ((error = parse_path(argv[1],&FLC,&index)) < 0)
    {
      printf("File does not exist\n");
      return -1;
    }
    info = get_file_info(FLC,index); 
    type = get_file_type(info);
    
    if(type == T_SUBDIR) { 
      printf("Argument needs to be a file.\n");
      return error;
    }
    else if(type == T_FILE) {
      success_fail = open_file(info);
      if(success_fail == E_CANTOPEN) {
	printf("Can't open the file.\n");
	close_file();
	return error;
      } 
      else {
	while(num_bytes >= max) {
	num_bytes = read_file(buffer,max);
	printf("%s",buffer); 
	}
        printf("\n"); // Instead, put one here to make a newline at end of all output
	close_file();
	return 0;
      }
    } 
    else {
      printf("Type is incorrect.\n");
      return error;
    }
  }
  kill_util();
} 
      


