#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <sys/time.h>

int main ()
{
  char  hard_time[8] = {'\x00','\x41','\x94','\x18','\x10','\x02','\x04','\x00'};
  char  timestring[26];
  char  inputstring[13];
  struct tm timestruct;
  struct timeval timeval;
  struct timezone timezone;
  
  timestruct.tm_sec  = (int)(hard_time[0] & '\x7F');
  timestruct.tm_min  = (int)(((hard_time[1] & '\xF0') >> 4) * 10 + (hard_time[1] & '\x0F'));
  timestruct.tm_hour = (int)(((hard_time[2] & '\x30') >> 4) * 10 + (hard_time[2] & '\x0F'));
  timestruct.tm_mday = (int)(((hard_time[3] & '\x30') >> 4) * 10 + (hard_time[3] & '\x0F'));
  timestruct.tm_mon  = (int)((((hard_time[4] & '\x10') >> 4) * 10 + (hard_time[4] & '\x0F')) - 1);
  timestruct.tm_wday = (int)((hard_time[5] & '\x07') - 1);
  timestruct.tm_year = (int)((((hard_time[6] & '\xF0') >> 4) * 10 + (hard_time[6] & '\x0F')) + 100);

  asctime_r(&timestruct, timestring);
  
  printf("%s", timestring);

  printf("\nEnter time to set in format YYMMDDhhmmss:");
  scanf("%s", &inputstring);
  strptime(inputstring, "%y%m%d%H%M%S", &timestruct);

  //gettimeofday(&timeval, &timezone);
  //localtime_r(&timeval.tv_sec, &timestruct);
  
  printf("%d\n", (unsigned int)(char)((((timestruct.tm_sec / 10) << 4) & '\x70') | ((timestruct.tm_sec % 10) & '\x0F')));
  printf("%d\n", (unsigned int)(char)((((timestruct.tm_min / 10) << 4) & '\x70') | ((timestruct.tm_min % 10) & '\x0F')));
  printf("%d\n", (unsigned int)(char)(((((timestruct.tm_hour / 10) << 4) & '\x30') | '\x80') | ((timestruct.tm_hour % 10) & '\x0F')));
  printf("%d\n", (unsigned int)(char)((((timestruct.tm_mday / 10) << 4) & '\x30') | ((timestruct.tm_mday % 10) & '\x0F')));
  printf("%d\n", (unsigned int)(char)(((((timestruct.tm_mon + 1) / 10) << 4) & '\x10') | (((timestruct.tm_mon + 1) % 10) & '\x0F')));
  printf("%d\n", (unsigned int)(char)((timestruct.tm_wday + 1) & '\x07'));
  printf("%d\n", (unsigned int)(char)(((((timestruct.tm_year - 100) / 10) << 4) & '\xF0') | (((timestruct.tm_year - 100) % 10) & '\x0F')));
  printf("%d\n", (unsigned int)'\x00');

}
