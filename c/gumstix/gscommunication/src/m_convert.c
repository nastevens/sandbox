/*
  Performs the actual conversions of raw microcontroller data packets
  into human readable numbers.  View the functions stubs in m_convert.h
  for more information on the theory of operation behind each function.
*/
#include "uc_comm.h"
#include "m_convert.h"

float dp_to_temp(data_packet temppack)
{
  return (float)(((temppack.datafields[0] << 8) | temppack.datafields[1]) * 0.01 - 40);
}

float dp_to_humd(data_packet humdpack)
{
  float SOrh;
  SOrh = (humdpack.datafields[0] << 8) | humdpack.datafields[1]; 
  return 0.0405 * SOrh - 2.8 * 0.000001 * SOrh * SOrh - 4;
}

float dp_to_cond(data_packet condpack)
{
  return 0.0;
}

void dp_to_DRS(data_packet DRSpack, float* retarr)
{
  int i;
  
  for (i=0; i<4; i++)
  {
    retarr[i] = (float)(((DRSpack.datafields[2*i] << 8) | DRSpack.datafields[2*i+1]) * 5.0 / 1024.0);
  }
}
