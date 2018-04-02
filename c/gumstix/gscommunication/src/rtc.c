/*
  Functions used to decode and encode times for the Dallas Semiconductor
  RTC chip
*/

#include <time.h>
#include <sys/time.h>
#include "rtc.h"


/* Convert RTC time array (7 bytes) to a tm time struct */
void RTC_to_tm(char* rtctime, struct tm* timestruct)
{
  timestruct->tm_sec  = (int)(((rtctime[0] & '\xF0') >> 4) * 10 + (rtctime[0] & '\x0F'));
  timestruct->tm_min  = (int)(((rtctime[1] & '\xF0') >> 4) * 10 + (rtctime[1] & '\x0F'));
  timestruct->tm_hour = (int)(((rtctime[2] & '\x30') >> 4) * 10 + (rtctime[2] & '\x0F'));
  timestruct->tm_mday = (int)(((rtctime[3] & '\x30') >> 4) * 10 + (rtctime[3] & '\x0F'));
  timestruct->tm_mon  = (int)((((rtctime[4] & '\x10') >> 4) * 10 + (rtctime[4] & '\x0F')) - 1);
  timestruct->tm_wday = (int)((rtctime[5] & '\x07') - 1);
  timestruct->tm_year = (int)((((rtctime[6] & '\xF0') >> 4) * 10 + (rtctime[6] & '\x0F')) + 100);
}

/* Convert tm structure to RTC time (8 bytes) */
void tm_to_RTC(struct tm timestruct, char* result)
{
  result[0] = (char)((((timestruct.tm_sec / 10) << 4) & '\x70') | ((timestruct.tm_sec % 10) & '\x0F'));
  result[1] = (char)((((timestruct.tm_min / 10) << 4) & '\x70') | ((timestruct.tm_min % 10) & '\x0F'));
  result[2] = (char)(((((timestruct.tm_hour / 10) << 4) & '\x30') | '\x80') | ((timestruct.tm_hour % 10) & '\x0F'));
  result[3] = (char)((((timestruct.tm_mday / 10) << 4) & '\x30') | ((timestruct.tm_mday % 10) & '\x0F'));
  result[4] = (char)(((((timestruct.tm_mon + 1) / 10) << 4) & '\x10') | (((timestruct.tm_mon + 1) % 10) & '\x0F'));
  result[5] = (char)((timestruct.tm_wday + 1) & '\x07');
  result[6] = (char)(((((timestruct.tm_year - 100) / 10) << 4) & '\xF0') | (((timestruct.tm_year - 100) % 10) & '\x0F'));
  result[7] = '\x00';

  #ifdef DEBUG
    int i;
    for (i=0; i<8; i++) printf("%d ", (int)result[i]);
    printf("\n");
  #endif
}
