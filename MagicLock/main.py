from kivy.config import Config

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '900')

from kivymd.app import MDApp

import screen_helper
from kivy.lang import Builder

import socket

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout

import ipaddress

from kivy.clock import Clock


class Dialog(BoxLayout):
    pass


class LockApp(MDApp):
    # layout_parent = ObjectProperty(None)
    screen = None

    def __init__(self, **kwargs):
        super(LockApp, self).__init__(**kwargs)
        self.serverAddress = ('192.168.178.104', 2222)
        self.UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPClient.setblocking(False)
        self.bufferSize = 1024

        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = '700'
        self.theme_cls.material_style = "M2"
        self.theme_cls.theme_style = "Dark"

        self.dialog = None
        self.lOCK_RELEASE_TIME = 6  # seconds

    def build(self):
        self.screen = Builder.load_string(screen_helper.screen_helper)
        return self.screen

    def set_server(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Change Server Address:",
                type="custom",
                content_cls=Dialog(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.dialog_close
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.update_server
                    ),
                ],
            )
        self.dialog.content_cls.ids.sever_address.text = self.serverAddress[0]
        self.dialog.content_cls.ids.sever_address.hint_text = "Server Address"
        self.dialog.content_cls.ids.sever_address.text_color_normal = 'red'
        self.dialog.open()

    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)

    def update_server(self, obj):

        if self.is_ipv4(self.dialog.content_cls.ids.sever_address.text):
            self.serverAddress = list(self.serverAddress)
            self.serverAddress[0] = self.dialog.content_cls.ids.sever_address.text
            self.serverAddress = tuple(self.serverAddress)
            self.dialog_close()
        else:
            self.dialog.content_cls.ids.sever_address.hint_text = "wrong format!"
            self.dialog.content_cls.ids.sever_address.text_color_normal = 'red'
            self.dialog.content_cls.ids.sever_address.text = self.serverAddress[0]

    @staticmethod
    def is_ipv4(string):
        try:
            ipaddress.IPv4Network(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def exit_app():
        LockApp().stop()

    def lock_cmd(self):
        cmd = 'unlock'
        cmd_encoded = cmd.encode('utf-8')
        self.UDPClient.sendto(cmd_encoded, self.serverAddress)
        self.screen.ids.BottomAppBar.icon_color = (0, 1, 0, 1)
        self.screen.ids.BottomAppBar.title = "unlocked"
        Clock.schedule_once(self.icon_color_reset, self.lOCK_RELEASE_TIME)

    def icon_color_reset(self, dt):
        self.screen.ids.BottomAppBar.icon_color = self.theme_cls.primary_color
        self.screen.ids.BottomAppBar.title = "released"
        Clock.schedule_once(self.clean_toolbar, self.lOCK_RELEASE_TIME)

    def clean_toolbar(self, dt):
        self.screen.ids.BottomAppBar.title = ""

    def temp_hum_cmd(self):
        cmd = 'temperature'
        cmd_encoded = cmd.encode('utf-8')
        self.UDPClient.sendto(cmd_encoded, self.serverAddress)

        cnt = 0
        while cnt < 10:
            try:
                message, address = self.UDPClient.recvfrom(self.bufferSize)
            except OSError:
                pass
            else:
                message_decoded = message.decode('utf-8')
                data = message_decoded.split(',')
                temperature = data[0] + '°C'
                humidity = data[1] + '%'

                self.screen.ids.tf_temp.text = temperature
                self.screen.ids.tf_hum.text = humidity
            cnt += 1


if __name__ == '__main__':
    LockApp().run()
