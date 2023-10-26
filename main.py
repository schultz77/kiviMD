# config
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')

from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
import helpers
from kivy.lang import Builder


class DemoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        screen = Screen()

        # username = MDTextField()
        # size_hint_x=None, width=200)

        username = Builder.load_string(helpers.username_input)
        screen.add_widget(username)
        return screen


DemoApp().run()
