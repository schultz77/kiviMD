screen_helper = """
#:import Window kivy.core.window.Window
#:set color_shadow [0, 0, 0, .2980392156862745]

<Dialog>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "60dp"

    MDTextField:
        id: sever_address
        hint_text: "Server Address"
        icon_left: "server-network"
        helper_text: "use ipv4 format (see current address)"
        text_color_normal: 'red'



MDBoxLayout:
    id: layout_parent
    layout_1: layout_child 
    orientation: "vertical"

    MDTopAppBar:
        id: toolbar
        # title: 'Magic Lock'
        md_bg_color: app.theme_cls.primary_color
        left_action_items: [["menu", lambda x: app.set_server()]]
        right_action_items: [["exit-run", lambda x: app.exit_app()]]
        elevation: 5

    BoxLayout:
        height: self.minimum_height
        width: self.minimum_width
        # spacing: dp(60)
        size_hint_x: .8
        pos_hint: {"center_x": .5, "center_y": .5}
    
        MDBoxLayout:
            id: layout_child
            tf_temp: tf_temp
            tf_hum: tf_hum
            orientation: "vertical"
            spacing: "40dp"
            adaptive_height: True
            size_hint_x: .8
            pos_hint: {"center_x": .5, "center_y": .5}
            
            Image:
                source: 'images/image77.png'
                pos_hint:{'center_x': 0.5, 'center_y': .9}
                allow_stretch: True
                keep_ratio: True
                size_hint_y: None
                size_hint_x: None
                width: self.parent.width * 0.7
                height: self.parent.width/self.image_ratio
    
            MDTextField:
                id: tf_temp
                mode: "round"
                font_size: '30sp'
                halign: 'right'
                # hint_text: "Enter username"
                helper_text: "temperature °C"
                helper_text_mode: "persistent"
                icon_left: "home-thermometer-outline"

                icon_left_color: app.theme_cls.primary_color

                # pos_hint:{'center_x': 0.5, 'center_y': 0.5}
                # size: Window.width - dp(20), "50dp"
                # size_hint_x:1.5
                # width:300
                readonly: True
    
            MDTextField:
                id: tf_hum
                mode: "round"
                font_size: '30sp'
                halign: 'right'
                # hint_text: "Enter username"
                helper_text: "humidity %"
                helper_text_mode: "persistent"
                icon_left: "water-percent"
                # icon: "eye-off"
                icon_left_color: app.theme_cls.primary_color

                readonly: True
    
    
            MDIconButton:
                id: update_button
                icon: "cellphone-arrow-down"
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                icon_size: "48sp"
                on_release:
                    app.temp_hum_cmd()


    MDBottomAppBar:
        MDTopAppBar:
            id: BottomAppBar
            elevation: 1
            # left_action_items: [["coffee", lambda x: app.navigation_draw()]]
            mode: 'end'
            type: 'bottom'
            icon: "lock-open-variant"
            on_action_button: app.lock_cmd()
            md_bg_color: app.theme_cls.primary_color

"""
