from GuiPanels.BrightnessPanel import BrightnessPanel
from GuiPanels.ColorPanel import ColorPanel
from GuiPanels.OnOffPanel import OnOffPanel
from GuiPanels.StatusPanel import StatusPanel
from Serial.SerialInterface import convert_input_message

MESSAGE = "message"  # Message type
ACKNOWLEDGE = "ack"  # Acknowledge

COMMAND_R = "R"  # Red command
COMMAND_G = "G"  # Green command
COMMAND_B = "B"  # Blue command
COMMAND_S = "S"  # Scale command
COMMAND_FL = "FL"  # Flash command
COMMAND_ST = "ST"  # Strobe command
COMMAND_FA = "FA"  # Fade command
COMMAND_SM = "SM"  # Smooth command
COMMAND_R_RGB = "RGB"  # Get RGB command
COMMAND_R_SCA = "SCA"  # Get Scale command
COMMAND_R_STA = "STA"  # Get Status command

MESSAGE_U = "U"  # Up message
MESSAGE_D = "D"  # Down message

ACK_W_RGB = 0
ACK_R_RGB = 1
ACK_W_FLASH = 2
ACK_W_STROBE = 3
ACK_W_FADE = 4
ACK_W_SMOOTH = 5
ACK_W_SCALE = 6
ACK_R_SCALE = 7
ACK_R_STATE = 8

STATES = ("", "Flash", "Strobe", "Fade", "Smooth")


