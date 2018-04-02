#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>

int main ()
{
  FILE* stream;
  char  buffer;
  int   numread;


  stream = (FILE*) open("/dev/ttyS3", O_RDONLY);
  if (stream < 0) exit(-1);

  while (1)
  {
	numread = 0;
    while (numread < 1) numread += read(stream, &buffer, 1);
	printf("%d\n", (int)buffer);
  }

}
