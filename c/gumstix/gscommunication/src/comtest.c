/* 
  Suite of test facilities for testing the connection between the GumStix
  microcomputer and the PIC microcontroller.  Takes user input from a 
  menu based interface and then performs the requested action with the
  microcontroller.  Uses the uc_comm.c and uc_comm.h
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
  data_packet respack;          /* Packet of results from microcontroller */
  char    choice[2] = {'0','\0'};  /* Menu choice, null term string */
  int     numvalue;             /* Numerical value of menu choice */
  float   result;               /* Returned measurement, single float number */
  float*  resultarr;            /* Returned measurements, float number array */
  char    rtcarr[8];            /* Array of RTC bytes */
  char    timestring[26];       /* String representation of time */
  struct  tm timestruct;        /* The tm structure returned from ctime */
  char    inputstring[21];      /* Input string for the date and time */
  int     ucretcode;            /* uc communication return code */
  int     i;                    /* Generic counter */
  
  /* Display selection menu and loop until quit */
  while(true) {
    system("clear");
    printf("Microcontroller Communication Test Panel\n\n");
    printf("\tOptions:\n");
    printf("\t--------\n");
    printf("\t1) Take temperature reading\n");
    printf("\t2) Take humidity reading\n");
    printf("\t3) Take conductance reading\n");
    printf("\t4) Take DRS reading\n\n");
    printf("\t5) Read real-time clock\n");
    printf("\t6) Write real-time clock\n\n");
    printf("\t7) Short beep\n");
    printf("\t8) Long beep\n\n");
    printf("\t9) Quit program\n\n");
    printf("\t\tEnter choice (1-9):");
    
    /* Get the user's choice, convert to an integer */
    choice[0] = getchar();
    numvalue = atoi(&choice[0]);

    /* Switch statement dispatches the program to perform the selected task */
    switch (numvalue) {
      
      case 1:
	if ((ucretcode = uc_send_receive(TAKE_TEMP,&respack)) < 0)
	{
	  uc_error_handle(ucretcode);
	} else {
	  printf("\n\n\tResult: %2f degrees C\n\n", dp_to_temp(respack));
	}
	choice[0] = getchar();
        break;
      
      case 2:
	if ((ucretcode = uc_send_receive(TAKE_HUMD, &respack)) < 0)
	{
	  uc_error_handle(ucretcode);
	} else {
	  printf("\n\n\tResult: %2f RH\n\n", dp_to_humd(respack));
	}
	choice[0] = getchar();
        break;
      
      case 3:
        printf("\n\n\tResult: %d mS\n\n", 0);
	choice[0] = getchar();
        break;
      
      case 4:
	if ((ucretcode = uc_send_receive(TAKE_DRS, &respack)) < 0)
	{
	  uc_error_handle(ucretcode);
	} else {
	  float voltages[4];
	  dp_to_DRS(respack, voltages);
	  printf("\n\n");
	  for(i=0; i<4; i++) printf("\tLED%d: %2f Volts\n", i, voltages[i]);
        }
	choice[0] = getchar();
        break;
      
      case 5:
        get_time(rtcarr);
	RTC_to_tm(rtcarr, &timestruct);
	asctime_r(&timestruct, timestring);
	printf("\n\n\tRTC Time: %s\n", timestring);
	choice[0] = getchar();
	break;
      
      case 6:
	printf("\nEnter time to set in format (YY:MM:DD:hh:mm:ss:WD): ");
        scanf("%s", &inputstring);
        strptime(inputstring, "%y:%m:%d:%H:%M:%S:%w", &timestruct);
        tm_to_RTC(timestruct, rtcarr);
        set_time(rtcarr);
	choice[0] = getchar();
	break;
      
      case 7:
      	short_beep();
	choice[0] = getchar();
        break;
      
      case 8:
      	long_beep();
	choice[0] = getchar();
	break;
      
      case 9:
        return;

      default:
        printf("Invalid selection\n");
        break;
    }
	choice[0] = getchar();
  }
}

