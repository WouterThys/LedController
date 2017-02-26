

class MyCircle(object):
    def __init__(self, x, y, r, text="", name=None):
        self.x = x
        self.y = y
        self.r = r
        self.coords = (x-r, y-r, x+r, y+r)
        self.text = text
        self.name = name
        self.item = None
        self.pwm_color = None
        self.canvas = None

    def draw(self, canvas, textcolor="white", outline="black", fill="white", activefill="gray",
             left_btn_click=None, right_btn_click=None, tags=None, image=None, pwm_color=None):
        if pwm_color is None:
            self.pwm_color = fill
        else:
            self.pwm_color = pwm_color
        self.canvas = canvas
        self.item = canvas.create_oval(self.coords, outline=outline, fill=fill, activefill=activefill, width=2, tags=tags)
        if not image is None:
            canvas.create_image(self.x, self.y, image=image)

        if outline == "black":
            text = canvas.create_text(self.x, self.y, text=self.text, fill=textcolor)
        else:
            text = canvas.create_text(self.x, self.y, text=self.text, fill=outline)

        # Add colors to tags
        t = (str(self.pwm_color), str(tags))
        canvas.itemconfig(self.item, tags=t)

        # Left button click
        canvas.tag_bind(self.item, "<1>", left_btn_click)
        canvas.tag_bind(text, "<1>", left_btn_click)

        # Right button click
        canvas.tag_bind(self.item, "<3>", right_btn_click)
        canvas.tag_bind(text, "<3>", right_btn_click)

    def set_colors(self, red, green, blue):
        self.pwm_color = (red, green, blue)
        self.canvas.itemconfig(self.item, fill="#%02x%02x%02x" % (red, green, blue))