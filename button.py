from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton, MDRectangleFlatButton
from kivymd.uix.screen import Screen


class BntApp(MDApp):
    def build(self):
        # self.theme_cls.primary_palette = "Amber"
        # self.theme_cls.primary_hue = "100"
        self.theme_cls.theme_style = "Light"
        screen = Screen()
        bnt_flat = MDRectangleFlatButton(text='Hello World', pos_hint={'center_x': 0.35, 'center_y': 0.5})
        btn_icon = MDFloatingActionButton(icon="lock-open-variant",
                                          pos_hint={'center_x': 0.75, 'center_y': 0.5},
                                          )
        screen.add_widget(bnt_flat)
        screen.add_widget(btn_icon)
        return screen


BntApp().run()
