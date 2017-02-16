#ifndef UART_DRIVER_H
#define	UART_DRIVER_H

#ifdef	__cplusplus
extern "C" {
#endif
    
#include <stdbool.h>
#include <stdint.h>

/**
 * Uart driver for PIC18F
 * Message format:
 *	<Start Character><Type Character><Device name>:<Command>:<Data>:<Stop Character>
 *	with:
 *	 - Start Character: '&'
 *	 - Type Character: The type of the message, ex: for a message '[M]', for block '[B]'
 *       - Device name: This PIC's device name (const char*)
 *   	 - Command: The command (const char*)
 *   	 - Data: The data (const char*)
 * 	 - Stop Character: '$'
 * 
 * Java example of writing a message to the PIC:
 *      String sendTxt = "";
 *		if (id > 9) id = 0;
 *		sendTxt = startCharacter + messageCharacter + ":" + sender + ":" + command + ":" + message + ":" + String.valueOf(id)+stopCharacter;
 *		return sendTxt;
 * 
 * Block format:
 * 
 * 
 */
    
    
#define MESSAGE_TYPE = 0;
#define BLOCK_TYPE = 1;
/**
 * Boolean indicating data can be read.
 */    
extern bool D_UART_ReadFlag;

/**
 * Data struct for reading data.
 */
typedef struct {
    const char* sender;
    const char* command;
    const char* message;
}READ_Data;
    
/**
* Initializes all the parameters to the default setting, as well as writing the
* tri-state registers. Initializes the UART to the default data rate and settings.
 * @param name The name of the device.
 * @param baud The baud rate.
 * @param interrupts Boolean to set if interrupts should be used.
*/
void D_UART_Init(const char* name, uint16_t baud, bool interrupts);

/**
 * Write data to the TX pin of UART module. 
 * @param command: Command
 * @param data: Data string to write
 */
void D_UART_Write(const char* command, const char* data);

/**
 * Write data to the TX pin of UART module. 
 * @param command: Command
 * @param data: Data integer to write
 */
void D_UART_WriteInt(const char* command, int data);

/**
 * Read data from the RX pin of UART module.
 * @return data: returns the data struct.
 */
READ_Data D_UART_Read();

/**
 * 
 * @return 
 */
READ_Data D_UART_ReadBlock(uint8_t cnt);
uint8_t D_UART_BlockLength();
uint8_t D_UART_MessageType();

void D_UART_Acknowledge(uint16_t val);

/**
 * Enable the UART module
 * @param enable Enable or disable UART.
 */
void D_UART_Enable(bool enable);

/**
 * Get the device name.
 * @return const char* device name
 */
const char* D_UART_GetDeviceName();


#ifdef	__cplusplus
}
#endif

#endif	/* UART_DRIVER */
