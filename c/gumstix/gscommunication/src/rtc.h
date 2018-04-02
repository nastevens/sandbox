/*
  Header file for functions used to encode and decode times and dates
  from the Dallas Semiconductor RTC chip
*/

/* Function prototypes */
void RTC_to_tm(char* rtctime, struct tm* timestruct);
void tm_to_RTC(struct tm timestruct, char* rtctime);
