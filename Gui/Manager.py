import tkMessageBox
from Queue import Queue
from threading import Event, Thread

import time

from SerialInterface import SerialInterface
from MainScreen import MainScreen


class Manager:
    def __init__(self, master):

        self.master = master

        self.my_serial = SerialInterface()
        try:
            self.my_serial.serial_configure()
            self.my_serial.serial_clear()
        except Exception as e:
            tkMessageBox.showerror("Serial Error", e.strerror)

        self.read_queue = Queue()
        self.read_event = Event()
        self.reading_thread = None
        self.start(True)

        self.gui = MainScreen(master, self, self.end_application)

        self.periodic_update()

    def periodic_update(self):
        #self.check_queue()
        self.gui.gui_update(self.read_queue)
        self.master.after(200, self.periodic_update)

    def start(self, should_start):
        if should_start:
            self.reading_thread = None
            self.read_event.clear()
            self.reading_thread = ReadThread(self.read_event, self.read_queue, self.my_serial)
            self.reading_thread.setDaemon(True)
            self.reading_thread.start()
            print "Read thread started"
        else:
            self.read_event.set()
            self.reading_thread.join(5)
            with self.read_queue.mutex:
                self.read_queue.queue.clear()
            self.my_serial.serial_clear()
            print "Read thread stopped"

    def end_application(self):
        self.master.quit()
        self.read_event.set()
        if self.reading_thread is not None:
            self.reading_thread.join(5)
        self.my_serial.serial_destroy()


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
                if self.serial_interface.serial_has_input() > 0:
                    msg = self.serial_interface.serial_read()
                    self.queue.put(msg)
                    print "Input: "+msg
            except Exception as e:
                print "EXCEPTION IN THREAD: " + e.message
                #self.event.set()

            time_delta = time.time() - start_time
            if time_delta < self.read_interval:
                time.sleep(self.read_interval - time_delta)