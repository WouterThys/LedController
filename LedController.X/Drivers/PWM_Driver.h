/* Microchip Technology Inc. and its subsidiaries.  You may use this software 
 * and any derivatives exclusively with Microchip products. 
 * 
 * THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS".  NO WARRANTIES, WHETHER 
 * EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED 
 * WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A 
 * PARTICULAR PURPOSE, OR ITS INTERACTION WITH MICROCHIP PRODUCTS, COMBINATION 
 * WITH ANY OTHER PRODUCTS, OR USE IN ANY APPLICATION. 
 *
 * IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE, 
 * INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND 
 * WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS 
 * BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE.  TO THE 
 * FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS 
 * IN ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF 
 * ANY, THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
 *
 * MICROCHIP PROVIDES THIS SOFTWARE CONDITIONALLY UPON YOUR ACCEPTANCE OF THESE 
 * TERMS. 
 */

/* 
 * File:   
 * Author: 
 * Comments:
 * Revision history: 
 */

// This is a guard condition so that contents of this file are not included
// more than once.  
#ifndef XC_HEADER_TEMPLATE_H
#define	XC_HEADER_TEMPLATE_H

#include <xc.h> // include processor files - each processor file is guarded.  
#include <stdbool.h>
#include <stdint.h>

#ifdef	__cplusplus
extern "C" {
#endif /* __cplusplus */
    
#define PWM_R   0
#define PWM_G   1
#define PWM_B   2
    
    typedef struct {
        uint8_t duty_cnt;
        uint8_t duty_val;
    } pwm_t;

    void D_PWM_Init(void);
    
    void D_PWM_Enable(bool enable);
    
    void D_PWM_SetDuty(uint8_t which, uint8_t duty);
    
    void D_PWM_SetRGB(uint8_t r, uint8_t g, uint8_t b);
    
    uint8_t D_PWM_GetRed(void);
    uint8_t D_PWM_GetGreen(void);
    uint8_t D_PWM_GetBlue(void);
    
    void D_PWM_ScaleUp(void);
    
    void D_PWM_ScaleDown(void);
    
    uint8_t D_PWM_GetScale(void);
    
    uint8_t D_PWM_GetState(void);
    
    /**
     * Flashed between R, G, B and W LEDs. Speed can be changed with the 
     * D_PWM_ScaleUp() and D_PWM_ScaleDown()
     */
    void D_PWM_Flash(void);
    
    /**
     * Smoothly going from fully on to fully off. Speed can be changed with the
     * D_PWM_ScaleUp() and D_PWM_ScaleDown()
     */
    void D_PWM_Strobe(void);
    
    void D_PWM_Fade(void);
    
    void D_PWM_Smooth(void);

#ifdef	__cplusplus
}
#endif /* __cplusplus */

#endif	/* XC_HEADER_TEMPLATE_H */

