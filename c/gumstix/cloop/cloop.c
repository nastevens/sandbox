/* cloop.c  -- Program for implementing a feedback control loop
   in order to estimate the conductance of skin */

#include <stdio.h>
#include <stdlib.h>

const double RB=100;
const int R1=3000;
const int VDD=4.788; 
const double VT=-2.0;

int main () {
  double ep;
  double rs;
  rs=0;
  do {
    ep = (VT - VDD * ((rs-R1)/(2*rs+RB)));
    /* TODO adjust the scaler on ep depending on difference */
    rs += ep;
    printf("Rs:%f  Ep:%f\n", rs, ep);
  }  while (ep > 0.001 || ep < -0.001);

  
}  
