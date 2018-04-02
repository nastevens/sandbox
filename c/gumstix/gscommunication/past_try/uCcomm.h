/* 
   uCcomm.h
   Contains the function prototypes for communicating with the data I/O
   microcontroller, as well as useful pnumonics for the various
   commands and responses
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/* Prototyping macro */
#define _PROTO(func, args) func args

/* Define constants */
/* uC Commands */
#define TAKE_TEMP 0x20
#define TAKE_HUMD 0x24
#define TAKE_COND 0x28
#define TAKE_DRS  0x2C
#define POP_STACK 0x40
#define DATA_ACK  0x48
#define DATA_NACK 0x54
#define SET_TIME  0x80
#define GET_TIME  0x84
#define RTC_ACK   0x88
#define RTC_NACK  0x94
#define SLEEP     0xE8
#define PING      0xE4
#define RESET_ALL 0xFC
#define BATTERY_STATUS   0xE0
#define WAKE_FROM_SLEEP  0xF4

/* uC Responses (only MS byte for cmds with return codes) */
#define DATA_READY       0x0
#define MEASURE_FAILED   0xC
#define BAT_STAT         0x1
//#define ACK_CMND       0x6 or 0x7 (five bit return code)
#define NACK_CMND        0x9
#define TIME_SET_SUCCESS 0x29
#define TIME_SET_FAILED  0x26
#define WAKE_READY       0xF0

/* Prototype functions */

/* Tries to open a connection to the microcontroller through serial
   port _device_ and then pings the microcontroller and waits for a response.
   Returns a file pointer to the serial device if successful, 0 if 
   the port initialization was successful, but the ping failed, and the
   file open error reporting code otherwise (<0). */
_PROTO( FILE* open_uC, ( char* device, int retries ) );

/* Sleeps uC (if connected) and closes the connection */
_PROTO(void close_uC, (FILE* handle));

/* Sends a byte down the serial port connection
   Always use this function to send data, do not send data directly!
   Using this function guarantees that only the one character that you
   want to be sent is sent... sending ints, longs, etc will pad the output 
   to the uC with 0's and probably confuse it 
   Returns 0 if successful and the error reporting code otherwise */
_PROTO(int send_byte, (FILE* handle, char data_byte));

/* Sends multiple bytes down the serial port connection given by _handle_
   Bytes to be sent are stored in a char array and fed out from index 0 to
   index _length_ .
   Returns 0 if successful and the error reporting code otherwise */
_PROTO(int send_byte_array, (FILE* handle, char* data_bytes, int length));
