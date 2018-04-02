/*
  Data packet to measurement value conversion header file.  Functions
  declared in this header convert a raw data packet received from the 
  microcontroller and convert it into a human readable representation of
  the measurement.  In the case of measurements taken by the SHT75, it 
  will also test the CRC checksum sent from the SHT unit (performing the
  checksum is a cycle intensive procedure - it is better to wait and 
  handle it at 200+Mhz on the GumStix than it is to do it on the 1Mhz
  microcontroller).  Also, the DRS conversion routine returns values in 
  an array since taking a DRS measurement produces four voltage readings.

  Adding conversions for new measurment tools is done by declaring the 
  conversion here, implementing it in m_convert.c, 
  setting up the command module in the microcontroller, and adding 
  constant definitions for the command code, errors, etc into
  the uc_comm.h file
*/

/* Function prototypes */
float  dp_to_temp(data_packet temppack);
float  dp_to_humd(data_packet humdpack);
float  dp_to_cond(data_packet condpack);
void   dp_to_DRS(data_packet DRSpack, float* retarr);
