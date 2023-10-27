from kivy.config import Config

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '900')

from kivy.properties import ObjectProperty
from kivymd.app import MDApp

import screen_helper
from kivy.lang import Builder

import socket


class LockApp(MDApp):
    layout_parent = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LockApp, self).__init__(**kwargs)
        self.serverAddress = ('192.168.178.104', 2222)
        self.UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.theme_cls.primary_palette = "Blue"
        self.screen = Builder.load_string(screen_helper.screen_helper)

        self.screen.ids.tf_temp.text = '30°C'
        self.screen.ids.tf_hum.text = '65%'


    def build(self):

        return self.screen

    def navigation_draw(self):
        print('navigation')

    def exit_app(self):
        LockApp().stop()

    def lock_cmd(self):
        cmd = 'unlock'
        cmd_encoded = cmd.encode('utf-8')
        self.UDPClient.sendto(cmd_encoded, self.serverAddress)


if __name__ == '__main__':
    LockApp().run()
