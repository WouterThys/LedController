#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <xc.h>
#include <string.h>

#include "PORT_Driver.h"
#include "UART_Driver.h"

/*******************************************************************************
 *          DEFINES
 ******************************************************************************/
#define _XTAL_FREQ 48000000
// &
#define START_CHAR 0x26 
// $
#define STOP_CHAR  0x24 
// :
#define SEP_CHAR   0x3A 

#define READ_STATE_START   0x00
#define READ_STATE_TYPE    0x01
#define READ_STATE_SENDER  0x02
#define READ_STATE_BLOCK   0x03
#define READ_STATE_COMMAND 0x04
#define READ_STATE_MESSAGE 0x05
#define READ_STATE_END     0x06

/*******************************************************************************
 *          MACRO FUNCTIONS
 ******************************************************************************/

/*******************************************************************************
 *          VARIABLES
 ******************************************************************************/
uint8_t baud;

const char* startCharacter =       "&";
const char* stopCharacter =        "$";
const char* deviceName;
const char* messageCharacter =     "[M]";
const char* blockCharacter =       "[B]";
const char* ackCharacter =         "[A]";

typedef struct {
    uint8_t command[5];  // Command buffer
    uint8_t commandCnt;   // Count of the command buffer
    uint8_t message[10];  // Message buffer
    uint8_t messageCnt;   // Count of the message buffer
}READ_ComMes;

typedef struct {
    uint8_t type[2];     // Type of the message buffer  
    uint8_t typeCnt;      // Count of the type buffer
    uint8_t blockLength;  // One block = <Command>:<Message>:
    
    uint8_t sender[5];   // Sender name buffer
    uint8_t senderCnt;    // Count of the sender buffer
    
//    uint8_t command[50];  // Command buffer
//    uint8_t commandCnt;   // Count of the command buffer
//    uint8_t message[50];  // Message buffer
//    uint8_t messageCnt;   // Count of the message buffer
    
    READ_ComMes comMes[3];   // Array with commands and messages
    
    uint8_t readId;       // Id send from the sender, to acknowledge
    uint8_t state;    // State of the read buffer
} READ_Buffer;
READ_Buffer readBuffer;

READ_Data readData;

bool D_UART_ReadFlag;

/*******************************************************************************
 *          BASIC FUNCTIONS
 ******************************************************************************/
void writeByte(uint8_t data);
uint8_t readByte(void);
void fillDataBuffer(uint8_t data);
void acknowledge();

void writeByte(uint8_t data) {
    D_UART_Enable(true);
    while(TXSTAbits.TRMT == 0); // Wait while buffer is still full
    TXREG = data;
}

uint8_t readByte() {
    if(RCSTAbits.FERR == 1) {
        uint8_t dum = RCREG;
        return 0;
    } 
    if(RCSTAbits.OERR == 1) {
        D_UART_Enable(false);
        __delay_us(10);
        D_UART_Enable(true);
        return 0;
    } 
    return RCREG;
}

READ_ComMes comMes;
uint8_t bufferCnt = 0;
uint8_t blockLength = 0;
void fillDataBuffer(uint8_t data){
    switch(readBuffer.state) {
        case READ_STATE_START:
            if(data == START_CHAR) {
                readBuffer.typeCnt = 0;
                readBuffer.blockLength = 0;
                blockLength = 0;
                readBuffer.senderCnt = 0;
                bufferCnt = 0;
                comMes.commandCnt = 0;
                comMes.messageCnt = 0;
                D_UART_ReadFlag = false;
                readBuffer.state = READ_STATE_TYPE;
            } else {
                readBuffer.state = READ_STATE_START;
                return;
            }
            break;
        
        case READ_STATE_TYPE:
            if (data == SEP_CHAR) {
                readBuffer.state = READ_STATE_SENDER;
                readBuffer.type[readBuffer.typeCnt] = '\0';
            } else {
                readBuffer.type[readBuffer.typeCnt] = data;
                readBuffer.typeCnt++;
                if(readBuffer.typeCnt > 10) {
                    readBuffer.typeCnt = 0;
                }
            }
            break;
            
        case READ_STATE_SENDER:
            if (data == SEP_CHAR) {
                readBuffer.state = READ_STATE_BLOCK;
                readBuffer.sender[readBuffer.senderCnt] = '\0';
            } else {
                readBuffer.sender[readBuffer.senderCnt] = data;
                readBuffer.senderCnt++;
                if(readBuffer.senderCnt > 50) {
                    readBuffer.senderCnt = 0;
                }
            }
            break;
            
        case READ_STATE_BLOCK:
            if (data == SEP_CHAR) {
                readBuffer.state = READ_STATE_COMMAND;
                readBuffer.sender[readBuffer.senderCnt] = '\0';
            } else {
                readBuffer.blockLength = (data - 0x30);
                blockLength = (data - 0x30);
            }
            break;
            
        case READ_STATE_COMMAND:
            if (data == SEP_CHAR) {
                readBuffer.state = READ_STATE_MESSAGE;
                comMes.command[comMes.commandCnt] = '\0';
            } else {
                comMes.command[comMes.commandCnt] = data;
                comMes.commandCnt++;
                if(comMes.commandCnt > 50) {
                    comMes.commandCnt = 0;
                }
            }
            break;
            
        case READ_STATE_MESSAGE:
            if (data == SEP_CHAR) {
                comMes.message[comMes.messageCnt] = '\0';
                readBuffer.comMes[bufferCnt] = comMes;
                uint8_t i = 0;
                for (i=0; i < comMes.commandCnt; i++) {
                    comMes.command[i] = 0;
                }
                for (i=0; i < comMes.messageCnt; i++) {
                    comMes.message[i] = 0;
                }
                comMes.commandCnt = 0;
                comMes.messageCnt = 0;
                blockLength--;
                bufferCnt++;
                if (blockLength == 0) {
                    readBuffer.state = READ_STATE_END;
                } else {
                    readBuffer.state = READ_STATE_COMMAND;
                }
            } else {
                comMes.message[comMes.messageCnt] = data;
                comMes.messageCnt++;
                if(comMes.messageCnt > 50) {
                    comMes.messageCnt = 0;
                }
            }
            break;
            
        case READ_STATE_END:
            if (data == STOP_CHAR) {
                acknowledge();
                readBuffer.state = READ_STATE_START;
                D_UART_ReadFlag = true;
            } else {
                readBuffer.readId = (data - 0x30);
            }
            break;
            
        default: 
            readBuffer.state = READ_STATE_START;
            break;
    }
}

