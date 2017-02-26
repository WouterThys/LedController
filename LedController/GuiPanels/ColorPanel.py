from Tkinter import *
from ast import literal_eval
from tkColorChooser import askcolor
from random import randint

from GuiPanels.ColorDialog import ColorDialog
from GuiShapes.SupaCanvas import SupaCanvas
from GuiShapes.SupaCircle import MyCircle
from Settings import CIRCLE_PWM_COLORS, read_settings, write_settings


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def to_rgb(rgb):
    try:
        return "#%02x%02x%02x" % rgb
    except TypeError as e:
        print e.message


class ColorPanel(Frame):
    def __init__(self, master,
                 btn_click_left=None,
                 btn_click_right=None,
                 on_flash_btn_click=None,
                 on_strobe_btn_click=None,
                 on_fade_btn_click=None,
                 on_smooth_btn_click=None,
                 on_test_btn_click=None,
                 *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master
        self.on_test_btn_click = on_test_btn_click
        self.cur_val = 0

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

        self.colors_dict = read_settings(CIRCLE_PWM_COLORS)

        circle_r.draw(self.canvas, fill=to_rgb((255, 0, 0)), activefill=to_rgb((245, 10, 10)),
                      left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                      pwm_color=to_rgb(literal_eval(self.colors_dict['circle_r'])), tags='circle_r')
        circle_g.draw(self.canvas, fill=to_rgb((0, 255, 0)), activefill=to_rgb((10, 245, 10)),
                      left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                      pwm_color=to_rgb(literal_eval(self.colors_dict['circle_g'])), tags='circle_g')
        circle_b.draw(self.canvas, fill=to_rgb((0, 0, 255)), activefill=to_rgb((10, 10, 245)),
                      left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                      pwm_color=to_rgb(literal_eval(self.colors_dict['circle_b'])), tags='circle_b')
        circle_w.draw(self.canvas, fill=to_rgb((255, 255, 255)), activefill=to_rgb((245, 245, 245)), textcolor="black",
                      left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                      pwm_color=to_rgb(literal_eval(self.colors_dict['circle_w'])), tags='circle_w')

        circle_11.draw(self.canvas, fill=to_rgb((255, 127, 0)), activefill=to_rgb((245, 117, 0)),
                       left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                       pwm_color=to_rgb(literal_eval(self.colors_dict['circle_11'])), tags='circle_11')
        circle_12.draw(self.canvas, fill=to_rgb((107, 214, 119)), activefill=to_rgb((97, 204, 119)),
                       left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                       pwm_color=to_rgb(literal_eval(self.colors_dict['circle_12'])), tags='circle_12')
        circle_13.draw(self.canvas, fill=to_rgb((10, 42, 255)), activefill=to_rgb((0, 32, 245)),
                       left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                       pwm_color=to_rgb(literal_eval(self.colors_dict['circle_13'])), tags='circle_13')
        circle_21.draw(self.canvas, fill=to_rgb((255, 160, 0)), activefill=to_rgb((245, 150, 0)),
                       left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                       pwm_color=to_rgb(literal_eval(self.colors_dict['circle_21'])), tags='circle_21')
        circle_22.draw(self.canvas, fill=to_rgb((110, 220, 220)), activefill=to_rgb((100, 210, 210)),
                       left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                       pwm_color=to_rgb(literal_eval(self.colors_dict['circle_22'])), tags='circle_22')
        circle_23.draw(self.canvas, fill=to_rgb((25, 0, 51)), activefill=to_rgb((15, 1, 41)),
                       left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                       pwm_color=to_rgb(literal_eval(self.colors_dict['circle_23'])), tags='circle_23')
        circle_31.draw(self.canvas, fill=to_rgb((255, 200, 0)), activefill=to_rgb((245, 190, 0)),
                       left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                       pwm_color=to_rgb(literal_eval(self.colors_dict['circle_31'])), tags='circle_31')
        circle_32.draw(self.canvas, fill=to_rgb((46, 204, 201)), activefill=to_rgb((36, 194, 191)),
                       left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                       pwm_color=to_rgb(literal_eval(self.colors_dict['circle_32'])), tags='circle_32')
        circle_33.draw(self.canvas, fill=to_rgb((129, 11, 147)), activefill=to_rgb((119, 1, 137)),
                       left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                       pwm_color=to_rgb(literal_eval(self.colors_dict['circle_33'])), tags='circle_33')
        circle_41.draw(self.canvas, fill=to_rgb((255, 233, 0)), activefill=to_rgb((245, 223, 0)),
                       left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                       pwm_color=to_rgb(literal_eval(self.colors_dict['circle_41'])), tags='circle_41')
        circle_42.draw(self.canvas, fill=to_rgb((28, 127, 142)), activefill=to_rgb((18, 127, 132)),
                       left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                       pwm_color=to_rgb(literal_eval(self.colors_dict['circle_42'])), tags='circle_42')
        circle_43.draw(self.canvas, fill=to_rgb((255, 0, 0)), activefill=to_rgb((0, 255, 0)),
                       left_btn_click=btn_click_left, right_btn_click=btn_click_right,
                       pwm_color=to_rgb(literal_eval(self.colors_dict['circle_43'])), tags='circle_43')

        circle_fl.draw(self.canvas, fill="DimGray", activefill="DarkGray", left_btn_click=on_flash_btn_click)
        circle_st.draw(self.canvas, fill="DimGray", activefill="DarkGray", left_btn_click=on_strobe_btn_click)
        circle_fa.draw(self.canvas, fill="DimGray", activefill="DarkGray", left_btn_click=on_fade_btn_click)
        circle_sm.draw(self.canvas, fill="DimGray", activefill="DarkGray", left_btn_click=on_smooth_btn_click)

    def get_rgb_from_click(self, event):
        cur = self.canvas.find_withtag(CURRENT)
        self.cur_val = cur[0]

        if self.cur_val % 2 != 0:
            color = self.canvas.gettags(self.cur_val)[0]
            if color == '#000000':
                return randint(0, 255), randint(0, 255), randint(0, 255)
            else:
                return hex_to_rgb(color)
        else:
            color = self.canvas.gettags(self.cur_val - 1)[0]
            return hex_to_rgb(color)

    def set_rgb_from_click(self, event):
        colors = self.get_rgb_from_click(event)
        d = ColorDialog(self.master,
                        current_red=str(colors[0]),
                        current_green=str(colors[1]),
                        current_blue=str(colors[2]),
                        test_btn_click=self.on_test_btn_click,
                        title="Adjust PWM value")

        if d.result is not None:
            if self.cur_val % 2 == 0:
                self.cur_val -= 1

            t = self.canvas.gettags(self.cur_val)
            t0 = to_rgb(d.result)
            t1 = t[1]
            self.canvas.itemconfigure(self.cur_val, tags=(t0, t1))
            self.colors_dict[str(t1)] = str(d.result)
            write_settings(CIRCLE_PWM_COLORS, self.colors_dict)
