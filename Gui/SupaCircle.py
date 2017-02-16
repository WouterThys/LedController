from Tkinter import *


class MyCircle(object):
    def __init__(self, x, y, r, text="", name=None):
        self.x = x
        self.y = y
        self.r = r
        self.coords = (x-r, y-r, x+r, y+r)
        self.text = text
        self.name = name

    def draw(self, canvas, textcolor="white", outline="black", fill="white", activefill="gray", btn_click=None, tags=None):
        item = canvas.create_oval(self.coords, outline=outline, fill=fill, activefill=activefill, width=2, tags=tags)
        canvas.tag_bind(item, "<1>", btn_click)
        if outline == "black":
            text = canvas.create_text(self.x, self.y, text=self.text, fill=textcolor)
        else:
            text = canvas.create_text(self.x, self.y, text=self.text, fill=outline)
        canvas.tag_bind(text, "<1>", btn_click)

    def on_mouse_click(self, event):
        print "I got clicked: (%s)" % self.name