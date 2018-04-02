#include <msp430.h>

#define LED_0 BIT0
#define LED_1 BIT6
#define LED_OUT P1OUT
#define LED_DIR P1DIR
#define BUTTON BIT3

enum state {
    OFF = 0x00,
    ON  = 0xFF
};

void set_leds(enum state, enum state);

int main(void)
{
    WDTCTL = WDTPW | WDTHOLD;
    LED_DIR |= (LED_0 | LED_1);
    set_leds(OFF, OFF);
    P1IE |= BUTTON;

    __eint();

    while(1)
    {
        LPM4; // Enter low-power mode 4
    }
}

void set_leds(enum state led0_state, enum state led1_state)
{
    LED_OUT = (led0_state & LED_0) | (led1_state & LED_1);
}

__attribute__((interrupt(PORT1_VECTOR)))
void Port_1(void)
{
    short int i;
    P1IFG &= ~BUTTON; // P1.3 IFG clear
    for (i = 0; i < 10; i++)
    {
        set_leds(ON, OFF);
        __delay_cycles(200000);
        set_leds(OFF, ON);
        __delay_cycles(200000);
    }
    set_leds(OFF, OFF);
}
