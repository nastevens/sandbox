// Shell.c
// The shell running the FAT12 project for team 6.

#include <stdio.h>
#include <unistd.h>
#include <strings.h>
#include  <stdio.h>
#include  <stdlib.h>
#include  <sys/types.h>
#include  <sys/ipc.h>
#include  <sys/shm.h>
#include  <string.h>
#include <errno.h>
#include <fcntl.h>
#include "util.h"
#include <assert.h>

int main(int argc, char* argv[]){
  
  int pid;
  int x;
  int end = 0;
  int i=0;
  int n, N;
  char read[100];
  char* input[10];
  int stream;
  struct shared_info* sinfo;
  int shm_id;
  int empty = 0;

  
  shm_id = shmget(SHM_KEY, sizeof(struct shared_info), IPC_CREAT | 0666);
  sinfo = (struct shared_info*)shmat(shm_id, NULL, 0);
  if (shm_id==(-1) || ((int)sinfo)==(-1))
  {
    printf("Shared memory allocation error\n");
    exit(-1);
  }
  
  if (argc != 2)
  {
    printf("Please pass name of disk image to use\n");
    exit(-1);
  }
  else if((stream = open(argv[1],O_RDWR) < 0))
  {
    printf("Error opening disk image\n");
    exit(-1);
  }
  else printf("Using image %s\n", argv[1]);
  stream = open(argv[1],O_RDWR);
  strcpy(sinfo->path, "/");
  sinfo->FLC = 0;
  sinfo->stream = stream;
  init_util();

  while(!end) {

    i = 0;
    printf("%s> ",sinfo->path);
    fgets(read,100,stdin);
    while(read[i] != '\n') {
      i++;
    }
    read[i] = '\0';
    for(i = 0; i < 100; i++) {
      if(read[i] == ' ') {
	continue;
      }
      if(read[i] == '\0') {
	empty = 1;
      }
      break;
    }
    if(empty) {
      empty = 0;
      continue;
    }
    i = 1;
    input[0] = strtok(read, " ");
    while((input[i] = strtok(NULL," ")) != NULL) {
      i++;
    }
    N = i;
    /*
    for(i = 0; i < N; i++) {
      printf("%s\n",input[i]);
    }
    */
    if(!strcmp(input[0], "exit") || !strcmp(input[0], "logout") || !strcmp(input[0], "end")) {
      end = 1;
    }
 
    else if(!strcmp(input[0],"HelloWorld")) {
      pid = fork();   //Create a child process

      if(pid < 0) {
	fprintf(stderr, "Fork failed\n");
	exit(-1);
      }

      if (pid == 0) {                      //If the current process is the child process
	n = execv("./HelloWorldOutput",input);
	printf("Error: %d \n",n);
	end = 1;
      }

      else if(pid>0) {                     //If the current process is the parent process
	wait(NULL);
      }

    }

    else if(!strcmp(input[0],"ls")) {                    // The _ls_ command.
      pid = fork();

      if(pid < 0) {
	fprintf(stderr, "Fork failed\n");
	exit(-1);
      }

      if(pid == 0) {
	n = execv("./ls",input);
	printf("Error: %d \n",n);
	end = 1;
      }

      else if(pid > 0) {
	wait(NULL);
      }

    }

    else if(!strcmp(input[0],"pwd")) {                   // The _pwd_ command.
      pid = fork(); //Create a child process

      if(pid < 0) {
	fprintf(stderr, "Fork failed\n");
	exit(-1);
      }

      if(pid == 0) {
	n = execv("./pwd",input);
	printf("Error: %d \n",n);
	end = 1;
      }

      else if(pid > 0) {
	wait(NULL);
      }

    }

    else if(!strcmp(input[0],"cat")) {                    // The _cat_ command.
      pid = fork(); //Create a child process

      if(pid < 0) {
	fprintf(stderr, "Fork failed\n");
	exit(-1);
      }

      if(pid == 0) {
	n = execv("./cat",input);
	printf("Error: %d \n",n);
	end = 1;
      }

      else if(pid > 0) {
	wait(NULL);
      }

    }

    else if(!strcmp(input[0],"df")) {                     // The _df_ command.
      pid = fork(); //Create a child process

      if(pid < 0) {
	fprintf(stderr, "Fork failed\n");
	exit(-1);
      }

      if(pid == 0) {
	n = execv("./df",input);
	printf("Error: %d \n",n);
	end = 1;
      }

      else if(pid > 0) {
	wait(NULL);
      }

    }

    else if(!strcmp(input[0],"touch")) {                     // The _touch_ command.
      pid = fork(); //Create a child process

      if(pid < 0) {
	fprintf(stderr, "Fork failed\n");
	exit(-1);
      }

      if(pid == 0) {
	n = execv("./touch",input);
	printf("Error: %d \n",n);
	end = 1;
      }

      else if(pid > 0) {
	wait(NULL);
      }

    }

    else if(!strcmp(input[0],"mkdir")) {                        // The _mkdir_ command.
      pid = fork(); //Create a child process

      if(pid < 0) {
	fprintf(stderr, "Fork failed\n");
	exit(-1);
      }

      if(pid == 0) {
	n = execv("./mkdir",input);
	printf("Error: %d \n",n);
	end = 1;
      }

      else if(pid > 0) {
	wait(NULL);
      }

    }

    else if(!strcmp(input[0],"rm")) {                        // The _rm_ command.
      pid = fork(); //Create a child process

      if(pid < 0) {
	fprintf(stderr, "Fork failed\n");
	exit(-1);
      }

      if(pid == 0) {
	n = execv("./rm",input);
	printf("Error: %d \n",n);
	end = 1;
      }

      else if(pid > 0) {
	wait(NULL);
      }

    }

    else if(!strcmp(input[0],"rmdir")) {                        // The _rmdir_ command.
      pid = fork(); //Create a child process

      if(pid < 0) {
	fprintf(stderr, "Fork failed\n");
	exit(-1);
      }

      if(pid == 0) {
	n = execv("./rmdir",input);
	printf("Error: %d \n",n);
	end = 1;
      }

      else if(pid > 0) {
	wait(NULL);
      }

    }

    else if(!strcmp(input[0],"cd")) {                        // The _cd_ command.
      pid = fork(); //Create a child process

      if(pid < 0) {
        fprintf(stderr, "Fork failed\n");
        exit(-1);
      }

      if(pid == 0) {
        n = execv("./cd",input);
        printf("Error: %d \n",n);
	end = 1;
      }

      else if(pid > 0) {
        wait(NULL);
      }

    }

    else if(!strcmp(input[0],"printBootSector")) {
      pid = fork(); //Create a child process

      if(pid < 0) {
        fprintf(stderr, "Fork failed\n");
        exit(-1);
      }

      if(pid == 0) {
        n = execv("./tnick",input);
        printf("Error: %d \n",n);
	end = 1;
      }

      else if(pid > 0) {
        wait(NULL);
      }

    }


    else if(!strcmp(input[0],"printFatEntries")) {
      pid = fork(); //Create a child process

      if(pid < 0) {
        fprintf(stderr, "Fork failed\n");
        exit(-1);
      }

      if(pid == 0) {
        n = execv("./tnick",input);
        printf("Error: %d \n",n);
	end = 1;
      }

      else if(pid > 0) {
        wait(NULL);
      }

    }


    else {
      printf("Invalid command.\n");    
    }
    
  }
  
  kill_util();
  close(stream);
  shmdt((void*)sinfo);
  shmctl(shm_id, IPC_RMID, NULL);
  return 1;

}



