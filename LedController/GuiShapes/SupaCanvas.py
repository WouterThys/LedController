from Tkinter import *


class SupaCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)

    def create_rounded(self, x1, y1, x2, y2, r, color="red"):
        self.create_arc(x1, y1, x1 + r, y1 + r, start=90, extent=90, style=PIESLICE, fill=color, outline=color)
        self.create_arc(x2 - r, y1, x2, y1 + r, start=0, extent=90, style=PIESLICE, fill=color, outline=color)
        self.create_arc(x1, y2 - r, x1 + r, y2, start=180, extent=90, style=PIESLICE, fill=color, outline=color)
        self.create_arc(x2 - r, y2 - r, x2, y2, start=270, extent=90, style=PIESLICE, fill=color, outline=color)
        self.create_rectangle(x1 + r / 2, y1, x2 - r / 2, y2, fill=color, outline=color)
        self.create_rectangle(x1, y1 + r / 2, x2, y2 - r /2, fill=color, outline=color)