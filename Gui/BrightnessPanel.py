from Tkinter import *

from SupaCanvas import SupaCanvas
from SupaCircle import MyCircle


class BrightnessPanel(Frame):
    def __init__(self, master,
                 br_on_btn_click=None,
                 br_off_btn_click=None,
                 *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        # Panel settings
        self.config(borderwidth=0, relief=FLAT)

        # Components
        self.canvas = SupaCanvas(self, height=90, width=180, bd=0, bg="White")
        self.canvas.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.canvas.create_rounded(0, 0, 180, 90, 50, color="DarkGray")

        circle_br_on = MyCircle(45, 45, 35)
        circle_br_off = MyCircle(135, 45, 35)

        circle_br_on.draw(self.canvas, fill="White", activefill="Gainsboro", btn_click=br_on_btn_click)
        circle_br_off.draw(self.canvas, fill="White", activefill="Gainsboro", btn_click=br_off_btn_click)