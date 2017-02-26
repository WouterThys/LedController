import time
from threading import Event, Thread

from Serial.SerialExeptions import SerialReadThreadException


class ReadThread(Thread):
    def __init__(self, event, queue, serial_interface, read_interval=0.1):
        Thread.__init__(self)
        self.serial_interface = serial_interface
        self.event = event
        self.queue = queue
        self.read_interval = read_interval

    def run(self):
        while not self.event.is_set():
            start_time = time.time()

            try:
                if self.serial_interface.has_input() > 0:
                    msg = self.serial_interface.serial_read()
                    self.queue.put(msg)
                    print "Input: " + msg  # TODO: Logs
            except Exception as e:
                self.serial_interface.enable_read_thread(False)
                #raise SerialReadThreadException("Exception in thread: " + e.message)

            time_delta = time.time() - start_time
            if time_delta < self.read_interval:
                time.sleep(self.read_interval - time_delta)