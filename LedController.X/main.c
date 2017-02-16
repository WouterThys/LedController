/*
 * File:   main.c
 * Author: wouter
 *
 * Created on October 22, 2016, 5:17 PM
 */
#include <xc.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>

#include "Drivers/TIMER0_Driver.h"
#include "Drivers/PORT_Driver.h"
#include "Drivers/UART_Driver.h"
#include "Drivers/PWM_Driver.h"

#define _XTAL_FREQ 48000000

#define COMMAND_R "R" /* Red */
#define COMMAND_G "G" /* Green */  
#define COMMAND_B "B" /* Blue */
#define COMMAND_S "S" /* Scale */

#define COMMAND_RGB "RGB" /* Get RGB */
#define COMMAND_SCA "SCA" /* Get Scale */
#define COMMAND_STA "STA" /* Get State */

#define COMMAND_FL "FL" /* Flash */
#define COMMAND_ST "ST" /* Strobe */
#define COMMAND_FA "FA" /* Fade */
#define COMMAND_SM "SM" /* Smooth */

#define MESSAGE_U "U" /* Up */
#define MESSAGE_D "D" /* Down */ 

READ_Data read;
uint8_t r;
uint8_t g;
uint8_t b;

void initialize();
void handle_message(READ_Data msg);
uint8_t strToInt(const char* str);

void initialize() {
    D_PORT_Init();
    // Initialize the UART module with a baud rate of 9600, with the use 
    // of interrupts.
    D_UART_Init("P", 19200, true);
    D_UART_Enable(true);
    
    // PWM
    D_PWM_Init();
    D_PWM_Enable(true);
    
    // Local variables
    r = 128;
    g = 128;
    b = 128;
    
    D_UART_Write("I", "init");
}

void main(void) {
    
    initialize();
    
    D_PWM_SetRGB(0xff, 0xff, 0xff);
    
    while(1) {
        
        if (D_UART_ReadFlag) {
            D_UART_ReadFlag = false;
            uint8_t length = D_UART_BlockLength();
            if (length == 1) {
                handle_message(D_UART_Read());
            } else if (length > 1) {
                uint8_t i;
                for (i=0; i < length; i++) {
                    handle_message(D_UART_ReadBlock(i));
                }
            }
        }    
    }
    return;
}


void handle_message(READ_Data msg) { 
    if (strcmp(msg.command, COMMAND_R) == 0) {  
        r = strToInt(msg.message);
        D_PWM_SetRGB(r, g, b);
        return;
    } 

    if (strcmp(msg.command, COMMAND_G) == 0) {
        g = strToInt(msg.message);
        D_PWM_SetRGB(r, g, b);
        return;
    } 
    
    if (strcmp(msg.command, COMMAND_B) == 0) {
        b = strToInt(msg.message); 
        D_PWM_SetRGB(r, g, b);
        return;
    } 
    
    if (strcmp(msg.command, COMMAND_S) == 0) {
        if (strcmp(msg.message, MESSAGE_D) == 0) {
            D_PWM_ScaleDown();
        }
        if (strcmp(msg.message, MESSAGE_U) == 0) {
            D_PWM_ScaleUp();
        }
        return;
    }
    
    if (strcmp(msg.command, COMMAND_FL) == 0) {
        D_PWM_Flash();
        return;
    } 
    
    if (strcmp(msg.command, COMMAND_ST) == 0) {
        D_PWM_Strobe();
        return;
    } 
    
    if (strcmp(msg.command, COMMAND_FA) == 0) {
        D_PWM_Fade();
        return;
    } 
    
    if (strcmp(msg.command, COMMAND_SM) == 0) {
        D_PWM_Smooth();
        return;
    } 
    
    if(strcmp(msg.command, COMMAND_RGB) == 0) {
        D_UART_WriteInt(COMMAND_R, D_PWM_GetRed());
        __delay_us(10);
        D_UART_WriteInt(COMMAND_G, D_PWM_GetGreen());
        __delay_us(10);
        D_UART_WriteInt(COMMAND_B, D_PWM_GetBlue());
        __delay_us(10);
        return;
    }
    
    if(strcmp(msg.command, COMMAND_SCA) == 0) {
        D_UART_WriteInt(COMMAND_SCA, D_PWM_GetScale());
        return;
    }
    
    if(strcmp(msg.command, COMMAND_STA) == 0) {
        D_UART_WriteInt(COMMAND_STA, D_PWM_GetState());
        return;
    }
}

uint8_t strToInt(const char* str) {
    uint8_t val = 0;
    uint8_t tmp = 0;
    uint8_t shift = 0;
    while(*str != '\0') {
        tmp = *str - 0x30;
        if (shift != 0) {
            val *= 10;
        }
        val += tmp;
        shift++;
        str++;
    }
    return val;
}