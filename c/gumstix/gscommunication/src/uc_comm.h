/* 
   The microcontroller communications header file.  Contains the definitions
   of functions and constants used when talking to the microcontroller.
*/

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <termios.h>

#define true  1
#define false 0
#define device "/dev/ttyS3"

/* Microcontroller command definitions */
#define TAKE_TEMP         '\x00'
#define TAKE_HUMD         '\x04'
#define TAKE_COND         '\x08'
#define TAKE_DRS          '\x0C'

#define SEND_PACKET       '\x20'
#define PACKET_ACK        '\x24'

#define SET_TIME          '\x40'
#define GET_TIME          '\x44'

#define BATT_STATUS       '\x60'
#define SLEEP             '\x64'
#define WAKE              '\x68'
#define PING              '\x6C'
#define RESET_ALL         '\x70'
#define SHORT_BEEP        '\x74'
#define LONG_BEEP         '\x78'

/* Microcontroller responses/interrupts */
/* Note that ACK and NACK contain variable data, so no defs here */
#define PACKET_PRESENT    '\x0A'
#define TIME_SET_SUCCESS  '\x29'
#define TIME_SET_FAILED   '\x26'
#define WAKE_READY        '\xF0'

/* Microcontroller error code definitions */
#define NO_ERROR          '\x00'
#define COMMAND_PENDING   '\x01'
#define UNREAD_PACKET     '\x02'
#define NO_PACKET_PRESENT '\x03'
#define DEV_COMM_ERROR    '\x04'
#define COMMAND_DROPPED   '\x05'
#define INVALID_COMMAND   '\x06'
#define TIMEOUT           '\x07'

/* Microcontroller constants */
#define PACKET_PREAMBLE   '\xCC'
#define PACKET_POSTAMBLE  '\x33'

/* Communication error code definitions */
#define ERROR_OPENING_DEVICE   (-1)
#define ERROR_ACK_NOT_RECEIVED (-2)
#define ERROR_CORRUPT_COMMAND  (-3)
#define ERROR_TIMEOUT          (-4)
#define ERROR_UNEXPECTED_RESPONSE (-5)
#define ERROR_LENGTH_MISMATCH  (-6)
/* Turn on DEBUG code on/off */
#define DEBUG

/* Define data packet structure for receiving data from the uC */
typedef struct dp
{
  int   comm_error;      /* Communication error field */
  char  command;         /* Copy of the command */
  int   dfieldlen;       /* Length of the data field */
  char  datafields[16];  /* 16 bytes (max) of probe data */
  char  crcbyte;         /* Cyclic reducdancy check byte */
  int   errcodes;        /* Microcontroller error field */
} data_packet;

/* Communication function prototypes */
int      uc_send_receive  (char command, data_packet* retpack);
int      uc_send_only     (char command);
void     uc_error_handle  (int errorcode);
float    take_temperature (void);
float    take_humidity    (void);
float    take_conductance (void);
float*   take_DRS         (void);
void     get_time         (char* rtcdata);
int      set_time         (char* timestring);
void     short_beep       (void);
void     long_beep        (void);

