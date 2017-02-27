import serial
import time
from Queue import Queue
from threading import Event

from Serial.SerialExeptions import SerialReadException, SerialPortNotOpenException, SerialInitialisationException, \
    SerialWriteException, SerialMessageConversionException, SerialAcknowledgeException
from Serial.SerialThreads import ReadThread
from Settings import read_settings, UART_SETTINGS

pMESSAGE = dict([("message", "[M]"), ("register", "[R]"), ("ack", "[A]"), ("block", "[B]")])
pCOMMAND = dict([("Initialize", "IN"), ("R", "R"), ("G", "G"), ("B", "B")])

START_CHAR = '&'
STOP_CHAR = '$'

READ_BUFFER_CHAR_LENGTH = 500


class SerialInterface:
    def __init__(self):
        self.my_serial = None
        self.ack_id = 0
        self.write_buffer = []
        self.can_write = True

        self.read_queue = Queue()
        self.read_event = Event()
        self.reading_thread = None

    def serial_configure(self):
        serial_settings = read_settings(UART_SETTINGS)

        try:
            if (self.my_serial is not None) and (self.my_serial.isOpen()):
                self.my_serial.close()
            self.my_serial = serial.Serial(
                port=serial_settings["com_port"],
                baudrate=serial_settings["baud_rate"],
                parity=serial_settings["parity"],
                stopbits=serial_settings["stop_bits"],
                bytesize=serial_settings["data_bits"]
            )
            self.serial_clear()
        except Exception as e:
            print e.strerror
            raise SerialInitialisationException("Error initialising serial interface", e.strerror)

    def enable_read_thread(self, enable):
        if enable:
            if (self.my_serial is not None) and self.my_serial.isOpen:
                self.reading_thread = None
                self.read_event.clear()
                self.reading_thread = ReadThread(self.read_event, self.read_queue, self)
                self.reading_thread.setDaemon(True)
                self.reading_thread.start()
                print "Read thread started"
            else:
                print "Read thread not started because serial is not open"
        else:
            try:
                self.read_event.set()
                self.reading_thread.join(5)
                with self.read_queue.mutex:
                    self.read_queue.queue.clear()
                self.my_serial.serial_clear()
            except RuntimeError as e:
                print e.message
            print "Read thread stopped"

    def has_input(self):
        try:
            return self.my_serial.inWaiting()
        finally:
            pass

    def serial_clear(self):
        if (self.my_serial is not None) and self.my_serial.isOpen:
            try:
                self.my_serial.flushInput()
                self.my_serial.flushOutput()
            finally:
                pass

    def serial_destroy(self):
        self.serial_clear()
        self.enable_read_thread(False)
        try:
            self.my_serial.close()
        finally:
            self.my_serial = None

    def serial_read(self):
        if (self.my_serial is not None) and self.my_serial.isOpen:
            out = ""
            c = ''
            cnt = 0
            while c != '$':
                try:
                    c = self.my_serial.read(1)
                except serial.SerialException as e:
                    raise SerialReadException("Error reading input characters", e.message)

                if not c:
                    raise SerialReadException("Error reading input characters",
                                              "Read buffer exceeded 'READ_BUFFER_CHAR_LENGTH' characters")
                out += c
                cnt += 1
                if cnt > READ_BUFFER_CHAR_LENGTH:  # Takes way to long before stop character came
                    raise SerialReadException("Error reading input characters",
                                              "Read buffer exceeded 'READ_BUFFER_CHAR_LENGTH' characters")
            return str(out)
        else:
            raise SerialPortNotOpenException("Serial port not open")

    def dry_write(self, message):
        try:
            self.my_serial.write(message + '\r\n')
            print "Output: " + message
        except serial.SerialTimeoutException as e:
            SerialWriteException("Error writing to output: TIMEOUT", e.message)
        except serial.SerialException as e:
            SerialWriteException("Error writing to output", e.message)

    def serial_write_message_block(self, command, message, count, ack_id):
        if (self.my_serial is not None) and self.my_serial.isOpen:
            if len(self.write_buffer) > 9:
                self.serial_reset_buffer()  # TODO: Throw
                print "Serial buffer was full, emptied it"
            self.ack_id = ack_id
            if self.ack_id > 9:
                self.ack_id = 0
            txt = self.construct_block("block", command, message, count, self.ack_id)
            self.write_buffer.append(txt)
            if self.can_write:
                self.check_write_buffer()
            return self.ack_id
        else:
            raise SerialPortNotOpenException("Serial port not open")

    def serial_reset_buffer(self):
        for msg in self.write_buffer:
            self.write_buffer.remove(msg)
        self.can_write = True

    def serial_write_message(self, command, message, ack_id):
        if (self.my_serial is not None) and self.my_serial.isOpen:
            if len(self.write_buffer) > 9:
                return -1  # TODO: throw
            if ack_id >= 0:
                self.ack_id = ack_id
            if self.ack_id > 9:
                self.ack_id = ack_id = 0
            txt = self.construct_message("message", command, message, ack_id)
            if ack_id >= 0:
                self.write_buffer.append(txt)
                if self.can_write:
                    self.check_write_buffer()
                return self.ack_id
            else:
                self.dry_write(txt)
        else:
            raise SerialPortNotOpenException("Serial port not open")

    def check_write_buffer(self):
        if len(self.write_buffer) > 0:
            self.can_write = False
            self.dry_write(self.write_buffer[0])
        else:
            return -1

    def acknowledge_message(self, ack_id):
        found_ack_id = False
        for msg in self.write_buffer:
            if int(msg[-2]) == int(ack_id):
                self.write_buffer.remove(msg)
                self.can_write = True
                found_ack_id = True
                self.check_write_buffer()
                break

        if not found_ack_id:
            raise SerialAcknowledgeException("Invalid acknowledge ID")

    def construct_message(self, type, command, message, ack_id):
        send_txt = ""
        if pMESSAGE.__contains__(type):
            if ack_id > 9:
                ack_id = 0
            if ack_id < 0:
                ack_id = 0
            self.ack_id = ack_id
            send_txt = START_CHAR + pMESSAGE.get(
                type) + ":" + "c" + ":" + str(1) + ":" + command + ":" + str(message) + ":" + str(ack_id) + STOP_CHAR
        return send_txt

    def construct_block(self, type, command, message, length, ack_id):
        send_txt = ""
        if pMESSAGE.__contains__(type):
            if ack_id > 9:
                ack_id = 0
            self.ack_id = ack_id
            send_txt = START_CHAR + pMESSAGE.get(type) + ":" + "c" + ":" + str(length) + ":"

            cnt = 0
            for c in command:
                send_txt += c + ":" + str(message[cnt]) + ":"
                cnt += 1

            send_txt = send_txt + str(ack_id) + STOP_CHAR
        return send_txt


def convert_input_message(input_msg):
    msg = Message()
    # Typecast and check
    input_msg = str(input_msg)
    if not input_msg:
        SerialMessageConversionException("Error converting message.", "Input message is empty.")
    if input_msg[0] != START_CHAR:
        SerialMessageConversionException("Error converting message.", "Start character different from %s." % START_CHAR)
    if input_msg[-1] != STOP_CHAR:
        SerialMessageConversionException("Error converting message.", "Stop character different from %s." % STOP_CHAR)
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
    except IOError as e:
        SerialMessageConversionException("Error converting message.", e.message)


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


class Message:
    def __init__(self):
        self.message = ""
        self.command = ""
        self.sender = ""
        self.type = ""
        self.message_time = time.time()
