import tkMessageBox

from MainScreen import MainScreen
from Serial.SerialExeptions import SerialError
from Serial.SerialInterface import SerialInterface


class Manager:
    def __init__(self, master):
        self.master = master
        self.my_serial = SerialInterface()
        self.my_serial = SerialInterface()

        try:
            self.my_serial.serial_configure()
            self.my_serial.serial_clear()
        except SerialError as e:
            print e.message
            tkMessageBox.showerror("Serial Error", e.message)

        self.my_serial.enable_read_thread(True)
        self.gui = MainScreen(master, self, self.end_application)
        self.periodic_update()

    def periodic_update(self):
        self.gui.gui_update(self.my_serial.read_queue)
        self.master.after(200, self.periodic_update)

    def end_application(self):
        self.master.quit()
        self.my_serial.serial_destroy()