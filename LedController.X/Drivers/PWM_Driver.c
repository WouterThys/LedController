#include <xc.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

#include "PWM_Driver.h"
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
static pwm_t PWM_Red, PWM_Green, PWM_Blue;
static uint8_t scale;
typedef enum {Color, Flash, Strobe, Fade, Smooth} states_t;
static states_t state;

/*******************************************************************************
 *          BASIC FUNCTIONS
 ******************************************************************************/
void setRGB(uint8_t r, uint8_t g, uint8_t b);
void pwmColors(uint8_t birghtness);
void handleState(void);
void flash(void);
void strobe(void);
void fade(void);
void smooth(void);

void setRGB(uint8_t r, uint8_t g, uint8_t b) {
    D_PWM_SetDuty(PWM_R, r);
    D_PWM_SetDuty(PWM_G, g);
    D_PWM_SetDuty(PWM_B, b);
}

void pwmColors(uint8_t birghtness) {
    // Duty checks
    if (PWM_Red.duty_cnt >= (PWM_Red.duty_val >> birghtness)) {
        R_PORT = 0;
    } else {
        R_PORT = 1;
    }
    
    if (PWM_Green.duty_cnt >= (PWM_Green.duty_val >> birghtness)) {
        G_PORT = 0;
    } else {
        G_PORT = 1;
    }
    
    if (PWM_Blue.duty_cnt >= (PWM_Blue.duty_val >> birghtness)) {
        B_PORT = 0;
    } else {
        B_PORT = 1;
    }
    
    // Duty counts
    PWM_Red.duty_cnt++;
    PWM_Green.duty_cnt++;
    PWM_Blue.duty_cnt++;
}

void flash(void) {
    static uint8_t count;
    static uint8_t color;
    
    if (count >= (0xFF >> scale)) {
        count = 0;
    }
    if (count == 0) {
        switch(color) {
            case 0: 
                setRGB(255, 0, 0);
                color = 1;
                break;
            case 1: 
                setRGB(0, 255, 0);
                color = 2;
                break;
            case 2: 
                setRGB(0, 0, 255);
                color = 3;
                break;    
            case 3: 
                setRGB(255, 255, 255);
                color = 0;
                break;    
        }
    }
    
    count++;
}

void strobe(void) {
    static uint8_t cnt;
    static bool up;
    
    if (cnt > 0xF7) {
        up = false;
    }
    if (cnt < 8) {
        up = true;
    }

    if (up) {
        cnt+=(scale+1);
    } else {
        cnt-=(scale+1);
    }
    
    setRGB(cnt, cnt, cnt);
}

void fade(void) {
    static uint8_t r_cnt = 0x00;
    static uint8_t g_cnt = 0x80;
    static uint8_t b_cnt = 0xFF;
    static bool r_up;
    static bool g_up;
    static bool b_up;
    
    if (r_cnt > 0xF7) {
        r_up = false;
    }
    if (r_cnt < 8) {
        r_up = true;
    }
    
    if (g_cnt > 0xF7) {
        g_up = false;
    }
    if (g_cnt < 8) {
        g_up = true;
    }
    
    if (b_cnt > 0xF7) {
        b_up = false;
    }
    if (b_cnt < 8) {
        b_up = true;
    }
    
    if (r_up) {
        r_cnt+=(scale+1);
    } else {
        r_cnt-=(scale+1);
    }
    
    if (g_up) {
        g_cnt+=(scale+1);
    } else {
        g_cnt-=(scale+1);
    }
    
    if (b_up) {
        b_cnt+=(scale+1);
    } else {
        b_cnt-=(scale+1);
    }
    
    setRGB(r_cnt, g_cnt, b_cnt);
}

void smooth(void) {
    static uint8_t count;
    static uint8_t color;
    
    if (count >= (0xFF >> scale)) {
        count = 0;
    }
    if (count == 0) {
        switch(color) {
            case 0: 
                setRGB(255, 0, 0);
                color = 1;
                break;
            case 1: 
                setRGB(255, 255, 0);
                color = 2;
                break;
            case 2: 
                setRGB(0, 255, 0);
                color = 3;
                break;    
            case 3: 
                setRGB(0, 255, 255);
                color = 4;
                break;    
            case 4: 
                setRGB(0, 0, 255);
                color = 5;
                break;  
            case 5: 
                setRGB(255, 0, 255);
                color = 0;
                break;   
        }
    }
    
    count++;
}

void handleState() {
    static uint8_t cnt;
    
    switch(state) {
        case Color:
            pwmColors(scale);
            break;
            
        case Flash:
            if (cnt == 0) {
                flash();
            }
            pwmColors(0);
            break;
            
        case Strobe:
            if (cnt == 0) {
                strobe();
            }
            pwmColors(0);
            break;
            
        case Fade:
            if (cnt == 0) {
                fade();
            }
            pwmColors(0);
            break;
            
        case Smooth:
            if (cnt == 0) {
                smooth();
            }
            pwmColors(0);
            break;
            
        default:
            break;
    }
    cnt++;
}

/*******************************************************************************
 *          DRIVER FUNCTIONS
 ******************************************************************************/
void D_PWM_Init(void) {
    // Clear variables
    PWM_Red.duty_cnt = 0;
    PWM_Red.duty_val = 0xFF;
    
    PWM_Green.duty_cnt = 0;
    PWM_Green.duty_val = 0xFF;
    
    PWM_Blue.duty_cnt = 0;
    PWM_Blue.duty_val = 0xFF;
    
    scale = 0;
    state = Color;
    
    // Timer 0
    D_TIMER0_Init(0);
    D_TIMER0_Enable(false);
    
    // Ports
    R_PORT_Dir = 0;
    G_PORT_Dir = 0;
    B_PORT_Dir = 0;
}
    
void D_PWM_Enable(bool enable) {
    D_TIMER0_Enable(enable);
}
    
void D_PWM_SetDuty(uint8_t which, uint8_t duty) {
    switch(which) {
        case PWM_R:
            PWM_Red.duty_val = duty;
            break;
            
        case PWM_G:
            PWM_Green.duty_val = duty;
            break;
            
        case PWM_B:
            PWM_Blue.duty_val = duty;
            break;
    }
}

void D_PWM_SetRGB(uint8_t r, uint8_t g, uint8_t b) {
    setRGB(r, g, b);
    state = Color;
}

uint8_t D_PWM_GetRed(void) {
    return PWM_Red.duty_cnt;
}

uint8_t D_PWM_GetGreen(void) {
    return PWM_Green.duty_cnt;    
}
    
uint8_t D_PWM_GetBlue(void) {
    return PWM_Blue.duty_cnt;  
}

void D_PWM_ScaleDown(void) {
    if (scale < 7) {
        scale++;
    }
}
    
void D_PWM_ScaleUp(void) {
    if (scale > 0) {
        scale--;
    }
}

uint8_t D_PWM_GetScale(void) {
    return scale;
}

uint8_t D_PWM_GetState(void) {
    return state;
}

void D_PWM_Flash(void) {
    state = Flash;
}
    
void D_PWM_Strobe(void) {
    state = Strobe;
}
    
void D_PWM_Fade(void) {
    state = Fade;
}
    
void D_PWM_Smooth(void) {
    state = Smooth;
}

/*******************************************************************************
 *          INTERRUPTS
 ******************************************************************************/
void interrupt high_priority HighISR(void) {
    if (INTCONbits.TMR0IF) {
        TMR0L = 0;
        TMR0H = 0;
        INTCONbits.TMR0IF = 0;
        handleState();
    }
}