class MainScreen:
    def __init__(self, master, manager, end_command):
        self.master = master
        self.manager = manager

        self.R = 0
        self.G = 0
        self.B = 0
        self.state = 0
        self.scale = 0

        # Window settings
        self.master.wm_title("LED Strip Controller")

        # Layout stuff
        self.brightness_panel = self.set_brightness_panel(master)
        self.brightness_panel.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.onoff_panel = self.set_onoff_panel(master)
        self.onoff_panel.grid(row=0, column=2, columnspan=2, sticky='nsew')

        self.color_panel = self.set_color_panel(master)
        self.color_panel.grid(row=1, rowspan=5, column=0, columnspan=4, sticky='nsew')

        self.status_panel = StatusPanel(master)
        self.status_panel.grid(row=6, column=0, columnspan=4, sticky="nsew")

        # Initialize
        self.read_rgb()
        self.read_state()
        self.read_scale()

        # Update
        master.update()
        master.minsize(master.winfo_width(), master.winfo_height())
        master.configure(bg="white")
        master.resizable(0,0)

    def gui_update(self, queue):
        while queue.qsize():
            read = queue.get(0)
            if read:
                msg = None
                try:
                    msg = convert_input_message(read)
                except StandardError as e:
                    print "Error in MainScreen: my_serial.convert(read): %s" % e.message

                if msg is not None:
                    if msg.type == MESSAGE:
                        if msg.command == COMMAND_R_SCA:
                            self.scale = int(msg.message)
                            if self.state > 0:
                                self.status_panel.set_info_2("Speed: " + msg.message)
                            else:
                                self.status_panel.set_info_2("Brightness: " + str(self.scale))

                        elif msg.command == COMMAND_R_STA:
                            self.state = int(msg.message)
                            if self.state > 0:
                                self.status_panel.set_info_1(STATES[self.state])
                                self.status_panel.set_info_2("Speed: " + str(self.scale))
                            else:
                                self.status_panel.set_info_1(
                                    "R: " + str(self.R) + ", G: " + str(self.G) + " B: " + str(self.B))
                                self.status_panel.set_info_2("Brightness: " + str(self.scale))

                        else:
                            if msg.command == COMMAND_R:
                                self.R = msg.message
                                self.status_panel.set_info_1(
                                    "R: " + str(self.R) + ", G: " + str(self.G) + " B: " + str(self.B))
                            elif msg.command == COMMAND_G:
                                self.G = msg.message
                                self.status_panel.set_info_1(
                                    "R: " + str(self.R) + ", G: " + str(self.G) + " B: " + str(self.B))
                            elif msg.command == COMMAND_B:
                                self.B = msg.message
                                self.status_panel.set_info_1(
                                    "R: " + str(self.R) + ", G: " + str(self.G) + " B: " + str(self.B))

                    elif msg.type == ACKNOWLEDGE:
                        try:
                            ack_type = int(msg.message)
                            self.manager.my_serial.acknowledge_message(ack_type)
                        except ValueError as e:
                            print "Error in MainScreen: exception in acknowledge message ==> %s\n" % e.message

                        if ack_type == ACK_W_RGB:
                            self.status_panel.set_info_1(
                                "R: " + str(self.R) + ", G: " + str(self.G) + " B: " + str(self.B))
                        elif ack_type == ACK_W_SCALE:
                            self.read_scale()
                        else:
                            if not ack_type == ACK_R_STATE:
                                self.read_state()

    def set_rgb(self, r, g, b):
        self.R = r
        self.G = g
        self.B = b

    def write_rgb(self):
        mes = []
        com = ["R", "G", "B"]
        mes.append(self.R)
        mes.append(self.G)
        mes.append(self.B)
        self.manager.my_serial.serial_write_message_block(com, mes, 3, ACK_W_RGB)

    def read_rgb(self):
        self.manager.my_serial.serial_write_message(COMMAND_R_RGB, "", ACK_R_RGB)

    def read_scale(self):
        self.manager.my_serial.serial_write_message(COMMAND_R_SCA, "", ACK_R_SCALE)

    def read_state(self):
        self.manager.my_serial.serial_write_message(COMMAND_R_STA, "", ACK_R_STATE)

    def write_flash(self):
        self.manager.my_serial.serial_write_message(COMMAND_FL, "", ACK_W_FLASH)

    def write_strobe(self):
        self.manager.my_serial.serial_write_message(COMMAND_ST, "", ACK_W_STROBE)

    def write_fade(self):
        self.manager.my_serial.serial_write_message(COMMAND_FA, "", ACK_W_FADE)

    def write_smooth(self):
        self.manager.my_serial.serial_write_message(COMMAND_SM, "", ACK_W_SMOOTH)

    def set_color_panel(self, master):
        def on_btn_click(event):
            try:
                (self.R, self.G, self.B) = self.color_panel.get_rgb_from_click(event)
                self.write_rgb()
            except Exception as e:
                print "Error in MainScreen: exception in set_color_panel ==> %s\n" % e.message

        def on_flash_btn_click(event):
            self.write_flash()

        def on_strobe_btn_click(event):
            self.write_strobe()

        def on_fade_btn_click(event):
            self.write_fade()

        def on_smooth_btn_click(event):
            self.write_smooth()

        color_panel = ColorPanel(master,
                                 btn_click=on_btn_click,
                                 on_flash_btn_click=on_flash_btn_click,
                                 on_strobe_btn_click=on_strobe_btn_click,
                                 on_fade_btn_click=on_fade_btn_click,
                                 on_smooth_btn_click=on_smooth_btn_click
                                 )

        return color_panel

    def set_brightness_panel(self, master):
        def on_br_up_btn_click(event):
            self.manager.my_serial.serial_write_message(COMMAND_S, MESSAGE_U, ACK_W_SCALE)

        def on_br_do_btn_click(event):
            self.manager.my_serial.serial_write_message(COMMAND_S, MESSAGE_D, ACK_W_SCALE)

        main_panel = BrightnessPanel(master,
                               br_on_btn_click=on_br_up_btn_click,
                               br_off_btn_click=on_br_do_btn_click)

        return main_panel

    def set_onoff_panel(self, master):
        def on_on_btn_click(event):
            if self.state == 0:  # Colors
                self.set_rgb(self.R, self.G, self.B)
                self.write_rgb()
            elif self.state == 1:  # Flash
                self.write_flash()
            elif self.state == 2:  # Strobe
                self.write_strobe()
            elif self.state == 3:  # Fade
                self.write_fade()
            elif self.state == 4:  # Smooth
                self.write_smooth()

        def on_off_btn_click(event):
            mes = [0, 0, 0]
            com = ["R", "G", "B"]
            self.manager.my_serial.serial_write_message_block(com, mes, 3, ACK_W_RGB)

        main_panel = OnOffPanel(master,
                               on_btn_click=on_on_btn_click,
                               off_btn_click=on_off_btn_click)

        return main_panel
