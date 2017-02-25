from Tkinter import *


class StatusPanel(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        # Panel settings
        self.config(bd=1, relief=RAISED, padx=2, pady=2)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        content_frame = Frame(self, bd=1, relief=SUNKEN, padx=1, pady=1)
        content_frame.grid(sticky="nsew")

        self.info1_txt = StringVar()
        self.info1_lbl = Label(content_frame, textvariable=self.info1_txt, fg="dim gray").pack(side=LEFT, fill=X)
        self.info2_txt = StringVar()
        self.info2_lbl = Label(content_frame, textvariable=self.info2_txt, fg="dim gray").pack(side=RIGHT, fill=X)
        # self.info3_txt = StringVar()
        # self.info3_lbl = Label(content_frame, textvariable=self.info3_txt, fg="dim gray").pack(side=RIGHT, fill=X)

        self.info1_txt.set("")
        self.info2_txt.set("")
        # self.info3_txt.set("")

    def set_info_1(self, text):
        self.info1_txt.set(str(text))

    def set_info_2(self, text):
        self.info2_txt.set(str(text))

    # def set_info_3(self, text):
    #     self.info3_txt.set(str(text))