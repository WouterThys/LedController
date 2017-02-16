import serial
import time

from Errors import SerialReadException, SerialBufferOverflowException
from Settings import read_settings, UART_SETTINGS

pMESSAGE = dict([("message", "[M]"), ("register", "[R]"), ("ack", "[A]"), ("block", "[B]")])
pCOMMAND = dict([("Initialize", "IN"), ("R", "R"), ("G", "G"), ("B", "B")])

start_char = '&'
stop_char = '$'


def serial_ports():
    import sys
    import glob
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except:
            pass
    return result


class SerialInterface:
    def __init__(self):
        self.ser = None
        self.start_char = '&'
        self.stop_char = '$'
        self.ack_id = 0
        self.write_buffer = []
        self.can_write = True

    def serial_configure(self):
        uart_settings = read_settings(UART_SETTINGS)

        try:
            if (self.ser is not None) and (self.ser.isOpen()):
                self.ser.close()
            self.ser = serial.Serial(
                port=uart_settings["com_port"],
                baudrate=uart_settings["baud_rate"],
                parity=uart_settings["parity"],
                stopbits=uart_settings["stop_bits"],
                bytesize=uart_settings["data_bits"]
            )
            print self.ser
        finally:
            # Catching errors should go elsewhere
            pass

    def serial_has_input(self):
        try:
            return self.ser.inWaiting()
        finally:
            pass

    def serial_clear(self):
        if self.ser.isOpen():
            try:
                self.ser.flushInput()
                self.ser.flushOutput()
            finally:
                pass

    def serial_destroy(self):
        self.serial_clear()
        try:
            self.ser.close()
        finally:
            self.ser = None

    def serial_read(self):
        if self.ser.isOpen():
            try:
                out = ""
                c = ''
                cnt = 0
                while c != '$':
                    c = self.ser.read(1)
                    if not c:
                        return ""
                    out += c
                    cnt += 1
                    if cnt > 500:  # Takes way to long before stop character came
                        return ""
                return str(out)
            except Exception as e:
                print e.message
        else:
            print "Serial port is not open"

    def dry_write(self, message):
        try:
            self.ser.write(message + '\r\n')
            print "Output: " + message
        finally:
            pass

    def serial_write_message_block(self, command, message, count, ack_id):
        if self.ser.isOpen():
            if len(self.write_buffer) > 9:
                self.serial_reset_buffer() # TODO: Throw
                print "Serial buffer was full, emptied it"
            self.ack_id = ack_id
            if self.ack_id >= 9:
                self.ack_id = 0
            txt = self.construct_block("block", command, message, count, self.ack_id)
            self.write_buffer.append(txt)
            if self.can_write:
                self.check_write_buffer()
            return self.ack_id
        else:
            print "Serial port is not open"

    def serial_reset_buffer(self):
        for msg in self.write_buffer:
            self.write_buffer.remove(msg)
        self.can_write = True

    def serial_write_message(self, command, message, ack_id):
        if self.ser.isOpen:
            if len(self.write_buffer) > 9:
                return -1  # TODO: throw
            self.ack_id = ack_id
            if self.ack_id > 9:
                self.ack_id = 0
            txt = self.construct_message("message", command, message, self.ack_id)
            self.write_buffer.append(txt)
            if self.can_write:
                self.check_write_buffer()
            return self.ack_id
        else:
            print "Serial port is not open"

    def check_write_buffer(self):
        if len(self.write_buffer) > 0:
            self.can_write = False
            self.dry_write(self.write_buffer[0])
        else:
            return -1

    def acknowledge_message(self, ack_id):
        for msg in self.write_buffer:
            if int(msg[-2]) == int(ack_id):
                self.write_buffer.remove(msg)
                self.can_write = True
                self.check_write_buffer()

    def construct_message(self, type, command, message, ack_id):
        send_txt = ""
        if pMESSAGE.__contains__(type):
            if ack_id > 9:
                ack_id = 0
            self.ack_id = ack_id
            send_txt = start_char + pMESSAGE.get(
                type) + ":" + "c" + ":"+ str(1) +":" + command + ":" + str(message) + ":" + str(ack_id) + stop_char
        return send_txt

    def construct_block(self, type, command, message, length, ack_id):
        send_txt = ""
        if pMESSAGE.__contains__(type):
            if ack_id > 9:
                ack_id = 0
            self.ack_id = ack_id
            send_txt = start_char + pMESSAGE.get(type) + ":" + "c" + ":" + str(length) + ":"

            cnt = 0
            for c in command:
                send_txt += c + ":" + str(message[cnt]) + ":"
                cnt += 1

            send_txt = send_txt + str(ack_id) + stop_char
        return send_txt

    def convert(self, input_msg):

        msg = Message()

        # Typecast and check
        input_msg = str(input_msg)
        if not input_msg:
            return -1

        if input_msg[0] != self.start_char:
            return -1
        if input_msg[-1] != self.stop_char:
            return -1

        # Remove start character
        input_msg = input_msg[1:-1]

        # Check message type
        try:
            t = input_msg[0:3]
            if t == pMESSAGE.get("message"):
                input_msg = input_msg[3:]
                m = input_msg.split(":")
                msg.type = "message"
                msg.sender = m[0]
                msg.command = m[1]
                msg.message = m[2]
                msg.message_time = time.time()
                return msg
            elif t == pMESSAGE.get("ack"):
                input_msg = input_msg[3:]
                msg.message = input_msg
                msg.message_time = time.time()
                msg.type = "ack"
                return msg
        except IOError:
            return -1


class Message:
    def __init__(self):
        self.message = ""
        self.command = ""
        self.sender = ""
        self.type = ""
        self.message_time = time.time()
