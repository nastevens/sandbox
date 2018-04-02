#include <stdio.h>
#include "util.h"
#include "err.h"

int main(int argc,char *argv[]) {
  int error = -1;
  int i;
  int flc;
  int index;
  int free_FLC;
  struct fileinfo info;
  int new_flc;
  int new_index; 
  int status;
  int num;
  char *last;
  char buffer[260];
  char buffer1[260];
  char file_name[10];
  char name[10];
  char ext[4];
  char* etmp;

  /*Checks number of arguments*/
  if(argc != 2) {
    printf("Please specify one directory.\n");
    return error;
  }
  /*Right number of arguments*/
  else {
    init_util();
    status = parse_path(argv[1],&flc,&index);
    
    /*Checks if directory exists*/
    if(status != E_NOTEXIST) {
      printf("Directory already exists.\n");
      return error;
    }
    /*Directory does not exist, make a new one!*/
    else {
      last = rindex(argv[1],'/');

      /*Check if path is relative*/
      if(last == 0) {
	get_abs_path(buffer1,argv[1]);
	last = rindex(buffer1,'/');
	num = (int)(last-buffer1+1);
	strncpy(buffer,buffer1,num);
	buffer[num] = '\0';
	//printf("Buffer is:%s\n",buffer);
	strcpy(name,argv[1]);
	//printf("I am here and name is:%s\n",name);
      }
      /*Path may still be relative, but there is at least one '/'*/
      else {
	/*Check if there is an ending '/'*/
	if(strlen(last) == 1) {         //Checks if the last character is "/"
	  get_abs_path(buffer, argv[1]);
	  //printf("Buffer is:%s\n",buffer);
	  strncpy(buffer1,buffer,(strlen(buffer)-1));
	  //printf("Buffer1 is:%s\n",buffer1);
	  buffer1[strlen(buffer)-1]='\0';
	  last = rindex(buffer1,'/');
	  if(last == 0) {
	    buffer[0] = '\0';
	    num = 1;
	  }
	  else {
	    num = (int)(last-buffer1+1);
	    strncpy(buffer,buffer1,num);
	    buffer[num] = '\0';
	    //printf("Buffer is:%s\n",buffer);
	    last = rindex(buffer1,'/');
	    if(last == 0) {
	      buffer[0] = '\0';
	    }
	  }
	}
	/*No ending '/', continue*/
	else {
	  //printf("Last is:%d\n",strlen(last));
	  num = (int)(last-argv[1]+1);
	  strncpy(buffer,argv[1],num);
	  strcpy(buffer1,argv[1]);
	  //printf("Buffer is:%s\n",buffer);
	  buffer[num] = '\0';
	}
	/*Check if the path is really relative*/
	if(argv[1][0] != '/' && last != 0) {
	  last = rindex(buffer1,'/');
	  num = (int)(last-buffer1+1);
	  //printf("%d\n",num);
          strcpy(name,&buffer1[num]);
        } 
	else if(argv[1][0] != '/' && last == 0) {
	  strcpy(name,buffer1);
	}
	/*Path is not relative, continue*/
	else {
	  strcpy(file_name,&buffer1[num]);  //Keeps track of the new directory name
	  //printf("%d\n",strlen(buffer1)-1);
	  file_name[strlen(buffer1)-1]='\0';
	  //printf("File name is:%s\n",file_name);
	  if(file_name[0] == '/') {       //Checks if the first character is the "/"
	    for(i=0;i<(strlen(buffer1)-1);i++) {
	      name[i] = file_name[i+1];
	    }
	    name[strlen(buffer1)-1]= '\0';
	  }
          else {
	    strcpy(name,file_name);
	  }
	}
      }
      
      //printf("num: %d buffer: %s\n", num, buffer);
      status = parse_path(buffer,&flc,&index);
      free_FLC = get_free_block();
      info = get_file_info(flc,index);
      info.attrib = '\x10';
      etmp = (char*)strtok(name, ".");
      strcpy(info.filename,etmp);
      etmp = (char*)strtok(NULL,".");
      strcpy(info.ext, ((etmp == NULL) ? "   " : etmp));
      allocate_block(free_FLC,info,info.FLC,&new_flc,&new_index);
      strcpy(info.filename,"..");
      strcpy(info.ext,"   ");
      allocate_block(0,info,free_FLC,&new_flc,&new_index);
      strcpy(info.filename,".");
      strcpy(info.ext,"   ");
      info.FLC = free_FLC;
      allocate_block(0,info,free_FLC,&new_flc,&new_index);
      return 1;
    }
  }
  kill_util();
}




























