from Tkinter import *
import os


class ColorDialog(Toplevel):
    def __init__(self, parent,
                 current_red,
                 current_green,
                 current_blue,
                 test_btn_click=None,
                 title=None):

        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.test_btn_click = test_btn_click

        self.r = current_red
        self.g = current_green
        self.b = current_blue

        if current_red:
            self.red_txt = StringVar()
            self.red_txt.set(current_red)
        if current_green:
            self.green_txt = StringVar()
            self.green_txt.set(current_green)
        if current_blue:
            self.blue_txt = StringVar()
            self.blue_txt.set(current_blue)
        self.red_en = None
        self.green_en = None
        self.blue_en = None

        if title:
            self.title(title)

        self.parent = parent
        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))

        self.initial_focus.focus_set()
        self.wait_window(self)

    #
    # construction hooks
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        Label(master, text="Red").grid(row=0, column=0, sticky='nsew')
        Label(master, text="Green").grid(row=0, column=1, sticky='nsew')
        Label(master, text="Blue").grid(row=0, column=2, sticky='nsew')

        vcmd = (master.register(self.validate_number),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.red_en = Entry(master, textvariable=self.red_txt, validate='key', validatecommand=vcmd)
        self.green_en = Entry(master, textvariable=self.green_txt, validate='key', validatecommand=vcmd)
        self.blue_en = Entry(master, textvariable=self.blue_txt, validate='key', validatecommand=vcmd)

        def up_key(val, event=None):
            if val.get() == '':
                v = 0
            else:
                v = int(val.get())
            v += 1
            if v > 255:
                v = 0
            val.set(v)

        def down_key(val, event=None):
            if val.get() == '':
                v = 0
            else:
                v = int(val.get())
            v -= 1
            if v < 0:
                v = 255
            val.set(v)

        self.red_en.bind("<Up>", lambda x: up_key(self.red_txt))
        self.green_en.bind("<Up>", lambda x: up_key(self.green_txt))
        self.blue_en.bind("<Up>", lambda x: up_key(self.blue_txt))
        self.red_en.bind("<Down>", lambda x: down_key(self.red_txt))
        self.green_en.bind("<Down>", lambda x: down_key(self.green_txt))
        self.blue_en.bind("<Down>", lambda x: down_key(self.blue_txt))

        self.red_en.grid(row=1, column=0, sticky='nsew')
        self.green_en.grid(row=1, column=1, sticky='nsew')
        self.blue_en.grid(row=1, column=2, sticky='nsew')
        return self.red_en

    def validate_number(self, action, index, value_if_allowed, prior_value, text, validation_type,
                        trigger_type, widget_name):
        if text in ' 0123456789':
            if value_if_allowed == '':
                return True

            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Test", width=10,
                   command=self.test)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind('t', self.test)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    def test(self, event=None):
        self.validate_vlaues()
        self.test_btn_click(self.r, self.g, self.b)

    def validate_vlaues(self):
        r_txt = self.red_txt.get()
        g_txt = self.green_txt.get()
        b_txt = self.blue_txt.get()

        if r_txt == '':
            r_txt = '0'
            self.red_txt.set(r_txt)
        elif int(r_txt) > 255:
            r_txt = '255'
            self.red_txt.set(r_txt)

        if g_txt == '':
            g_txt = '0'
            self.green_txt.set('0')
        elif int(g_txt) > 255:
            g_txt = '255'
            self.green_txt.set(g_txt)

        if b_txt == '':
            b_txt = '0'
            self.blue_txt.set('0')
        elif int(b_txt) > 255:
            b_txt = '255'
            self.blue_txt.set(b_txt)

        self.r = int(r_txt)
        self.g = int(g_txt)
        self.b = int(b_txt)

    #
    # command hooks
    def validate(self):
        return 1 # override

    def apply(self):
        self.test()
        self.result =  self.r, self.g, self.b