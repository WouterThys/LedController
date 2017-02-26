import tkMessageBox
import tkSimpleDialog
import ttk
from Tkinter import *
from serial import Serial

from Serial.SerialInterface import serial_ports
from Settings import read_settings, UART_SETTINGS, write_settings


class SerialSettingsDialog(tkSimpleDialog.Dialog):
    def __init__(self, master):
        self.settings_dict = read_settings(UART_SETTINGS)
        tkSimpleDialog.Dialog.__init__(self, master, "Serial settings")

    def body(self, master):
        Label(master, text="Com port").grid(row=0, sticky=W)
        Label(master, text="Baud rate").grid(row=1, sticky=W)
        Label(master, text="Data bits").grid(row=2, sticky=W)
        Label(master, text="Stop bits").grid(row=3, sticky=W)
        Label(master, text="Parity").grid(row=4, sticky=W)

        port_txt = StringVar()
        baud_txt = StringVar()
        bits_txt = StringVar()
        stop_txt = StringVar()
        pari_txt = StringVar()

        self.port_cb = ttk.Combobox(master, values=serial_ports(), textvariable=port_txt)
        self.baud_cb = ttk.Combobox(master, values=Serial.BAUDRATES, textvariable=baud_txt)
        self.bits_cb = ttk.Combobox(master, values=Serial.BYTESIZES, textvariable=bits_txt)
        self.stop_cb = ttk.Combobox(master, values=Serial.STOPBITS, textvariable=stop_txt)
        self.pari_cb = ttk.Combobox(master, values=Serial.PARITIES, textvariable=pari_txt)

        port = self.settings_dict["com_port"]
        baud = self.settings_dict["baud_rate"]
        data = self.settings_dict["data_bits"]
        stop = self.settings_dict["stop_bits"]
        pari = self.settings_dict["parity"]

        try:
            self.port_cb.current(serial_ports().index(port))
        except Exception as e:
            print e.message

        try:
            self.baud_cb.current(Serial.BAUDRATES.index(baud))
        except Exception as e:
            print e.message

        try:
            self.bits_cb.current(Serial.BYTESIZES.index(data))
        except Exception as e:
            print e.message

        try:
            self.stop_cb.current(Serial.STOPBITS.index(stop))
        except Exception as e:
            print e.message

        try:
            self.pari_cb.current(Serial.PARITIES.index(pari))
        except Exception as e:
            print e.message

        self.port_cb.grid(row=0, column=1)
        self.baud_cb.grid(row=1, column=1)
        self.bits_cb.grid(row=2, column=1)
        self.stop_cb.grid(row=3, column=1)
        self.pari_cb.grid(row=4, column=1)

        return self.port_cb  # Initial focus

    def validate(self):
        try:
            self.settings_dict['parity'] = str(self.pari_cb.get())
            self.settings_dict['baudrate'] = int(self.baud_cb.get())
            self.settings_dict['bytesize'] = int(self.bits_cb.get())
            self.settings_dict['stopbits'] = int(self.stop_cb.get())
            return 1
        except Exception as e:
            tkMessageBox.showerror(
                "Bad input",
                "Illegal values, please try again: "+e.message
            )
            return 0

    def apply(self):
        yaml_dict = read_settings(UART_SETTINGS)
        yaml_dict['parity'] = str(self.pari_cb.get())
        yaml_dict['baud_rate'] = int(self.baud_cb.get())
        yaml_dict['data_bits'] = int(self.bits_cb.get())
        yaml_dict['stop_bits'] = int(self.stop_cb.get())
        yaml_dict['com_port'] = str(self.port_cb.get())
        write_settings(UART_SETTINGS, yaml_dict)