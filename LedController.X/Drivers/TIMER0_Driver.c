#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <xc.h>
#include <string.h>

#include "PORT_Driver.h"
#include "TIMER0_Driver.h"

/*******************************************************************************
 *          DEFINES
 ******************************************************************************/

/*******************************************************************************
 *          MACRO FUNCTIONS
 ******************************************************************************/

/*******************************************************************************
 *          VARIABLES
 ******************************************************************************/

/*******************************************************************************
 *          BASIC FUNCTIONS
 ******************************************************************************/

/*******************************************************************************
 *          DRIVER FUNCTIONS
 ******************************************************************************/
void D_TIMER0_Init(uint8_t prescale){
    D_TIMER0_Enable(false);
    
    // T0CON register settings
    T0CONbits.T08BIT = 1; // Timer0 is configured as an 8-bit timer/counter
    T0CONbits.T0CS = 0; // Internal instruction cycle clock (CLKO)
    T0CONbits.PSA = 1; // Timer0 pre-scaler is assigned. Timer0 clock input comes from pre-scaler output.
    switch(prescale) {
        default:
            T0CONbits.T0PS = 0b000; break;
        case 2:   T0CONbits.T0PS = 0b000; break;
        case 4:   T0CONbits.T0PS = 0b001; break;
        case 8:   T0CONbits.T0PS = 0b010; break;
        case 16:  T0CONbits.T0PS = 0b011; break;
        case 32:  T0CONbits.T0PS = 0b100; break;
        case 64:  T0CONbits.T0PS = 0b101; break;
        case 128: T0CONbits.T0PS = 0b110; break;
        case 256: T0CONbits.T0PS = 0b111; break;
    }
    TMR0L = 0;
    TMR0H = 0;
    
    // Interrupts timer
    RCONbits.IPEN = 1;   // Enable priority levels on interrupts
    INTCONbits.GIEH = 1; // Enable high interrupt
    INTCONbits.GIEL = 1; // Enable low interrupt
    INTCONbits.TMR0IE = 0; // Wait for enable
    INTCONbits.TMR0IF = 0; // Clear flag
    INTCON2bits.TMR0IP = 1; // Hight priority
}

void D_TIMER0_Enable(bool enable) {
    if (enable) {
        T0CONbits.TMR0ON = 1;
        INTCONbits.TMR0IE = 1;
        D_TIMER0_Flag = false;
    } else {
        T0CONbits.TMR0ON = 0;
        INTCONbits.TMR0IE = 0;
        D_TIMER0_Flag = false;
    }
}



