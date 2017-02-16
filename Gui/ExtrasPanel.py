from Tkinter import *

from SupaCircle import MyCircle


class ExtrasPanel(Frame):
    def __init__(self, master,
                 flash_btn_click=None,
                 strobe_btn_click=None,
                 fade_btn_click=None,
                 smooth_btn_click=None,
                 *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        # Panel settings
        self.config(relief=FLAT)

        # Components
        self.canvas = Canvas(self, height=370, width=90, bg="White")
        self.canvas.grid(row=1, column=0, columnspan=4, sticky='nsew')

        # Circles
        circle_flash = MyCircle(50, 50, 35, text='Flash')
        circle_strobe = MyCircle(50, 140, 35, text='Strobe')
        circle_fade = MyCircle(50, 230, 35, text='Fade')
        circle_smooth = MyCircle(50, 330, 35, text='Smooth')

        circle_flash.draw(self.canvas, fill="DarkGray", activefill="Gray", btn_click=flash_btn_click)
        circle_strobe.draw(self.canvas, fill="DarkGray", activefill="Gray", btn_click=strobe_btn_click)
        circle_fade.draw(self.canvas, fill="DarkGray", activefill="Gray", btn_click=fade_btn_click)
        circle_smooth.draw(self.canvas, fill="DarkGray", activefill="Gray", btn_click=smooth_btn_click)