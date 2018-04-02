#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <fcntl.h>

/* Function prototypes */
void take_temperature(void);
void take_humidity(void);

/* Main execution loop */
int main()
{
  take_temperature();
  take_humidity();
}

void take_temperature()
{
  int   serialstream;
  char  command = '\x20';
  unsigned char  output[2];
  int   i;
  long  starttime;
  
  /* Record the start time for timeout */
  starttime = time(NULL);

  serialstream = open("/dev/ttyS3", O_RDWR);
  if (serialstream >= 0)
  {
    write(serialstream, &command, 1);
    for (i=0; i<2; i++) output[i] = 0;
    for (i=0; i<2; i++)
    {
      while (output[i] == 0 && ((time(NULL) - starttime) < 5))
      {
        read(serialstream, &output[i], 1);
      }
    }
    close(serialstream);
  }
  printf ("%3f,", (float)(((output[0] << 8) | output[1]) * 0.01 - 40));
}

void take_humidity()
{ 
  int   serialstream;
  char  command = '\x24';
  unsigned char  output[2];
  int   i;
  long  starttime;
  
  /* Record the start time for timeout */
  starttime = time(NULL);

  serialstream = open("/dev/ttyS3", O_RDWR);
  if (serialstream >= 0)
  {
    write(serialstream, &command, 1);
    for (i=0; i<2; i++) output[i] = 0;
    for (i=0; i<2; i++)
    {
      while (output[i] == 0 && ((time(NULL) - starttime) < 5))
      {
        read(serialstream, &output[i], 1);
      }
    }
    close(serialstream);
  }
  float SOrh = ((output[0] << 8) | output[1]);
  printf("%3f", (float)(0.0405 * SOrh - 2.8 * 0.000001 * SOrh * SOrh - 4));
}
