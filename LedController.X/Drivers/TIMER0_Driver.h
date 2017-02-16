#ifndef TIMER0_DRIVER_H
#define	TIMER0_DRICER_H

#ifdef	__cplusplus
extern "C" {
#endif
    
#include <stdbool.h>
#include <stdint.h>
    
    /**
     */
    bool D_TIMER0_Flag = false;

    /**
     * 
     * @param prescale
     */
    void D_TIMER0_Init(uint8_t prescale);
    
    /**
     * 
     * @param enable
     */
    void D_TIMER0_Enable(bool enable);

#ifdef	__cplusplus
}
#endif

#endif	/* TIMER0_DRIVER */
