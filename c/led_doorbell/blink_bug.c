#include <msp430.h>

#define LED_0 BIT0
#define LED_1 BIT6
#define LED_OUT P1OUT
#define LED_DIR P1DIR
#define BUTTON BIT3

unsigned int blink = 0;

void main(void)
{
    WDTCTL = WDTPW | WDTHOLD;
    LED_DIR |= (LED_0 | LED_1);
    LED_OUT &= ~(LED_0 | LED_1);
    P1IE |= BUTTON;

    __eint();

    while(1)
    {
        if(blink > 0)
        {
            P1OUT ^= (LED_0 | LED_1);
            __delay_cycles(100000);
        } 
    }
}

__attribute__((interrupt(PORT1_VECTOR)))
void Port_1(void)
{
    blink ^= 0x01;
    P1IFG &= ~BUTTON; // P1.3 IFG cleared
    LED_OUT &= ~(LED_0 | LED_1); // Clear LEDs
}
