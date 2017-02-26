from Tkinter import *

from GuiShapes.SupaCanvas import SupaCanvas
from GuiShapes.SupaCircle import MyCircle


class OnOffPanel(Frame):
    def __init__(self, master,
                 on_btn_click=None,
                 off_btn_click=None,
                 *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        # Panel settings
        self.config(borderwidth=0, relief=FLAT)

        # Components
        self.canvas = SupaCanvas(self, height=90, width=180, bd=0, bg="White")
        self.canvas.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.canvas.create_rounded(0, 0, 180, 90, 50, color="DarkGray")

        circle_off = MyCircle(45, 45, 35, text="OFF")
        circle_on = MyCircle(135, 45, 35, text="ON")

        circle_on.draw(self.canvas, fill="Red", activefill="FireBrick", left_btn_click=on_btn_click)
        circle_off.draw(self.canvas, fill="Black", activefill="SlateGray", left_btn_click=off_btn_click)