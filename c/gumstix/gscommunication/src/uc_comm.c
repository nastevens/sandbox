/*
  Functions for communicating with the microncontroller
*/

/* General includes */
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <termios.h>

/* Program specific includes */
#include "uc_comm.h"

/*
  Sends a command to the microcontroller w/o waiting for data to 
  returned.  Still checks for a command ACK from the uC and errors
  if not received.  Returns 0 if successful, or following errors if not:

  ERROR_OPENING_DEVICE
  ERROR_ACK_NOT_RECEIVED
  ERROR_TIMEOUT
  ERROR_CORRUPT_COMMAND
*/
int uc_send_only (char command)
{
  FILE* stream;		/* File stream to serial port */
  char  ack;		/* ACK to check command receipt */
  int   numread;	/* Number of bytes read from serial port */
  int   numwrote;	/* Number of bytes written to serial port */
  #ifdef DEBUG
    int   i;
  #endif

  /* Open stream to serial port for read/write */
  stream = (FILE*) open(device, O_RDWR);
  if (stream < 0) return ERROR_OPENING_DEVICE;

  /* Write command byte to microcontroller */
  numwrote = write(stream, &command, 1);
  #ifdef DEBUG
    printf("Wrote %d byte(s) of command %d to %s\n", numwrote, (int)command, device);
  #endif

  /* Read ACKnowledge byte from uC, check for consistancy
     with command that was sent */
  /* TODO implement timeout waiting for ACK */
  numread = 0;
  while(numread < 1) numread += read(stream, &ack, 1);
  if (numread < 1) return ERROR_ACK_NOT_RECEIVED;
  if ((ack & '\x1F') != ((command>>2) & '\x1F')) return ERROR_CORRUPT_COMMAND;
  #ifdef DEBUG
    printf("Received ACK of %d from %s\n", (int)ack, device);
  #endif

  /* Done - close stream and exit */
  close(stream);
  return 0;
} 


