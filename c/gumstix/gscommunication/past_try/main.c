/* 
   main.c
   The main controls sections of the program
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "uCcomm.h"

/* Lay out program process of events:
   1) See if we are connected to the PC or not
      Yes: Goto data transfer/time update routines --B--
      No:  Goto data collection routines --A--
   --A--
   1) Make sure that memory card is connected, mounted, and get a tally
      available space
   2) Start up the microcontroller and verify that we can talk to it
   3) Synchronize the GumStix clock to the RTC clock
   4) Load the measurement configuration file (which measurements, how often,
      how long to run)
   5) Begin timers for each of the measurements
   6) Perform requested measurements at intervals set off by the timing alarms
   7) When total test time is expired, or battery warning has been tripped,
      finish collecting data from microcontroller and shut it down.  Shutdown
      GumStix.
   --B--
   1) Wait for command from PC
   2) Send data if requested
   3) If time update is received:
      i)   Start up microcontroller and verify that we can talk to it
      ii)  Get reading from RTC
      iii) Show reading to PC
      iv)  PC sends updated timestamp
      v)   Send updated time to microcontroller
      vi)  Verify time sent successfully
      vii) Report success to PC
*/

int main(char** argv, int argc)
{
  open_uC("/dev/ttyS0", 3);
}
