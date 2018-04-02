/* 
  Modified version of the comtest testing facilities.  This is the 
  comdaemon (a daemon being a *nix program that runs at startup and forks 
  to the background, the same thing as a TSR in Windows terms).  It will
  run on the GumStix and wait for input to take readings and store them
  onto the MMC card. Uses the uc_comm.c and uc_comm.h
  files for functions to communicate with the microcontroller, the 
  m_convert.c and m_convert.h files for converting raw probe data to
  real numbers, and the rtc.c and rtc.h files for performing functions on
  data received and transmitted to the Real Time Clock.

  Setting the DEBUG define will turn on debug code throughout the program,
  including advanced information on the status of communication with the 
  microcontroller as well as printing out intermediate steps of complex
  computations.
*/

/* Turn DEBUG code on/off */
#define DEBUG

/* Standard includes */
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <time.h>
//#include <sys/time.h>

/* Program specific includes */
#include "uc_comm.h"
#include "rtc.h"
#include "m_convert.h"

/* 
  Main program loop - waits for a command from the user interface and then
  dispatches the command to the proper functions
*/  
int main (void) {
  data_packet  respack;
  pid_t   pid;					/* Process ID (PID) */
  char    bp;					/* Button push */
  int     numread;				/* Number of bytes read */
  FILE*   stream;
  char    junkdata[32];			/* Read junk data */
  
  /* Daemonize the process */
  if ((pid = fork()) != 0) exit(0);
  setsid();

  /* Beep to let know active */
  usleep(500000);
  short_beep();
  usleep(500000);
  short_beep();
  usleep(500000);
  short_beep();

  /* Wait for pushbutton signal */
  stream = (FILE*) open("/dev/ttyS3", O_RDONLY);
  while(1)
  {
    numread = 0;
	while (numread < 1) numread += read(stream, &bp, 1);
    if(bp == 240)
	{
	  usleep(200000);
	  read(stream, &junkdata, 32);
	  short_beep();
	  sleep(1);
	  short_beep();
	  sleep(1);
	  short_beep();
	  sleep(1);
	  long_beep();
	  sleep(1);
	  uc_send_receive(TAKE_TEMP, &respack);
	  dp_to_temp(respack);
	  usleep(500000);
	  uc_send_receive(TAKE_HUMD, &respack);
	  usleep(500000);
	  uc_send_receive(TAKE_DRS, &respack);
	  usleep(1);
	  short_beep();
	  usleep(200000);
	  short_beep();
	  usleep(200000);
	  short_beep();
	}
	usleep(500000);
	numread = 0;
	do {
	  numread = read(stream, &bp, 1);
	} while (numread != 0);
  }	

}