/* 
  Send a command, waits for an ACKnowledge, and then waits until a data
  packet is ready.  Reads the data packet from the device and returns it 
  to the calling function in _retpack_.  Returns 0 if the command was 
  successful, or one of the following codes if it was not:

  ERROR_OPENING_DEVICE
  ERROR_ACK_NOT_RECEIVED
  ERROR_TIMEOUT
  ERROR_CORRUPT_COMMAND
  ERROR_UNEXPECTED_RESPONSE
*/
int uc_send_receive (char command, data_packet *retpack)
{
  FILE* stream;              /* File stream to serial port */
  char  ack;                 /* ACK to check command receipt */
  char  char_buf;            /* Buffer for transferring #defines to a var */
  char  packet_header[3];    /* Preamble, command byte, len and err nibbles */
  char  packet_footer[2];    /* CRC byte, postamble */
  char  data_fields[16];     /* Packet data payload */
  int   numread;             /* Number of bytes read from device */
  int   numwrote;            /* Number of bytes written to the device */
  char  junkdata[32];        /* Flush the serial device before write */
  #ifdef DEBUG
    int   i;
  #endif

  /* Open the stream to the serial port device */
  stream = (FILE*) open(device, O_RDWR);
  if (stream < 0) return ERROR_OPENING_DEVICE;
  
  /* Try to read junk bytes out of the serial buffer */
  numread = read(stream, junkdata, 32);
  #ifdef DEBUG
    printf("Read %d bytes of junk data from %s\n", numread, device);
  #endif
  
  /* Write the command byte to the device */
  numwrote = write(stream, &command, 1);
  #ifdef DEBUG
    printf("Wrote %d byte(s) of command %d to %s\n", numwrote, (int)command, device);
  #endif

  /* Read ACKnowledge byte from uC, check for consistancy
     with command that was sent */
  /* TODO implement timeout waiting for ACK */
  numread = 0;
  while (numread < 1) numread += read(stream, &ack, 1);
  if (numread < 1) return ERROR_ACK_NOT_RECEIVED;
  #ifdef DEBUG
    printf("Received ACK of %d from %s\n", (int)ack, device);
  #endif
  if ((ack & '\x1F') != ((command>>2) & '\x1F')) return ERROR_CORRUPT_COMMAND;

  /* Wait until uC is done taking measurement.  It will then send another
     ACK (PACKET_PRESENT) indicating that there is data ready to be
     retrieved.  Check to make sure it's actually the right response */
  /* TODO implement a timeout waiting for data */
  numread = 0;
  while(numread < 1) numread += read(stream, &ack, 1);
  if (numread < 1) return ERROR_ACK_NOT_RECEIVED;
  if (ack != PACKET_PRESENT) return ERROR_UNEXPECTED_RESPONSE;
  #ifdef DEBUG
    printf("Received PACKET_PRESENT of %d from %s\n", (int)ack, device);
  #endif
  
  /* Move the command to SEND_PACKET to a buffer to transfer to function, 
     and then enter receive mode to accept the packet */
  char_buf = SEND_PACKET;
  write(stream, &char_buf, 1);
  #ifdef DEBUG
    printf("Requested SEND_PACKET of %d on %s\n", (int)char_buf, device);
  #endif    

  /* Read ACKnowledge byte from uC, check for consistancy
     with command that was sent */
  /* TODO implement timeout waiting for ACK */
  numread = 0;
  while (numread < 1) numread += read(stream, &ack, 1);
  #ifdef DEBUG
    printf("Received ACK of %d from %s\n", (int)ack, device);
  #endif
  if (numread < 1) return ERROR_ACK_NOT_RECEIVED;
  if ((ack & '\x1F') != ((char_buf>>2) & '\x1F')) return ERROR_CORRUPT_COMMAND;

/* Begin reading the packet stream, starting with the packet header
     information.  We'll use the len field of the header to determine how
     many data bytes we should expect */  
  numread = 0;
  while (numread < 3) numread += read(stream, &packet_header[numread], 1);
  if (numread != 3 || packet_header[0] != PACKET_PREAMBLE) return ERROR_UNEXPECTED_RESPONSE;
  #ifdef DEBUG
    printf("Read packet header of %d bytes from %s\n", numread, device);
    for (i=0; i<numread; i++) printf("Header b%d: %d\t", i, (int)packet_header[i]);
    printf("\n");
  #endif

  /* Copy the 2 salient bytes of the packet header into the return packet.
     Mask the 3rd byte to get the error nibble and the length nibble */
  retpack->command   = packet_header[1];
  retpack->dfieldlen = (int)(packet_header[2] & '\x0F');
  retpack->errcodes  = (int)((packet_header[2] >> 4) & '\x0F');
  
  /* Using the length of the data field pulled from the packet header, 
     read that many data bytes and store into a temporary data fields
     variable */
  numread = 0;
  while (numread < retpack->dfieldlen) numread += read(stream, &retpack->datafields[numread], 1);
  //numread = read(stream, retpack->datafields, retpack->dfieldlen);
  if (numread != retpack->dfieldlen) return ERROR_LENGTH_MISMATCH;
  #ifdef DEBUG
    printf("Packet header indicates %d bytes, read %d bytes\n", retpack->dfieldlen, numread);
    for (i=0; i<numread; i+=2) 
    {
      printf("Data b%d:%d\tData b%d:%d\n", i, (int)retpack->datafields[i], i+1, (i == retpack->dfieldlen + 1) ? 0 : (int)retpack->datafields[i+1]);
    }
  #endif

  /* Read the last two bytes of the packet - the CRC checksum byte and 
     the postamble */
  numread = 0;
  while (numread < 2) numread += read(stream, &packet_footer[numread], 1);
  #ifdef DEBUG
    printf("Read packet footer of %d bytes from %s\n", numread, device);
    for (i=0; i<numread; i++) printf("Footer b%d: %d\t", i, (int)packet_footer[i]);
    printf("\n");
  #endif
  if ((numread != 2) || (packet_footer[1] != PACKET_POSTAMBLE)) return ERROR_UNEXPECTED_RESPONSE;
  retpack->crcbyte = packet_footer[0];

  /* If the packet was successfully received, send a PACKET_ACK to have the
     microcontroller clear the data buffer and be ready for the next command */
  /* TODO: code so that a failed read can try 2 or 3 more times */
  char_buf = PACKET_ACK;
  numwrote = write(stream, &char_buf, 1);
  #ifdef DEBUG
    printf("Wrote %d byte(s) of PACKET_ACK %s\n", numwrote, device);
  #endif

  /* Read ACKnowledge byte from uC, check for consistancy
     with command that was sent */
  /* TODO implement timeout waiting for ACK */
  numread = 0;
  while(numread < 1) numread += read(stream, &ack, 1);
  #ifdef DEBUG
    printf("Received ACK of %d from %s\n", (int)ack, device);
  #endif
  if (numread < 1) return ERROR_ACK_NOT_RECEIVED;
  if ((ack & '\x1F') != ((char_buf>>2) & '\x1F')) return ERROR_CORRUPT_COMMAND;

  /* All done, close stream and return success */
  close(stream);
  return 0;

}

void uc_error_handle(int errorcode)
{
  printf("This is the error code handler\n");
  printf("Unfortunately, I received error %d\n", errorcode);
}


void get_time(char* rtcdata)
{
  int         i;
  data_packet results;

  uc_send_receive(GET_TIME, &results);
  for (i=0; i<7; i++) rtcdata[i] = results.datafields[i];

}

void short_beep(void)
{
  int status;
  status = uc_send_only(SHORT_BEEP);
  if (status < 0) uc_error_handle(status);
  return;
}

void long_beep(void)
{
  int status;
  status = uc_send_only(LONG_BEEP);
  if (status < 0) uc_error_handle(status);
  return;
}

int set_time(char* timestring)
{
  FILE* stream;
  char  ack;
  int   numread;
  char  p_buf;
  int   numsent;
#ifdef DEBUG
  int   i;
#endif

  stream = (FILE*) open(device, O_RDWR);
#ifdef DEBUG
  printf("Opened device %s, given file pointer %d\n", device, stream);
#endif

  if (stream >= 0)
  {
    p_buf = '\x40';
    write(stream, &p_buf, 1);
#ifdef DEBUG
    printf("Wrote command SET_TIME to %s\n", device);
#endif
    
    numread = 0;
    while (numread < 1) numread += read(stream, &ack, 1);

#ifdef DEBUG
    printf("Received ACK of %d from %s\n", (int)ack, device);
#endif

    numsent = write(stream, timestring, 8);

#ifdef DEBUG
    printf("Wrote %d bytes to %s\n", numsent, device);
    for(i=0; i<8; i++) printf("%d ", (int)timestring[i]);
#endif

    close(stream);
    return 0;
  }

}