void acknowledge() {
    printf(startCharacter);
    
    printf(ackCharacter);
    // id
    printf("%x",readBuffer.readId);
    
    printf(stopCharacter);
}

/*******************************************************************************
 *          DRIVER FUNCTIONS
 ******************************************************************************/
void D_UART_Init(const char* name, uint16_t baud, bool interrupts) {
    // Port settings
    UART_TX_Dir = 0;
    UART_RX_Dir = 1;
    
    // Clear/set variables
    deviceName = name;
    D_UART_ReadFlag = false;
    
    // Disable UART while initializing
    D_UART_Enable(false);
    
    // TXSTA register settings
    TXSTAbits.TX9 = 0; // Selects 8-bit transmission
    TXSTAbits.SYNC = 0; // Synchronous mode
    TXSTAbits.BRGH = 0; // Low speed
    
    // RCSTA register settings
    RCSTAbits.RX9 = 0; // Selects 8-bit reception

    // BAUDCON register settings
    BAUDCONbits.RXDTP = 0; // RX data is inverted
    BAUDCONbits.TXCKP = 0; // TX data is inverted
    BAUDCONbits.BRG16 = 0; // 8-bit Baud Rate Generator

    SPBRG = ((_XTAL_FREQ/baud)/64)-1; // Baud rate selection
    
    // Interrupts for reading
    if (interrupts) {
        RCONbits.IPEN = 1;   // Enable priority levels on interrupts
        INTCONbits.GIEH = 1; // Enable high interrupt
        INTCONbits.GIEL = 1; // Enable low interrupt
        PIR1bits.RCIF = 0; // Clear flag
        IPR1bits.RCIP = 0; // Low priority
        PIE1bits.RCIE = 1; // Enable UART interrupt
    }
}

void D_UART_Write(const char* command, const char* data) {
    printf(startCharacter);
    
    printf(messageCharacter);
    printf(deviceName);
    // Command
    printf(":");printf(command);
    // Message
    printf(":");printf(data);
    
    printf(stopCharacter);
    __delay_ms(1);
}

void D_UART_WriteInt(const char* command, int data) {
    printf(startCharacter);
    
    printf(messageCharacter);
    printf(deviceName);
    // Command
    printf(":");printf(command);
    // Message
    printf(":");printf("%d",data);
    
    printf(stopCharacter);
    __delay_ms(1);
}

READ_Data D_UART_Read(){
    READ_ComMes cm = readBuffer.comMes[0];
    readData.sender = readBuffer.sender;
    readData.command = cm.command;
    readData.message = cm.message;
    return readData;
}

READ_Data D_UART_ReadBlock(uint8_t cnt) {
    READ_ComMes cm = readBuffer.comMes[cnt];
    readData.sender = readBuffer.sender;
    readData.command = cm.command;
    readData.message = cm.message;
    return readData;
}

uint8_t D_UART_BlockLength() {
    return readBuffer.blockLength;
}

void D_UART_Enable(bool enable) {
    if(enable) {
        UART_TX_Dir = 0;
        UART_RX_Dir = 1;
        TXSTAbits.TXEN = 1; // Activate TX
        RCSTAbits.CREN = 1; // Activate RX
        RCSTAbits.SPEN = 1; // Enable UART
    } else {
        UART_TX_Dir = 0;
        UART_RX_Dir = 0;
        TXSTAbits.TXEN = 0; // Deactivate TX
        RCSTAbits.CREN = 0; // Deactivate RX
        RCSTAbits.SPEN = 0; // Enable UART
    }
}

//void D_UART_Acknowledge(uint16_t val) {
//    printf(startCharacter);
//    
//    printf(ackCharacter);
//    // id
//    printf("%x",readBuffer.readId);
//    
//    if (val != NULL) {
//        printf(":%d", val);
//    }
//    
//    printf(stopCharacter);
//}

const char* D_UART_GetDeviceName() {
    return deviceName;
}

void putch(char data) {
    writeByte(data); // Write the data
}


/*******************************************************************************
 *          INTERRUPTS
 ******************************************************************************/
void interrupt low_priority LowISR(void) {
    if (PIR1bits.RC1IF) {
        fillDataBuffer(readByte());
        PIR1bits.RC1IF = 0;
    }
}