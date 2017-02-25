from Tkinter import *

from GuiShapes.SupaCanvas import SupaCanvas
from GuiShapes.SupaCircle import MyCircle


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def to_rgb(rgb):
    return "#%02x%02x%02x" % rgb


class ColorPanel(Frame):
    def __init__(self, master,
                 btn_click=None,
                 on_flash_btn_click=None,
                 on_strobe_btn_click=None,
                 on_fade_btn_click=None,
                 on_smooth_btn_click=None,
                 *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        # Panel settings
        self.config(borderwidth=0, relief=FLAT)

        # Components
        self.canvas = SupaCanvas(self, height=450, width=360, bd=0, bg="White")
        self.canvas.grid(row=0, column=0, columnspan=4, sticky='nsew')

        self.canvas.create_rounded(0, 0, 360, 90, 50, color="DarkGray")  # Upper gray background
        self.canvas.create_rounded(0, 0, 300, 180, 50, color="DarkGray")  # Upper gray background
        self.canvas.create_rounded(0, 0, 90, 450, 50, color="DarkGray")  #
        self.canvas.create_rounded(90, 0, 180, 450, 50, color="DarkGray")  #
        self.canvas.create_rounded(180, 0, 270, 450, 50, color="DarkGray")  #
        self.canvas.create_rounded(0, 360, 270, 450, 50, color="DarkGray")  #
        self.canvas.create_rounded(270, 90, 360, 450, 50, color="White")  # White right side strip

        # Circles
        circle_r = MyCircle(45, 45, 35, text='R')
        circle_g = MyCircle(135, 45, 35, text='G')
        circle_b = MyCircle(225, 45, 35, text='B')
        circle_w = MyCircle(315, 45, 35, text='W')

        circle_11 = MyCircle(45, 135, 35)
        circle_12 = MyCircle(135, 135, 35)
        circle_13 = MyCircle(225, 135, 35)

        circle_21 = MyCircle(45, 225, 35)
        circle_22 = MyCircle(135, 225, 35)
        circle_23 = MyCircle(225, 225, 35)

        circle_31 = MyCircle(45, 315, 35)
        circle_32 = MyCircle(135, 315, 35)
        circle_33 = MyCircle(225, 315, 35)

        circle_41 = MyCircle(45, 405, 35)
        circle_42 = MyCircle(135, 405, 35)
        circle_43 = MyCircle(225, 405, 35)

        circle_fl = MyCircle(315, 135, 35, text="FLASH")
        circle_st = MyCircle(315, 225, 35, text="STROBE")
        circle_fa = MyCircle(315, 315, 35, text="FADE")
        circle_sm = MyCircle(315, 405, 35, text="SMOOTH")

        circle_r.draw(self.canvas, fill=to_rgb((255, 0, 0)), activefill=to_rgb((245, 10, 10)), btn_click=btn_click)
        circle_g.draw(self.canvas, fill=to_rgb((0, 255, 0)), activefill=to_rgb((10, 245, 10)), btn_click=btn_click)
        circle_b.draw(self.canvas, fill=to_rgb((0, 0, 255)), activefill=to_rgb((10, 10, 245)), btn_click=btn_click)
        circle_w.draw(self.canvas, fill=to_rgb((255, 255, 255)), activefill=to_rgb((245, 245, 245)), btn_click=btn_click, textcolor="black")

        circle_11.draw(self.canvas, fill=to_rgb((255, 127, 0)), activefill=to_rgb((245, 117, 0)), btn_click=btn_click)
        circle_12.draw(self.canvas, fill=to_rgb((107, 214, 119)), activefill=to_rgb((97 , 204, 119)), btn_click=btn_click)
        circle_13.draw(self.canvas, fill=to_rgb((10, 42, 255)), activefill=to_rgb((0, 32, 245)), btn_click=btn_click)
        circle_21.draw(self.canvas, fill=to_rgb((255, 160, 0)), activefill=to_rgb((245, 150, 0)), btn_click=btn_click)
        circle_22.draw(self.canvas, fill=to_rgb((110, 220, 220)), activefill=to_rgb((100, 210, 210)), btn_click=btn_click)
        circle_23.draw(self.canvas, fill=to_rgb((129, 11, 147)), activefill=to_rgb((119, 1, 137)), btn_click=btn_click)
        circle_31.draw(self.canvas, fill=to_rgb((255, 200, 0)), activefill=to_rgb((245, 190, 0)), btn_click=btn_click)
        circle_32.draw(self.canvas, fill=to_rgb((46, 204, 201)), activefill=to_rgb((36, 194, 191)), btn_click=btn_click)
        circle_33.draw(self.canvas, fill=to_rgb((255, 0, 0)), activefill=to_rgb((0, 255, 0)), btn_click=btn_click)
        circle_41.draw(self.canvas, fill=to_rgb((255, 233, 0)), activefill=to_rgb((245, 223, 0)), btn_click=btn_click)
        circle_42.draw(self.canvas, fill=to_rgb((28, 127, 142)), activefill=to_rgb((18, 127, 132)), btn_click=btn_click)
        circle_43.draw(self.canvas, fill=to_rgb((0, 0, 0)), activefill=to_rgb((10, 10, 10)), btn_click=btn_click)

        circle_fl.draw(self.canvas, fill="DimGray", activefill="DarkGray", btn_click=on_flash_btn_click)
        circle_st.draw(self.canvas, fill="DimGray", activefill="DarkGray", btn_click=on_strobe_btn_click)
        circle_fa.draw(self.canvas, fill="DimGray", activefill="DarkGray", btn_click=on_fade_btn_click)
        circle_sm.draw(self.canvas, fill="DimGray", activefill="DarkGray", btn_click=on_smooth_btn_click)

    def get_rgb_from_click(self, event):
        cur = self.canvas.find_withtag(CURRENT)
        cur_val = cur[0]

        if cur_val % 2 != 0:
            return hex_to_rgb(self.canvas.itemcget(cur, "fill"))
        else:
            return hex_to_rgb(self.canvas.itemcget((cur_val-1), "fill"))

